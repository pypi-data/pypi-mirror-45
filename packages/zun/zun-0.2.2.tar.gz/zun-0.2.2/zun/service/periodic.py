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

import functools

from oslo_log import log
from oslo_service import periodic_task

from zun.common import context
from zun.compute.compute_node_tracker import ComputeNodeTracker
from zun.container import driver
from zun import objects

LOG = log.getLogger(__name__)


def set_context(func):
    @functools.wraps(func)
    def handler(self, ctx):
        if ctx is None:
            ctx = context.get_admin_context(all_tenants=True)
        func(self, ctx)
    return handler


class ContainerStateSyncPeriodicJob(periodic_task.PeriodicTasks):
    def __init__(self, conf):
        self.host = conf.host
        self.driver = driver.load_container_driver(
            conf.container_driver)
        self.node_tracker = ComputeNodeTracker(self.host, self.driver)
        super(ContainerStateSyncPeriodicJob, self).__init__(conf)

    @periodic_task.periodic_task(run_immediately=True)
    @set_context
    def sync_container_state(self, ctx):
        LOG.debug('Start syncing container states.')

        containers = objects.Container.list(ctx)
        self.driver.update_containers_states(ctx, containers)

        LOG.debug('Complete syncing container states.')

    @periodic_task.periodic_task(run_immediately=True)
    @set_context
    def inventory_host(self, ctx):
        self.node_tracker.update_available_resources(ctx)


def setup(conf, tg):
    pt = ContainerStateSyncPeriodicJob(conf)
    tg.add_dynamic_timer(
        pt.run_periodic_tasks,
        periodic_interval_max=conf.periodic_interval_max,
        context=None)
