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

import mock

from glanceclient import client as glanceclient

from oslo_config import cfg

from commissaire_openstack.common import clients
from commissaire_openstack.common import exception
from commissaire_openstack.tests import base


class ClientsTest(base.BaseTestCase):

    def setUp(self):
        super(ClientsTest, self).setUp()

        cfg.CONF.set_override('auth_uri', 'http://server.test:5000/v2.0',
                              group='keystone_authtoken')
        cfg.CONF.import_opt('api_version', 'commissaire_openstack.common.clients',
                            group='glance_client')

    @mock.patch.object(clients.OpenStackClients, 'keystone')
    def test_url_for(self, mock_keystone):
        obj = clients.OpenStackClients(None)
        obj.url_for(service_type='fake_service', interface='fake_endpoint')

        mock_endpoint = mock_keystone.return_value.session.get_endpoint
        mock_endpoint.assert_called_once_with(service_type='fake_service',
                                              interface='fake_endpoint')

    @mock.patch.object(clients.OpenStackClients, 'keystone')
    def test_commissaire_openstack_url(self, mock_keystone):
        fake_region = 'fake_region'
        fake_endpoint = 'fake_endpoint'
        cfg.CONF.set_override('region_name', fake_region,
                              group='commissaire_openstack_client')
        cfg.CONF.set_override('endpoint_type', fake_endpoint,
                              group='commissaire_openstack_client')
        obj = clients.OpenStackClients(None)
        obj.commissaire_openstack_url()

        mock_endpoint = mock_keystone.return_value.session.get_endpoint
        mock_endpoint.assert_called_once_with(region_name=fake_region,
                                              service_type='node-enrollment',
                                              interface=fake_endpoint)
