#    Copyright 2016 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import six

from oslo_log import log as logging
from oslo_service import periodic_task
from oslo_utils import excutils
from oslo_utils import uuidutils

from zun.common import consts
from zun.common import exception
from zun.common.i18n import _
from zun.common import utils
from zun.common.utils import translate_exception
from zun.compute import compute_node_tracker
import zun.conf
from zun.container import driver
from zun.image import driver as image_driver
from zun.image.glance import driver as glance
from zun import objects

CONF = zun.conf.CONF
LOG = logging.getLogger(__name__)


class Manager(periodic_task.PeriodicTasks):
    """Manages the running containers."""

    def __init__(self, container_driver=None):
        super(Manager, self).__init__(CONF)
        self.driver = driver.load_container_driver(container_driver)
        self.host = CONF.host
        self._resource_tracker = None
        if self._use_sandbox():
            self.use_sandbox = True
        else:
            self.use_sandbox = False

    def _fail_container(self, context, container, error, unset_host=False):
        container.status = consts.ERROR
        container.status_reason = error
        container.task_state = None
        if unset_host:
            container.host = None
        container.save(context)

    def container_create(self, context, limits, requested_networks, container):
        utils.spawn_n(self._do_container_create, context, container,
                      requested_networks, limits)

    def container_run(self, context, limits, requested_networks, container):
        utils.spawn_n(self._do_container_run, context, container,
                      requested_networks, limits)

    def _do_container_run(self, context, container, requested_networks,
                          limits=None):
        created_container = self._do_container_create(context,
                                                      container,
                                                      requested_networks,
                                                      limits)
        if created_container:
            self._do_container_start(context, created_container)

    def _do_sandbox_cleanup(self, context, container):
        sandbox_id = container.get_sandbox_id()
        if sandbox_id is None:
            return

        try:
            self.driver.delete_sandbox(context, container)
        except Exception as e:
            LOG.error("Error occurred while deleting sandbox: %s",
                      six.text_type(e))

    def _update_task_state(self, context, container, task_state):
        container.task_state = task_state
        container.save(context)

    def _do_container_create_base(self, context, container, requested_networks,
                                  sandbox=None, limits=None, reraise=False):
        self._update_task_state(context, container, consts.IMAGE_PULLING)
        repo, tag = utils.parse_image_name(container.image)
        image_pull_policy = utils.get_image_pull_policy(
            container.image_pull_policy, tag)
        image_driver_name = container.image_driver
        try:
            image, image_loaded = image_driver.pull_image(
                context, repo, tag, image_pull_policy, image_driver_name)
            image['repo'], image['tag'] = repo, tag
            if not image_loaded:
                self.driver.load_image(image['path'])
        except exception.ImageNotFound as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.error(six.text_type(e))
                self._do_sandbox_cleanup(context, container)
                self._fail_container(context, container, six.text_type(e))
            return
        except exception.DockerError as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.error("Error occurred while calling Docker image API: %s",
                          six.text_type(e))
                self._do_sandbox_cleanup(context, container)
                self._fail_container(context, container, six.text_type(e))
            return
        except Exception as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.exception("Unexpected exception: %s",
                              six.text_type(e))
                self._do_sandbox_cleanup(context, container)
                self._fail_container(context, container, six.text_type(e))
            return

        container.task_state = consts.CONTAINER_CREATING
        container.image_driver = image.get('driver')
        container.save(context)
        try:
            limits = limits
            rt = self._get_resource_tracker()
            if image['driver'] == 'glance':
                self.driver.read_tar_image(image)
            with rt.container_claim(context, container, container.host,
                                    limits):
                container = self.driver.create(context, container, image,
                                               requested_networks)
                self._update_task_state(context, container, None)
                return container
        except exception.DockerError as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.error("Error occurred while calling Docker create API: %s",
                          six.text_type(e))
                self._do_sandbox_cleanup(context, container)
                self._fail_container(context, container, six.text_type(e),
                                     unset_host=True)
            return
        except Exception as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.exception("Unexpected exception: %s",
                              six.text_type(e))
                self._do_sandbox_cleanup(context, container)
                self._fail_container(context, container, six.text_type(e),
                                     unset_host=True)
            return

    def _do_container_create(self, context, container, requested_networks,
                             limits=None, reraise=False):
        LOG.debug('Creating container: %s', container.uuid)

        # check if container driver is NovaDockerDriver and
        # security_groups is non empty, then return by setting
        # the error message in database
        if ('NovaDockerDriver' in CONF.container_driver and
                container.security_groups):
            msg = "security_groups can not be provided with NovaDockerDriver"
            self._fail_container(self, context, container, msg)
            return

        sandbox = None
        if self.use_sandbox:
            sandbox = self._create_sandbox(context, container,
                                           requested_networks, reraise)
            if sandbox is None:
                return

        created_container = self._do_container_create_base(context,
                                                           container,
                                                           requested_networks,
                                                           sandbox, limits,
                                                           reraise)
        return created_container

    def _use_sandbox(self):
        if CONF.use_sandbox and self.driver.capabilities["support_sandbox"]:
            return True
        elif (not CONF.use_sandbox and
                self.driver.capabilities["support_standalone"]):
            return False
        else:
            raise exception.ZunException(_(
                "The configuration of use_sandbox '%(use_sandbox)s' is not "
                "supported by driver '%(driver)s'.") %
                {'use_sandbox': CONF.use_sandbox,
                 'driver': self.driver})

    def _create_sandbox(self, context, container, requested_networks,
                        reraise=False):
        self._update_task_state(context, container, consts.SANDBOX_CREATING)
        sandbox_image = CONF.sandbox_image
        sandbox_image_driver = CONF.sandbox_image_driver
        sandbox_image_pull_policy = CONF.sandbox_image_pull_policy
        repo, tag = utils.parse_image_name(sandbox_image)
        try:
            image, image_loaded = image_driver.pull_image(
                context, repo, tag, sandbox_image_pull_policy,
                sandbox_image_driver)
            if not image_loaded:
                self.driver.load_image(image['path'])
            sandbox_id = self.driver.create_sandbox(
                context, container, image=sandbox_image,
                requested_networks=requested_networks)
            return sandbox_id
        except Exception as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.exception("Unexpected exception: %s",
                              six.text_type(e))
                self._fail_container(context, container, six.text_type(e))

    def _do_container_start(self, context, container, reraise=False):
        LOG.debug('Starting container: %s', container.uuid)
        self._update_task_state(context, container, consts.CONTAINER_STARTING)
        try:
            container = self.driver.start(context, container)
            self._update_task_state(context, container, None)
            return container
        except exception.DockerError as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.error("Error occurred while calling Docker start API: %s",
                          six.text_type(e))
                self._fail_container(context, container, six.text_type(e))
        except Exception as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.exception("Unexpected exception: %s",
                              six.text_type(e))
                self._fail_container(context, container, six.text_type(e))

    @translate_exception
    def container_delete(self, context, container, force):
        LOG.debug('Deleting container: %s', container.uuid)
        self._update_task_state(context, container, consts.CONTAINER_DELETING)
        reraise = not force
        try:
            self.driver.delete(context, container, force)
        except exception.DockerError as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.error(("Error occurred while calling Docker  "
                           "delete API: %s"), six.text_type(e))
                self._fail_container(context, container, six.text_type(e))
        except Exception as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.exception("Unexpected exception: %s", six.text_type(e))
                self._fail_container(context, container, six.text_type(e))

        if self.use_sandbox:
            self._delete_sandbox(context, container, reraise)

        self._update_task_state(context, container, None)
        container.destroy(context)
        self._get_resource_tracker()

        # Remove the claimed resource
        rt = self._get_resource_tracker()
        rt.remove_usage_from_container(context, container, True)
        return container

    def _delete_sandbox(self, context, container, reraise=False):
        sandbox_id = container.get_sandbox_id()
        if sandbox_id:
            self._update_task_state(context, container,
                                    consts.SANDBOX_DELETING)
            try:
                self.driver.delete_sandbox(context, container)
            except Exception as e:
                with excutils.save_and_reraise_exception(reraise=reraise):
                    LOG.exception("Unexpected exception: %s", six.text_type(e))
                    self._fail_container(context, container, six.text_type(e))

    def add_security_group(self, context, container, security_group):
        utils.spawn_n(self._add_security_group, context, container,
                      security_group)

    def _add_security_group(self, context, container, security_group):
        LOG.debug('Adding security_group to container: %s', container.uuid)
        try:
            self.driver.add_security_group(context, container, security_group)
            container.security_groups += [security_group]
            container.save(context)
        except Exception as e:
            with excutils.save_and_reraise_exception(reraise=False):
                LOG.exception("Unexpected exception: %s", six.text_type(e))

    @translate_exception
    def container_list(self, context):
        LOG.debug('Listing container...')
        try:
            return self.driver.list(context)
        except exception.DockerError as e:
            LOG.error("Error occurred while calling Docker list API: %s",
                      six.text_type(e))
            raise
        except Exception as e:
            LOG.exception("Unexpected exception: %s", six.text_type(e))
            raise

    @translate_exception
    def container_show(self, context, container):
        LOG.debug('Showing container: %s', container.uuid)
        try:
            container = self.driver.show(context, container)
            if container.obj_what_changed():
                container.save(context)
            return container
        except exception.DockerError as e:
            LOG.error("Error occurred while calling Docker show API: %s",
                      six.text_type(e))
            raise
        except Exception as e:
            LOG.exception("Unexpected exception: %s", six.text_type(e))
            raise

    def _do_container_reboot(self, context, container, timeout, reraise=False):
        LOG.debug('Rebooting container: %s', container.uuid)
        self._update_task_state(context, container, consts.CONTAINER_REBOOTING)
        try:
            container = self.driver.reboot(context, container, timeout)
            self._update_task_state(context, container, None)
            return container
        except exception.DockerError as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.error(("Error occurred while calling Docker reboot "
                           "API: %s"), six.text_type(e))
                self._fail_container(context, container, six.text_type(e))
        except Exception as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.exception("Unexpected exception: %s",
                              six.text_type(e))
                self._fail_container(context, container, six.text_type(e))

    def container_reboot(self, context, container, timeout):
        utils.spawn_n(self._do_container_reboot, context, container, timeout)

    def _do_container_stop(self, context, container, timeout, reraise=False):
        LOG.debug('Stopping container: %s', container.uuid)
        self._update_task_state(context, container, consts.CONTAINER_STOPPING)
        try:
            container = self.driver.stop(context, container, timeout)
            self._update_task_state(context, container, None)
            return container
        except exception.DockerError as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.error("Error occurred while calling Docker stop API: %s",
                          six.text_type(e))
                self._fail_container(context, container, six.text_type(e))
        except Exception as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.exception("Unexpected exception: %s",
                              six.text_type(e))
                self._fail_container(context, container, six.text_type(e))

    def container_stop(self, context, container, timeout):
        utils.spawn_n(self._do_container_stop, context, container, timeout)

    def container_start(self, context, container):
        utils.spawn_n(self._do_container_start, context, container)

    def _do_container_pause(self, context, container, reraise=False):
        LOG.debug('Pausing container: %s', container.uuid)
        try:
            container = self.driver.pause(context, container)
            container.save(context)
            return container
        except exception.DockerError as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.error("Error occurred while calling Docker pause API: %s",
                          six.text_type(e))
                self._fail_container(context, container, six.text_type(e))
        except Exception as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.exception("Unexpected exception: %s,",
                              six.text_type(e))
                self._fail_container(context, container, six.text_type(e))

    def container_pause(self, context, container):
        utils.spawn_n(self._do_container_pause, context, container)

    def _do_container_unpause(self, context, container, reraise=False):
        LOG.debug('Unpausing container: %s', container.uuid)
        try:
            container = self.driver.unpause(context, container)
            container.save(context)
            return container
        except exception.DockerError as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.error(
                    "Error occurred while calling Docker unpause API: %s",
                    six.text_type(e))
                self._fail_container(context, container, six.text_type(e))
        except Exception as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.exception("Unexpected exception: %s",
                              six.text_type(e))
                self._fail_container(context, container, six.text_type(e))

    def container_unpause(self, context, container):
        utils.spawn_n(self._do_container_unpause, context, container)

    @translate_exception
    def container_logs(self, context, container, stdout, stderr,
                       timestamps, tail, since):
        LOG.debug('Showing container logs: %s', container.uuid)
        try:
            return self.driver.show_logs(context, container,
                                         stdout=stdout, stderr=stderr,
                                         timestamps=timestamps, tail=tail,
                                         since=since)
        except exception.DockerError as e:
            LOG.error("Error occurred while calling Docker logs API: %s",
                      six.text_type(e))
            raise
        except Exception as e:
            LOG.exception("Unexpected exception: %s", six.text_type(e))
            raise

    @translate_exception
    def container_exec(self, context, container, command, run, interactive):
        LOG.debug('Executing command in container: %s', container.uuid)
        try:
            exec_id = self.driver.execute_create(context, container, command,
                                                 interactive)
            if run:
                return self.driver.execute_run(exec_id, command)
            else:
                return {'exec_id': exec_id,
                        'url': CONF.docker.docker_remote_api_url}
        except exception.DockerError as e:
            LOG.error("Error occurred while calling Docker exec API: %s",
                      six.text_type(e))
            raise
        except Exception as e:
            LOG.exception("Unexpected exception: %s", six.text_type(e))
            raise

    @translate_exception
    def container_exec_resize(self, context, exec_id, height, width):
        LOG.debug('Resizing the tty session used by the exec: %s', exec_id)
        try:
            return self.driver.execute_resize(exec_id, height, width)
        except exception.DockerError as e:
            LOG.error("Error occurred while calling Docker exec API: %s",
                      six.text_type(e))
            raise
        except Exception as e:
            LOG.exception("Unexpected exception: %s", six.text_type(e))
            raise

    def _do_container_kill(self, context, container, signal, reraise=False):
        LOG.debug('Killing a container: %s', container.uuid)
        try:
            container = self.driver.kill(context, container, signal)
            container.save(context)
            return container
        except exception.DockerError as e:
            with excutils.save_and_reraise_exception(reraise=reraise):
                LOG.error("Error occurred while calling Docker kill API: %s",
                          six.text_type(e))
                self._fail_container(context, container, six.text_type(e))

    def container_kill(self, context, container, signal):
        utils.spawn_n(self._do_container_kill, context, container, signal)

    @translate_exception
    def container_update(self, context, container, patch):
        LOG.debug('Updating a container: %s', container.uuid)
        # Update only the fields that have changed
        for field, patch_val in patch.items():
            if getattr(container, field) != patch_val:
                setattr(container, field, patch_val)

        try:
            self.driver.update(context, container)
            container.save(context)
            return container
        except exception.DockerError as e:
            LOG.error("Error occurred while calling docker API: %s",
                      six.text_type(e))
            raise

    @translate_exception
    def container_attach(self, context, container):
        LOG.debug('Get websocket url from the container: %s', container.uuid)
        try:
            url = self.driver.get_websocket_url(context, container)
            token = uuidutils.generate_uuid()
            access_url = '%s?token=%s&uuid=%s' % (
                CONF.websocket_proxy.base_url, token, container.uuid)
            container.websocket_url = url
            container.websocket_token = token
            container.save(context)
            return access_url
        except Exception as e:
            LOG.error(("Error occurred while calling "
                       "get websocket url function: %s"),
                      six.text_type(e))
            raise

    @translate_exception
    def container_resize(self, context, container, height, width):
        LOG.debug('Resize tty to the container: %s', container.uuid)
        try:
            container = self.driver.resize(context, container, height, width)
            return container
        except exception.DockerError as e:
            LOG.error(("Error occurred while calling docker "
                       "resize API: %s"),
                      six.text_type(e))
            raise

    @translate_exception
    def container_top(self, context, container, ps_args):
        LOG.debug('Displaying the running processes inside the container: %s',
                  container.uuid)
        try:
            return self.driver.top(context, container, ps_args)
        except exception.DockerError as e:
            LOG.error("Error occurred while calling Docker top API: %s",
                      six.text_type(e))
            raise
        except Exception as e:
            LOG.exception("Unexpected exception: %s", six.text_type(e))
            raise

    @translate_exception
    def container_get_archive(self, context, container, path):
        LOG.debug('Copying resource from the container: %s', container.uuid)
        try:
            return self.driver.get_archive(context, container, path)
        except exception.DockerError as e:
            LOG.error(
                "Error occurred while calling Docker get_archive API: %s",
                six.text_type(e))
            raise
        except Exception as e:
            LOG.exception("Unexpected exception: %s", six.text_type(e))
            raise

    @translate_exception
    def container_put_archive(self, context, container, path, data):
        LOG.debug('Copying resource to the container: %s', container.uuid)
        try:
            return self.driver.put_archive(context, container, path, data)
        except exception.DockerError as e:
            LOG.error(
                "Error occurred while calling Docker put_archive API: %s",
                six.text_type(e))
            raise
        except Exception as e:
            LOG.exception("Unexpected exception: %s", six.text_type(e))
            raise

    @translate_exception
    def container_stats(self, context, container):
        LOG.debug('Displaying stats of the container: %s', container.uuid)
        try:
            return self.driver.stats(context, container)
        except exception.DockerError as e:
            LOG.error("Error occurred while calling Docker stats API: %s",
                      six.text_type(e))
            raise
        except Exception as e:
            LOG.exception("Unexpected exception: %s", six.text_type(e))
            raise

    @translate_exception
    def container_commit(self, context, container, repository, tag=None):
        LOG.debug('Committing the container: %s', container.uuid)
        snapshot_image = None
        try:
            # NOTE(miaohb): Glance is the only driver that support image
            # uploading in the current version, so we have hard-coded here.
            # https://bugs.launchpad.net/zun/+bug/1697342
            snapshot_image = image_driver.create_image(context, repository,
                                                       glance.GlanceDriver())
        except exception.DockerError as e:
            LOG.error("Error occurred while calling glance "
                      "create_image API: %s",
                      six.text_type(e))
        utils.spawn_n(self._do_container_commit, context, snapshot_image,
                      container, repository, tag)
        return snapshot_image.id

    def _do_container_image_upload(self, context, snapshot_image, data, tag):
        try:
            image_driver.upload_image_data(context, snapshot_image,
                                           tag, data, glance.GlanceDriver())
        except Exception as e:
            LOG.exception("Unexpected exception while uploading image: %s",
                          six.text_type(e))
            raise

    def _do_container_commit(self, context, snapshot_image, container,
                             repository, tag=None):
        LOG.debug('Creating image...')
        if tag is None:
            tag = 'latest'

        try:
            container_image_id = self.driver.commit(context, container,
                                                    repository, tag)
            container_image = self.driver.get_image(repository + ':' + tag)
        except exception.DockerError as e:
            LOG.error("Error occurred while calling docker commit API: %s",
                      six.text_type(e))
            raise
        LOG.debug('Upload image %s to glance', container_image_id)
        self._do_container_image_upload(context, snapshot_image,
                                        container_image, tag)

    def image_pull(self, context, image):
        utils.spawn_n(self._do_image_pull, context, image)

    def _do_image_pull(self, context, image):
        LOG.debug('Creating image...')
        repo_tag = image.repo + ":" + image.tag
        try:
            pulled_image, image_loaded = image_driver.pull_image(
                context, image.repo, image.tag)
            if not image_loaded:
                self.driver.load_image(pulled_image['path'])
            image_dict = self.driver.inspect_image(repo_tag)
            image.image_id = image_dict['Id']
            image.size = image_dict['Size']
            image.save()
        except exception.ImageNotFound as e:
            LOG.error(six.text_type(e))
            return
        except exception.DockerError as e:
            LOG.error("Error occurred while calling Docker image API: %s",
                      six.text_type(e))
            raise
        except Exception as e:
            LOG.exception("Unexpected exception: %s",
                          six.text_type(e))
            raise

    @translate_exception
    def image_search(self, context, image, image_driver_name, exact_match):
        LOG.debug('Searching image...', image=image)
        try:
            return image_driver.search_image(context, image,
                                             image_driver_name, exact_match)
        except Exception as e:
            LOG.exception("Unexpected exception while searching image: %s",
                          six.text_type(e))
            raise

    def _get_resource_tracker(self):
        if not self._resource_tracker:
            rt = compute_node_tracker.ComputeNodeTracker(self.host,
                                                         self.driver)
            self._resource_tracker = rt
        return self._resource_tracker

    @periodic_task.periodic_task(run_immediately=True)
    def delete_unused_containers(self, context):
        """Delete container with status DELETED"""
        # NOTE(kiennt): Need to filter with both status (DELETED) and
        #               task_state (None). If task_state in
        #               [CONTAINER_DELETING, SANDBOX_DELETING] it may
        #               raise some errors when try to delete container.
        filters = {
            'auto_remove': True,
            'status': consts.DELETED,
            'task_state': None,
        }
        containers = objects.Container.list(context,
                                            filters=filters)

        if containers:
            for container in containers:
                try:
                    msg = ('%(behavior)s deleting container '
                           '%(container_name)s with status DELETED')
                    LOG.info(msg, {'behavior': 'Start',
                                   'container_name': container.name})
                    self.container_delete(context, container, True)
                    LOG.info(msg, {'behavior': 'Complete',
                                   'container_name': container.name})
                except exception.DockerError:
                    return
                except Exception:
                    return

    def capsule_create(self, context, capsule, requested_networks, limits):
        utils.spawn_n(self._do_capsule_create, context,
                      capsule, requested_networks, limits)

    def _do_capsule_create(self, context, capsule, requested_networks=None,
                           limits=None, reraise=False):
        capsule.containers[0].image = CONF.sandbox_image
        capsule.containers[0].image_driver = CONF.sandbox_image_driver
        capsule.containers[0].image_pull_policy = \
            CONF.sandbox_image_pull_policy
        capsule.containers[0].save(context)
        sandbox = self._create_sandbox(context,
                                       capsule.containers[0],
                                       requested_networks, reraise)
        self._update_task_state(context, capsule.containers[0], None)
        capsule.containers[0].status = consts.RUNNING
        capsule.containers[0].save(context)
        sandbox_id = capsule.containers[0].get_sandbox_id()
        count = len(capsule.containers)
        for k in range(1, count):
            capsule.containers[k].set_sandbox_id(sandbox_id)
            capsule.containers[k].addresses = capsule.containers[0].addresses
            created_container = \
                self._do_container_create_base(context,
                                               capsule.containers[k],
                                               requested_networks,
                                               sandbox,
                                               limits)
            if created_container:
                self._do_container_start(context, created_container)
