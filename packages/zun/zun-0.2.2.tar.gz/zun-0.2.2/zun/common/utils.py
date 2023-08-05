# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# It's based on oslo.i18n usage in OpenStack Keystone project and
# recommendations from
# https://docs.openstack.org/oslo.i18n/latest/user/usage.html

"""Utilities and helper functions."""
import eventlet
import functools
import mimetypes
import time

from oslo_concurrency import lockutils
from oslo_context import context as common_context
from oslo_log import log as logging
from oslo_service import loopingcall
import pecan
import six

from zun.common import clients
from zun.common import consts
from zun.common import exception
from zun.common.i18n import _
import zun.conf

CONF = zun.conf.CONF
LOG = logging.getLogger(__name__)

synchronized = lockutils.synchronized_with_prefix('zun-')

VALID_STATES = {
    'commit': [consts.RUNNING, consts.STOPPED, consts.PAUSED],
    'delete': [consts.CREATED, consts.ERROR, consts.STOPPED, consts.DELETED],
    'delete_force': [consts.CREATED, consts.CREATING, consts.ERROR,
                     consts.RUNNING, consts.STOPPED, consts.UNKNOWN,
                     consts.DELETED],
    'start': [consts.CREATED, consts.STOPPED, consts.ERROR],
    'stop': [consts.RUNNING],
    'reboot': [consts.CREATED, consts.RUNNING, consts.STOPPED, consts.ERROR],
    'pause': [consts.RUNNING],
    'unpause': [consts.PAUSED],
    'kill': [consts.RUNNING],
    'execute': [consts.RUNNING],
    'execute_resize': [consts.RUNNING],
    'update': [consts.CREATED, consts.RUNNING, consts.STOPPED, consts.PAUSED],
    'attach': [consts.RUNNING],
    'resize': [consts.RUNNING],
    'top': [consts.RUNNING],
    'get_archive': [consts.CREATED, consts.PAUSED, consts.RUNNING,
                    consts.STOPPED],
    'put_archive': [consts.CREATED, consts.PAUSED, consts.RUNNING,
                    consts.STOPPED],
    'logs': [consts.CREATED, consts.ERROR, consts.PAUSED, consts.RUNNING,
             consts.STOPPED, consts.UNKNOWN],
    'stats': [consts.RUNNING],
    'add_security_group': [consts.CREATED, consts.RUNNING, consts.STOPPED,
                           consts.PAUSED]
}


def validate_container_state(container, action):
    if container.status not in VALID_STATES[action]:
        raise exception.InvalidStateException(
            id=container.uuid,
            action=action,
            actual_state=container.status)


def safe_rstrip(value, chars=None):
    """Removes trailing characters from a string if that does not make it empty

    :param value: A string value that will be stripped.
    :param chars: Characters to remove.
    :return: Stripped value.

    """
    if not isinstance(value, six.string_types):
        LOG.warning((
            "Failed to remove trailing character. Returning original object. "
            "Supplied object is not a string: %s."
        ), value)
        return value

    return value.rstrip(chars) or value


def _do_allow_certain_content_types(func, content_types_list):
    # Allows you to bypass pecan's content-type restrictions
    cfg = pecan.util._cfg(func)
    cfg.setdefault('content_types', {})
    cfg['content_types'].update((value, '')
                                for value in content_types_list)
    return func


def allow_certain_content_types(*content_types_list):
    def _wrapper(func):
        return _do_allow_certain_content_types(func, content_types_list)
    return _wrapper


def allow_all_content_types(f):
    return _do_allow_certain_content_types(f, mimetypes.types_map.values())


def parse_image_name(image):
    image_parts = image.split(':', 1)

    image_repo = image_parts[0]
    image_tag = 'latest'

    if len(image_parts) > 1:
        image_tag = image_parts[1]

    return image_repo, image_tag


def spawn_n(func, *args, **kwargs):
    """Passthrough method for eventlet.spawn_n.

    This utility exists so that it can be stubbed for testing without
    interfering with the service spawns.

    It will also grab the context from the threadlocal store and add it to
    the store on the new thread.  This allows for continuity in logging the
    context when using this method to spawn a new thread.
    """
    _context = common_context.get_current()

    @functools.wraps(func)
    def context_wrapper(*args, **kwargs):
        # NOTE: If update_store is not called after spawn_n it won't be
        # available for the logger to pull from threadlocal storage.
        if _context is not None:
            _context.update_store()
        func(*args, **kwargs)

    eventlet.spawn_n(context_wrapper, *args, **kwargs)


def translate_exception(function):
    """Wraps a method to catch exceptions.

    If the exception is not an instance of ZunException,
    translate it into one.
    """

    @functools.wraps(function)
    def decorated_function(self, context, *args, **kwargs):
        try:
            return function(self, context, *args, **kwargs)
        except Exception as e:
            if not isinstance(e, exception.ZunException):
                LOG.exception("Unexpected error: %s", six.text_type(e))
                e = exception.ZunException("Unexpected error: %s"
                                           % six.text_type(e))
                raise e
            raise

    return decorated_function


