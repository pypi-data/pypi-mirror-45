# All Rights Reserved.
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

import collections
import copy

from oslo_log import log as logging

from zun.common import exception
from zun.common import utils
from zun.compute import claims
from zun import objects
from zun.objects import base as obj_base
from zun.scheduler import client as scheduler_client

LOG = logging.getLogger(__name__)
COMPUTE_RESOURCE_SEMAPHORE = "compute_resources"


class ComputeNodeTracker(object):
    def __init__(self, host, container_driver):
        self.host = host
        self.container_driver = container_driver
        self.compute_node = None
        self.tracked_containers = {}
        self.old_resources = collections.defaultdict(objects.ComputeNode)
        self.scheduler_client = scheduler_client.SchedulerClient()

    def update_available_resources(self, context):
        # Check if the compute_node is already registered
        node = self._get_compute_node(context)
        if not node:
            # If not, register it and pass the object to the driver
            numa_obj = self.container_driver.get_host_numa_topology()
            node = objects.ComputeNode(context)
            node.hostname = self.host
            node.numa_topology = numa_obj
            node.create(context)
            LOG.info('Node created for :%(host)s', {'host': self.host})
        self.container_driver.get_available_resources(node)
        self.compute_node = node
        self._update_available_resource(context)
        # NOTE(sbiswas7): Consider removing the return statement if not needed
        return node

    def _get_compute_node(self, context):
        """Returns compute node for the host"""
        try:
            return objects.ComputeNode.get_by_hostname(context, self.host)
        except exception.ComputeNodeNotFound:
            LOG.warning("No compute node record for: %(host)s",
                        {'host': self.host})

    @utils.synchronized(COMPUTE_RESOURCE_SEMAPHORE)
    def container_claim(self, context, container, hostname, limits=None):
        """Indicate resources are needed for an upcoming container build.

        This should be called before the compute node is about to perform
        an container build operation that will consume additional resources.

        :param context: security context
        :param container: container to reserve resources for.
        :type container: zun.objects.container.Container object
        :param hostname: The zun hostname selected by the scheduler
        :param limits: Dict of oversubscription limits for memory, disk,
                       and CPUs.
        :returns: A Claim ticket representing the reserved resources.  It can
                  be used to revert the resource usage if an error occurs
                  during the container build.
        """
        # No memory and cpu specified, no need to claim resource now.
        if not (container.memory or container.cpu):
            self._set_container_host(context, container)
            return claims.NopClaim()

        # We should have the compute node created here, just get it.
        self.compute_node = self._get_compute_node(context)
        if self.disabled(hostname):
            self._set_container_host(context, container)
            return claims.NopClaim()

        claim = claims.Claim(context, container, self, self.compute_node,
                             limits=limits)

        self._set_container_host(context, container)
        self._update_usage_from_container(container)
        # persist changes to the compute node:
        self._update(self.compute_node)

        return claim

    def disabled(self, hostname):
        return not self.container_driver.node_is_available(hostname)

    def _set_container_host(self, context, container):
        """Tag the container as belonging to this host.

        This should be done while the COMPUTE_RESOURCES_SEMAPHORE is held so
        the resource claim will not be lost if the audit process starts.
        """
        container.host = self.host
        container.save(context)

    def _update_usage_from_container(self, container, is_removed=False):
        """Update usage for a single container."""

        uuid = container.uuid
        is_new_container = uuid not in self.tracked_containers
        is_removed_container = not is_new_container and is_removed

        if is_new_container:
            self.tracked_containers[uuid] = \
                obj_base.obj_to_primitive(container)
            sign = 1

        if is_removed_container:
            self.tracked_containers.pop(uuid)
            sign = -1

        if is_new_container or is_removed_container:
            # TODO(Shunli): Handle pci, scheduler allocation here.

            # new container, update compute node resource usage:
            self._update_usage(self._get_usage_dict(container), sign=sign)

    def _update_usage_from_containers(self, context, containers):
        """Calculate resource usage based on container utilization.

        This is different than the conatiner daemon view as it will account
        for all containers assigned to the local compute host, even if they
        are not currently powered on.
        """
        self.tracked_containers.clear()

        cn = self.compute_node
        # set some initial values, reserve room for host
        cn.cpu_used = 0
        cn.mem_free = cn.mem_total
        cn.mem_used = 0
        cn.running_containers = 0

        for cnt in containers:
            self._update_usage_from_container(cnt)

        cn.mem_free = max(0, cn.mem_free)

    def _update_usage(self, usage, sign=1):
        mem_usage = usage['memory']
        cpus_usage = usage.get('cpu', 0)

        cn = self.compute_node
        cn.mem_used += sign * mem_usage
        cn.cpu_used += sign * cpus_usage

        # free ram may be negative, depending on policy:
        cn.mem_free = cn.mem_total - cn.mem_used

        cn.running_containers += sign * 1

        # TODO(Shunli): Calculate the numa usage here

    def _update(self, compute_node):
        if not self._resource_change(compute_node):
            return
        # Persist the stats to the Scheduler
        self.scheduler_client.update_resource(compute_node)
        # Update pci tracker here

    def _resource_change(self, compute_node):
        """Check to see if any resources have changed."""
        hostname = compute_node.hostname
        old_compute = self.old_resources[hostname]
        if not obj_base.obj_equal_prims(
                compute_node, old_compute, ['updated_at']):
            self.old_resources[hostname] = copy.deepcopy(compute_node)
            return True
        return False

    @utils.synchronized(COMPUTE_RESOURCE_SEMAPHORE)
    def _update_available_resource(self, context):

        # if we could not init the compute node the tracker will be
        # disabled and we should quit now
        if self.disabled(self.host):
            return

        # Grab all containers assigned to this node:
        containers = objects.Container.list_by_host(context, self.host)

        # Now calculate usage based on container utilization:
        self._update_usage_from_containers(context, containers)

        # No migration for docker, is there will be orphan container? Nova has.

        cn = self.compute_node

        # update the compute_node
        self._update(cn)
        LOG.debug('Compute_service record updated for %(host)s',
                  {'host': self.host})

    def _get_usage_dict(self, container, **updates):
        """Make a usage dict _update methods expect.

        Accepts an Container, and a set of updates.
        Converts the object to a dict and applies the updates.

        :param container: container as an object
        :param updates: key-value pairs to update the passed object.

        :returns: a dict with all the information from container updated
                  with updates
        """
        usage = {}
        # (Fixme): The Container.memory is string.
        memory = 0
        if container.memory:
            memory = int(container.memory[:-1])
        usage = {'memory': memory,
                 'cpu': container.cpu or 0}

        # update numa usage here

        return usage

    @utils.synchronized(COMPUTE_RESOURCE_SEMAPHORE)
    def abort_container_claim(self, container):
        """Remove usage from the given container."""
        self._update_usage_from_container(container, is_removed=True)

        self._update(self.compute_node)

    @utils.synchronized(COMPUTE_RESOURCE_SEMAPHORE)
    def remove_usage_from_container(self, context, container,
                                    is_removed=True):
        """Just a wrapper of the private function to hold lock."""

        # We need to get the latest compute node info
        self.compute_node = self._get_compute_node(context)
        self._update_usage_from_container(container, is_removed)
        self._update(self.compute_node)
