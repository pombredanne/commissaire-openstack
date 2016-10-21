# Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from commissaire_openstack.api.controllers.v1 import commissaire_openstack_services as zservice
from commissaire_openstack.tests import base
from commissaire_openstack.tests.unit.api import utils as apiutils


class TestCommissaire_OpenstackServiceObject(base.BaseTestCase):

    def setUp(self):
        super(TestCommissaire_OpenstackServiceObject, self).setUp()
        self.rpc_dict = apiutils.zservice_get_data()

    def test_msvc_obj_fields_filtering(self):
        """Test that it does filtering fields """
        self.rpc_dict['fake-key'] = 'fake-value'
        msvco = zservice.Commissaire_OpenstackService("up", **self.rpc_dict)
        self.assertNotIn('fake-key', msvco.fields)
