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
"""Zun test utilities."""
import mock

from oslo_config import cfg
from oslo_serialization import jsonutils as json

from zun.common import name_generator
from zun.db import api as db_api

CONF = cfg.CONF


def get_test_container(**kwargs):
    return {
        'id': kwargs.get('id', 42),
        'uuid': kwargs.get('uuid', 'ea8e2a25-2901-438d-8157-de7ffd68d051'),
        'container_id': kwargs.get('container_id', 'ddcb39a3fcec'),
        'name': kwargs.get('name', 'container1'),
        'project_id': kwargs.get('project_id', 'fake_project'),
        'user_id': kwargs.get('user_id', 'fake_user'),
        'image': kwargs.get('image', 'ubuntu'),
        'created_at': kwargs.get('created_at'),
        'updated_at': kwargs.get('updated_at'),
        'command': kwargs.get('command', 'fake_command'),
        'status': kwargs.get('status', 'Running'),
        'status_reason': kwargs.get('status_reason', 'Created Successfully'),
        'task_state': kwargs.get('task_state', 'container_creating'),
        'environment': kwargs.get('environment', {'key1': 'val1',
                                                  'key2': 'val2'}),
        'cpu': kwargs.get('cpu', 1.0),
        'memory': kwargs.get('memory', '512m'),
        'workdir': kwargs.get('workdir', '/home/ubuntu'),
        'ports': kwargs.get('ports', [80, 443]),
        'hostname': kwargs.get('hostname', 'testhost'),
        'labels': kwargs.get('labels', {'key1': 'val1', 'key2': 'val2'}),
        'meta': kwargs.get('meta', {'key1': 'val1', 'key2': 'val2'}),
        'addresses': kwargs.get('addresses', {
            'private': [
                {
                    'OS-EXT-IPS-MAC:mac_addr': 'fa:16:3e:04:da:76',
                    'port': '1234567',
                    'version': 4,
                    'addr': '10.0.0.12',
                    'OS-EXT-IPS:type': 'fixed'
                },
            ],
        }),
        'image_pull_policy': kwargs.get('image_pull_policy', 'always'),
        'host': kwargs.get('host', 'localhost'),
        'restart_policy': kwargs.get('restart_policy',
                                     {'Name': 'no', 'MaximumRetryCount': '0'}),
        'status_detail': kwargs.get('status_detail', 'up from 5 hours'),
        'interactive': kwargs.get('interactive', True),
        'image_driver': kwargs.get('image_driver', 'glance'),
        'websocket_url': 'ws://127.0.0.1:6784/4c03164962fa/attach/'
                         'ws?logs=0&stream=1&stdin=1&stdout=1&stderr=1',
        'websocket_token': '7878038e-957c-4d52-ae19-1e9561784e7b',
        'security_groups': kwargs.get('security_groups', ['default']),
        'auto_remove': kwargs.get('auto_remove', False),
    }


def create_test_container(**kwargs):
    """Create test container entry in DB and return Container DB object.

    Function to be used to create test Container objects in the database.
    :param kwargs: kwargs with overriding values for container's attributes.
    :returns: Test Container DB object.
    """
    container = get_test_container(**kwargs)
    # Let DB generate ID if it isn't specified explicitly
    if CONF.db_type == 'sql' and 'id' not in kwargs:
        del container['id']
    dbapi = db_api._get_dbdriver_instance()
    return dbapi.create_container(kwargs['context'], container)


def get_test_image(**kwargs):
    return {
        'id': kwargs.get('id', 42),
        'uuid': kwargs.get('uuid', 'ea8e2a25-2901-438d-8157-de7ffd68d051'),
        'repo': kwargs.get('repo', 'image1'),
        'tag': kwargs.get('tag', 'latest'),
        'image_id': kwargs.get('image_id', 'sha256:c54a2cc56cbb2f0400'),
        'size': kwargs.get('size', '1848'),
        'project_id': kwargs.get('project_id', 'fake_project'),
        'user_id': kwargs.get('user_id', 'fake_user'),
        'created_at': kwargs.get('created_at'),
        'updated_at': kwargs.get('updated_at'),
    }


