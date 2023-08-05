# Copyright 2016 Intel.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from glanceclient import client as glanceclient
from neutronclient.v2_0 import client as neutronclient
from novaclient import client as novaclient

from zun.common import exception
from zun.common import keystone
import zun.conf


class OpenStackClients(object):
    """Convenience class to create and cache client instances."""

    def __init__(self, context):
        self.context = context
        self._keystone = None
        self._glance = None
        self._nova = None
        self._neutron = None

    def url_for(self, **kwargs):
        return self.keystone().session.get_endpoint(**kwargs)

    def zun_url(self):
        endpoint_type = self._get_client_option('zun', 'endpoint_type')
        region_name = self._get_client_option('zun', 'region_name')
        return self.url_for(service_type='container',
                            interface=endpoint_type,
                            region_name=region_name)

    @property
    def auth_url(self):
        return self.keystone().auth_url

    @property
    def auth_token(self):
        return self.context.auth_token or self.keystone().auth_token

    def keystone(self):
        if self._keystone:
            return self._keystone

        self._keystone = keystone.KeystoneClientV3(self.context)
        return self._keystone

    def _get_client_option(self, client, option):
        return getattr(getattr(zun.conf.CONF, '%s_client' % client), option)

    @exception.wrap_keystone_exception
    def glance(self):
        if self._glance:
            return self._glance

        endpoint_type = self._get_client_option('glance', 'endpoint_type')
        region_name = self._get_client_option('glance', 'region_name')
        glanceclient_version = self._get_client_option('glance', 'api_version')
        endpoint = self.url_for(service_type='image',
                                interface=endpoint_type,
                                region_name=region_name)
        args = {
            'endpoint': endpoint,
            'auth_url': self.auth_url,
            'token': self.auth_token,
            'username': None,
            'password': None,
            'cacert': self._get_client_option('glance', 'ca_file'),
            'cert': self._get_client_option('glance', 'cert_file'),
            'key': self._get_client_option('glance', 'key_file'),
            'insecure': self._get_client_option('glance', 'insecure')
        }
        self._glance = glanceclient.Client(glanceclient_version, **args)

        return self._glance

    @exception.wrap_keystone_exception
    def nova(self):
        if self._nova:
            return self._nova

        nova_api_version = self._get_client_option('nova', 'api_version')
        session = self.keystone().session
        self._nova = novaclient.Client(nova_api_version, session=session)

        return self._nova

    @exception.wrap_keystone_exception
    def neutron(self):
        if self._neutron:
            return self._neutron

        session = self.keystone().session
        endpoint_type = self._get_client_option('neutron', 'endpoint_type')
        self._neutron = neutronclient.Client(session=session,
                                             endpoint_type=endpoint_type)

        return self._neutron