def check_container_id(function):
    """Check container_id property of given container instance."""

    @functools.wraps(function)
    def decorated_function(*args, **kwargs):
        container = args[2]
        if getattr(container, 'container_id', None) is None:
            msg = _("Cannot operate an uncreated container.")
            raise exception.Invalid(message=msg)
        return function(*args, **kwargs)

    return decorated_function


def poll_until(retriever, condition=lambda value: value,
               sleep_time=1, time_out=None, success_msg=None,
               timeout_msg=None):
    """Retrieves object until it passes condition, then returns it.

    If time_out_limit is passed in, PollTimeOut will be raised once that
    amount of time is elapsed.
    """
    start_time = time.time()

    def poll_and_check():
        obj = retriever()
        if condition(obj):
            raise loopingcall.LoopingCallDone(retvalue=obj)
        if time_out is not None and time.time() - start_time > time_out:
            raise exception.PollTimeOut

    try:
        poller = loopingcall.FixedIntervalLoopingCall(
            f=poll_and_check).start(sleep_time, initial_delay=False)
        poller.wait()
        LOG.info(success_msg)
    except exception.PollTimeOut:
        LOG.error(timeout_msg)
        raise
    except Exception as e:
        LOG.exception("Unexpected exception occurred: %s",
                      six.text_type(e))
        raise


def get_image_pull_policy(image_pull_policy, image_tag):
    if not image_pull_policy:
        if image_tag == 'latest':
            image_pull_policy = 'always'
        else:
            image_pull_policy = 'ifnotpresent'
    return image_pull_policy


def should_pull_image(image_pull_policy, present):
    if image_pull_policy == 'never':
        return False
    if (image_pull_policy == 'always' or
            (image_pull_policy == 'ifnotpresent' and not present)):
        return True
    return False


def get_floating_cpu_set():
    """Parse floating_cpu_set config.

    :returns: a set of pcpu ids can be used by containers
    """

    if not CONF.floating_cpu_set:
        return None

    cpuset_ids = parse_floating_cpu(CONF.floating_cpu_set)
    if not cpuset_ids:
        raise exception.Invalid(_("No CPUs available after parsing %r") %
                                CONF.floating_cpu_set)
    return cpuset_ids


def parse_floating_cpu(spec):
    """Parse a CPU set specification.

    Each element in the list is either a single CPU number, a range of
    CPU numbers.

    :param spec: cpu set string eg "1-4,6"
    :returns: a set of CPU indexes

    """

    cpuset_ids = set()
    for rule in spec.split(','):
        range_part = rule.strip().split("-", 1)
        if len(range_part) > 1:
            try:
                start, end = [int(p.strip()) for p in range_part]
            except ValueError:
                raise exception.Invalid()
            if start < end:
                cpuset_ids |= set(range(start, end + 1))
            else:
                raise exception.Invalid()
        else:
            try:
                cpuset_ids.add(int(rule))
            except ValueError:
                raise exception.Invalid()

    return cpuset_ids


def list_ports(context, container, **kwargs):
    container_ports = []
    if not container.addresses:
        return container_ports
    else:
        port_list = []
        neutron_client = clients.OpenStackClients(context).neutron()
        for ports in container.addresses.values():
            port_list.extend([p['port'] for p in ports])
        port_set = set(port_list)
        for port in port_set:
            container_ports.append(neutron_client.show_port(port)['port'])
    return container_ports


def get_security_group_ids(context, security_groups, **kwargs):
    if security_groups is None:
        return None
    else:
        neutron = clients.OpenStackClients(context).neutron()
        search_opts = {'tenant_id': context.project_id}
        security_groups_list = neutron.list_security_groups(
            **search_opts).get('security_groups', [])
        security_group_ids = [item['id'] for item in security_groups_list
                              if item['name'] in security_groups]
        if len(security_group_ids) >= len(security_groups):
            return security_group_ids
        else:
            raise exception.ZunException(_(
                "Any of the security group in %s is not found ") %
                security_groups)


def check_capsule_template(tpl):
    # TODO(kevinz): add volume spec check
    kind_field = tpl.get('kind', None)
    if kind_field != 'capsule' or kind_field != 'Capsule':
        raise exception.InvalidCapsuleTemplate("kind fields need to "
                                               "be set as capsule")
    spec_field = tpl.get('spec', None)
    if spec_field is None:
        raise exception.InvalidCapsuleTemplate("No Spec found")
    if spec_field.get('containers', None) is None:
        raise exception.InvalidCapsuleTemplate("No valid containers field")
    containers_spec = spec_field.get('containers', None)
    containers_num = len(containers_spec)
    if containers_num == 0:
        raise exception.InvalidCapsuleTemplate("Capsule need to have one "
                                               "container at least")

    for i in range(0, containers_num):
        container_image = containers_spec[i].get('image', None)
        if container_image is None:
            raise exception.InvalidCapsuleTemplate("Container "
                                                   "image is needed")
    return containers_spec