def create_test_image(**kwargs):
    """Create test image entry in DB and return Image DB object.

    Function to be used to create test Image objects in the database.
    :param kwargs: kwargs with overriding values for image's attributes.
    :returns: Test Image DB object.
    """
    image = get_test_image(**kwargs)
    # Let DB generate ID if it isn't specified explicitly
    if 'id' not in kwargs:
        del image['id']
    if 'repo' not in kwargs:
        image['repo'] = _generate_repo_for_image()
    dbapi = db_api._get_dbdriver_instance()
    return dbapi.pull_image(kwargs['context'], image)


def _generate_repo_for_image():
    """Generate a random name like: zeta-22-image."""
    name_gen = name_generator.NameGenerator()
    name = name_gen.generate()
    return name + '-image'


def get_test_zun_service(**kwargs):
    return {
        'id': kwargs.get('id', 23),
        'uuid': kwargs.get('uuid', '2e8e2a25-2901-438d-8157-de7ffd68d066'),
        'host': kwargs.get('host', 'fakehost'),
        'binary': kwargs.get('binary', 'fake-bin'),
        'disabled': kwargs.get('disabled', False),
        'disabled_reason': kwargs.get('disabled_reason', 'fake-reason'),
        'last_seen_up': kwargs.get('last_seen_up'),
        'forced_down': kwargs.get('forced_down', False),
        'report_count': kwargs.get('report_count', 13),
        'created_at': kwargs.get('created_at'),
        'updated_at': kwargs.get('updated_at'),
    }


def create_test_zun_service(**kwargs):
    zun_service = get_test_zun_service(**kwargs)
    # Let DB generate ID if it isn't specifiled explicitly
    if CONF.db_type == 'sql' and 'id' not in kwargs:
        del zun_service['id']
    dbapi = db_api._get_dbdriver_instance()
    return dbapi.create_zun_service(zun_service)


def get_test_resource_provider(**kwargs):
    return {
        'id': kwargs.get('id', 42),
        'uuid': kwargs.get('uuid', 'e166bf0e-66db-409d-aa4d-3af94efd8bcf'),
        'name': kwargs.get('name', 'provider1'),
        'root_provider': kwargs.get('root_provider',
                                    'd3d4c98a-8c95-4d3c-8605-ea38ea036556'),
        'parent_provider': kwargs.get('parent_provider',
                                      '2c4de408-6c4f-4257-8274-f2d2192fe871'),
        'can_host': kwargs.get('can_host', 0),
        'created_at': kwargs.get('created_at'),
        'updated_at': kwargs.get('updated_at'),
    }


def create_test_resource_provider(**kwargs):
    provider = get_test_resource_provider(**kwargs)
    # Let DB generate ID if it isn't specified explicitly
    if CONF.db_type == 'sql' and 'id' not in kwargs:
        del provider['id']
    dbapi = db_api._get_dbdriver_instance()
    return dbapi.create_resource_provider(kwargs['context'], provider)


def get_test_resource_class(**kwargs):
    return {
        'id': kwargs.get('id', 42),
        'uuid': kwargs.get('uuid', '1136bf0e-66db-409d-aa4d-3af94eed8bcc'),
        'name': kwargs.get('name', 'VCPU'),
        'created_at': kwargs.get('created_at'),
        'updated_at': kwargs.get('updated_at'),
    }


def create_test_resource_class(**kwargs):
    resource = get_test_resource_class(**kwargs)
    # Let DB generate ID if it isn't specified explicitly
    if CONF.db_type == 'sql' and 'id' not in kwargs:
        del resource['id']
    dbapi = db_api._get_dbdriver_instance()
    return dbapi.create_resource_class(kwargs['context'], resource)


