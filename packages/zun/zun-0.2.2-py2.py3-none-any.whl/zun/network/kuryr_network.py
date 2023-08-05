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

import ipaddress
import six

from neutronclient.common import exceptions
from oslo_log import log as logging
from oslo_utils import excutils

from zun.common import exception
from zun.common.i18n import _
import zun.conf
from zun.network import network
from zun.network import neutron


CONF = zun.conf.CONF

LOG = logging.getLogger(__name__)


class KuryrNetwork(network.Network):
    def init(self, context, docker_api):
        self.docker = docker_api
        self.neutron_api = neutron.NeutronAPI(context)
        self.context = context

    def create_network(self, name, neutron_net_id):
        """Create a docker network with Kuryr driver.

        The docker network to be created will be based on the specified
        neutron net. It is assumed that the neutron net will have one
        or two subnets. If there are two subnets, it must be a ipv4
        subnet and a ipv6 subnet and containers created from this network
        will have both ipv4 and ipv6 addresses.

        What this method does is finding the subnets under the specified
        neutron net, retrieving the cidr, gateway, subnetpool of each
        subnet, and compile the list of parameters for docker.create_network.
        """
        # find a v4 and/or v6 subnet of the network
        subnets = self.neutron_api.list_subnets(network_id=neutron_net_id)
        subnets = subnets.get('subnets', [])
        v4_subnet = self._get_subnet(subnets, ip_version=4)
        v6_subnet = self._get_subnet(subnets, ip_version=6)
        if not v4_subnet and not v6_subnet:
            raise exception.ZunException(_(
                "The Neutron network %s has no subnet") % neutron_net_id)

        ipam_options = {
            "Driver": CONF.network.driver_name,
            "Options": {},
            "Config": []
        }
        if v4_subnet:
            ipam_options["Options"]['neutron.pool.uuid'] = (
                v4_subnet.get('subnetpool_id'))
            ipam_options["Config"].append({
                "Subnet": v4_subnet['cidr'],
                "Gateway": v4_subnet['gateway_ip']
            })
        if v6_subnet:
            ipam_options["Options"]['neutron.pool.v6.uuid'] = (
                v6_subnet.get('subnetpool_id'))
            ipam_options["Config"].append({
                "Subnet": v6_subnet['cidr'],
                "Gateway": v6_subnet['gateway_ip']
            })

        options = {
            'neutron.net.uuid': neutron_net_id
        }
        if v4_subnet:
            options['neutron.pool.uuid'] = v4_subnet.get('subnetpool_id')
        if v6_subnet:
            options['neutron.pool.v6.uuid'] = v6_subnet.get('subnetpool_id')
        LOG.debug("Calling docker.create_network to create network %s, "
                  "ipam_options %s, options %s", name, ipam_options, options)
        docker_network = self.docker.create_network(
            name=name,
            driver=CONF.network.driver_name,
            enable_ipv6=True if v6_subnet else False,
            options=options,
            ipam=ipam_options)

        return docker_network

    def _get_subnet(self, subnets, ip_version):
        subnets = [s for s in subnets if s['ip_version'] == ip_version]
        if len(subnets) == 0:
            return None
        elif len(subnets) == 1:
            return subnets[0]
        else:
            raise exception.ZunException(_(
                "Multiple Neutron subnets exist with ip version %s") %
                ip_version)

    def remove_network(self, network_name):
        self.docker.remove_network(network_name)

    def inspect_network(self, network_name):
        return self.docker.inspect_network(network_name)

    def list_networks(self, **kwargs):
        return self.docker.networks(**kwargs)

    def connect_container_to_network(self, container, network_name,
                                     requested_network, security_groups=None):
        """Connect container to the network

        This method will create a neutron port, retrieve the ip address(es)
        of the port, and pass them to docker.connect_container_to_network.
        """
        container_id = container.get_sandbox_id()
        if not container_id:
            container_id = container.container_id

        if requested_network.get('port'):
            neutron_port_id = requested_network.get('port')
            neutron_port = self.neutron_api.get_neutron_port(neutron_port_id)
            # NOTE(hongbin): If existing port is specified, security_group_ids
            # is ignored because existing port already has security groups.
            # We might revisit this behaviour later. Alternatively, we could
            # either throw an exception or overwrite the port's security
            # groups.
        else:
            network = self.inspect_network(network_name)
            neutron_net_id = network['Options']['neutron.net.uuid']
            port_dict = {
                'network_id': neutron_net_id,
                'tenant_id': self.context.project_id,
            }
            ip_addr = requested_network.get("v4-fixed-ip") or requested_network.\
                get("v6-fixed-ip")
            if ip_addr:
                port_dict['fixed_ips'] = [{'ip_address': ip_addr}]
            if security_groups is not None:
                port_dict['security_groups'] = security_groups
            neutron_port = self.neutron_api.create_port({'port': port_dict})
            neutron_port = neutron_port['port']

        ipv4_address = None
        ipv6_address = None
        addresses = []
        for fixed_ip in neutron_port['fixed_ips']:
            ip_address = fixed_ip['ip_address']
            ip = ipaddress.ip_address(six.text_type(ip_address))
            if ip.version == 4:
                ipv4_address = ip_address
                addresses.append({
                    'addr': ip_address,
                    'version': 4,
                    'port': neutron_port['id']
                })
            else:
                ipv6_address = ip_address
                addresses.append({
                    'addr': ip_address,
                    'version': 6,
                    'port': neutron_port['id']
                })

        kwargs = {}
        if ipv4_address:
            kwargs['ipv4_address'] = ipv4_address
        if ipv6_address:
            kwargs['ipv6_address'] = ipv6_address
        self.docker.connect_container_to_network(
            container_id, network_name, **kwargs)
        return addresses

    def disconnect_container_from_network(self, container, network_name,
                                          neutron_network_id=None):
        container_id = container.get_sandbox_id()
        if not container_id:
            container_id = container.container_id

        neutron_ports = set()
        if container.addresses and neutron_network_id:
            addrs_list = container.addresses.get(neutron_network_id, [])
            for addr in addrs_list:
                port_id = addr['port']
                neutron_ports.add(port_id)

        try:
            self.docker.disconnect_container_from_network(container_id,
                                                          network_name)
        finally:
            for port_id in neutron_ports:
                try:
                    self.neutron_api.delete_port(port_id)
                except exceptions.PortNotFoundClient:
                    LOG.warning('Maybe your libnetwork distribution do not '
                                'have patch https://review.openstack.org/#/c/'
                                '441024/ or neutron tag extension does not '
                                'supported or not enabled.')

    def add_security_groups_to_ports(self, container, security_group_ids):
        container_id = container.get_sandbox_id()
        if not container_id:
            container_id = container.container_id

        port_ids = set()
        for addrs_list in container.addresses.values():
            for addr in addrs_list:
                port_id = addr['port']
                port_ids.add(port_id)

        search_opts = {'tenant_id': self.context.project_id}
        neutron_ports = self.neutron_api.list_ports(
            **search_opts).get('ports', [])
        neutron_ports = [p for p in neutron_ports if p['id'] in port_ids]
        for port in neutron_ports:
            if 'security_groups' not in port:
                port['security_groups'] = []
            port['security_groups'].extend(security_group_ids)
            updated_port = {'security_groups': port['security_groups']}
            try:
                LOG.info("Adding security group %(security_group_ids)s "
                         "to port %(port_id)s",
                         {'security_group_ids': security_group_ids,
                          'port_id': port['id']})
                self.neutron_api.update_port(port['id'],
                                             {'port': updated_port})
            except Exception:
                with excutils.save_and_reraise_exception():
                    LOG.exception("Neutron Error:")
