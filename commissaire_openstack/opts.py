# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools

import commissaire_openstack.api.app
import commissaire_openstack.common.keystone
import commissaire_openstack.common.rpc_service
import commissaire_openstack.common.service
import commissaire_openstack.compute.config


def list_opts():
    return [
        ('DEFAULT',
         itertools.chain(
             commissaire_openstack.common.rpc_service.periodic_opts,
             commissaire_openstack.common.service.service_opts,
         )),
        ('api', commissaire_openstack.api.app.API_SERVICE_OPTS),
        ('compute', commissaire_openstack.compute.config.SERVICE_OPTS),
        ('keystone_auth', commissaire_openstack.common.keystone.keystone_auth_opts),
    ]