def get_test_inventory(**kwargs):
    return {
        'id': kwargs.get('id', 42),
        'resource_provider_id': kwargs.get('resource_provider_id', 1),
        'resource_class_id': kwargs.get('resource_class_id', 2),
        'total': kwargs.get('total', 4),
        'reserved': kwargs.get('reserved', 1),
        'min_unit': kwargs.get('min_unit', 0),
        'max_unit': kwargs.get('max_unit', 4),
        'step_size': kwargs.get('step_size', 1),
        'allocation_ratio': kwargs.get('allocation_ratio', 1.0),
        'is_nested': kwargs.get('is_nested', True),
        'blob': kwargs.get('blob', [1, 2, 5]),
        'created_at': kwargs.get('created_at'),
        'updated_at': kwargs.get('updated_at'),
    }


def create_test_inventory(**kwargs):
    inventory = get_test_inventory(**kwargs)
    # Let DB generate ID if it isn't specified explicitly
    if CONF.db_type == 'sql' and 'id' not in kwargs:
        del inventory['id']
    provider_id = inventory.pop('resource_provider_id')
    dbapi = db_api._get_dbdriver_instance()
    return dbapi.create_inventory(kwargs['context'], provider_id, inventory)


def get_test_allocation(**kwargs):
    return {
        'id': kwargs.get('id', 42),
        'resource_provider_id': kwargs.get('resource_provider_id', 1),
        'resource_class_id': kwargs.get('resource_class_id', 2),
        'consumer_id': kwargs.get('consumer_id',
                                  'cb775e13-72e2-4bfa-9646-020725e1325e'),
        'used': kwargs.get('used', 1),
        'is_nested': kwargs.get('is_nested', 0),
        'blob': kwargs.get('blob', [1, 2, 5]),
        'created_at': kwargs.get('created_at'),
        'updated_at': kwargs.get('updated_at'),
    }


def create_test_allocation(**kwargs):
    allocation = get_test_allocation(**kwargs)
    # Let DB generate ID if it isn't specified explicitly
    if CONF.db_type == 'sql' and 'id' not in kwargs:
        del allocation['id']
    dbapi = db_api._get_dbdriver_instance()
    return dbapi.create_allocation(kwargs['context'], allocation)


def get_test_numa_topology(**kwargs):
    return {
        "nodes": [
            {
                "id": 0,
                "cpuset": [1, 2],
                "pinned_cpus": []
            },
            {
                "id": 1,
                "cpuset": [3, 4],
                "pinned_cpus": [3, 4]
            }
        ]
    }


def get_test_compute_node(**kwargs):
    return {
        'uuid': kwargs.get('uuid', '24a5b17a-f2eb-4556-89db-5f4169d13982'),
        'hostname': kwargs.get('hostname', 'localhost'),
        'numa_topology': kwargs.get('numa_topology', get_test_numa_topology()),
        'mem_total': kwargs.get('mem_total', 1024),
        'mem_free': kwargs.get('mem_free', 512),
        'mem_available': kwargs.get('mem_available', 512),
        'mem_used': kwargs.get('mem_used', 512),
        'total_containers': kwargs.get('total_containers', 10),
        'running_containers': kwargs.get('running_containers', 8),
        'paused_containers': kwargs.get('paused_containers', 0),
        'stopped_containers': kwargs.get('stopped_containers', 2),
        'cpus': kwargs.get('cpus', 48),
        'cpu_used': kwargs.get('cpu_used', 6.5),
        'architecture': kwargs.get('architecture', 'x86_64'),
        'os_type': kwargs.get('os_type', 'linux'),
        'os': kwargs.get('os', 'Centos'),
        'kernel_version': kwargs.get('kernel_version',
                                     '3.10.0-123.el7.x86_64'),
        'labels': kwargs.get('labels', {"dev.type": "product"}),
        'created_at': kwargs.get('created_at'),
        'updated_at': kwargs.get('updated_at'),
    }


def create_test_compute_node(**kwargs):
    compute_host = get_test_compute_node(**kwargs)
    dbapi = db_api._get_dbdriver_instance()
    return dbapi.create_compute_node(kwargs['context'], compute_host)


class FakeEtcdMultipleResult(object):
    def __init__(self, value):
        self.children = []
        for v in value:
            res = mock.MagicMock()
            res.value = json.dump_as_bytes(v)
            self.children.append(res)


class FakeEtcdResult(object):
    def __init__(self, value):
        self.value = json.dump_as_bytes(value)
