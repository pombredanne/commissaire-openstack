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

from commissaire_openstack.common.rpc_service import CONF
from commissaire_openstack import objects
from commissaire_openstack.servicegroup import commissaire_openstack_service_periodic as periodic
from commissaire_openstack.tests import base


class Commissaire_OpenstackServicePeriodicTestCase(base.BaseTestCase):
    def setUp(self):
        super(Commissaire_OpenstackServicePeriodicTestCase, self).setUp()
        mock_commissaire_openstack_service_refresh = mock.Mock()

        class FakeSrv(object):
            report_state_up = mock_commissaire_openstack_service_refresh

        self.fake_srv = FakeSrv()
        self.fake_srv_refresh = mock_commissaire_openstack_service_refresh

    @mock.patch.object(objects.Commissaire_OpenstackService, 'get_by_host_and_binary')
    @mock.patch.object(objects.Commissaire_OpenstackService, 'create')
    @mock.patch.object(objects.Commissaire_OpenstackService, 'report_state_up')
    def test_update_commissaire_openstack_service_firsttime(self,
                                          mock_srv_refresh,
                                          mock_srv_create,
                                          mock_srv_get
                                          ):
        p_task = periodic.Commissaire_OpenstackServicePeriodicTasks(CONF,
                                                  'fake-conductor')
        mock_srv_get.return_value = None

        p_task.update_commissaire_openstack_service(None)

        mock_srv_get.assert_called_once_with(mock.ANY, p_task.host,
                                             p_task.binary)
        mock_srv_create.assert_called_once_with()
        mock_srv_refresh.assert_called_once_with()

    @mock.patch.object(objects.Commissaire_OpenstackService, 'get_by_host_and_binary')
    @mock.patch.object(objects.Commissaire_OpenstackService, 'create')
    def test_update_commissaire_openstack_service_on_restart(self,
                                           mock_srv_create,
                                           mock_srv_get):
        p_task = periodic.Commissaire_OpenstackServicePeriodicTasks(CONF,
                                                  'fake-conductor')
        mock_srv_get.return_value = self.fake_srv

        p_task.update_commissaire_openstack_service(None)

        mock_srv_get.assert_called_once_with(mock.ANY, p_task.host,
                                             p_task.binary)
        self.fake_srv_refresh.assert_called_once_with()

    def test_update_commissaire_openstack_service_regular(self):
        p_task = periodic.Commissaire_OpenstackServicePeriodicTasks(CONF,
                                                  'fake-conductor')
        p_task.commissaire_openstack_service_ref = self.fake_srv

        p_task.update_commissaire_openstack_service(None)

        self.fake_srv_refresh.assert_called_once_with()
