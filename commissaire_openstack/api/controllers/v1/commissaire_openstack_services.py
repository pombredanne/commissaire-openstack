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

import pecan

from commissaire_openstack.api.controllers import base
from commissaire_openstack.api.controllers import types
from commissaire_openstack.api.controllers.v1 import collection
from commissaire_openstack.common import exception
from commissaire_openstack import objects


class Commissaire_OpenstackService(base.APIBase):

    fields = {
        'host': {
            'validate': types.String.validate,
            'validate_args': {
                'min_length': 1,
                'max_length': 255,
            },
        },
        'state': {
            'validate': types.String.validate,
            'validate_args': {
                'min_length': 1,
                'max_length': 255,
            },
        },
        'id': {
            'validate': types.Integer.validate,
            'validate_args': {
                'minimum': 1,
            },
        }
    }

    def __init__(self, state, **kwargs):
        super(Commissaire_OpenstackService, self).__init__(**kwargs)
        setattr(self, 'state', state)


class Commissaire_OpenstackServiceCollection(collection.Collection):

    fields = {
        'services': {
            'validate': types.List(types.Custom(Commissaire_OpenstackService)).validate,
        },
    }

    def __init__(self, **kwargs):
        super(Commissaire_OpenstackServiceCollection, self).__init__()
        self._type = 'services'

    @staticmethod
    def convert_db_rec_list_to_collection(servicegroup_api,
                                          rpc_hsvcs, **kwargs):
        collection = Commissaire_OpenstackServiceCollection()
        collection.services = []
        for p in rpc_hsvcs:
            alive = servicegroup_api.service_is_up(p)
            state = 'up' if alive else 'down'
            hsvc = Commissaire_OpenstackService(state, **p.as_dict())
            collection.services.append(hsvc)
        next = collection.get_next(limit=None, url=None, **kwargs)
        if next is not None:
            collection.next = next
        return collection


class Commissaire_OpenstackServiceController(object):
    """REST controller for commissaire_openstack-services."""

    def __init__(self, **kwargs):
        super(Commissaire_OpenstackServiceController, self).__init__()

    # TODO(hongbin): uncomment this once policy is ported
    # @policy.enforce_wsgi("commissaire_openstack-service", "get_all")
    @pecan.expose(generic=True, template='json')
    @exception.wrap_pecan_controller_exception
    def index(self, **kwargs):
        """Retrieve a list of commissaire_openstack-services.

        """
        hsvcs = objects.Commissaire_OpenstackService.list(pecan.request.context,
                                        limit=None,
                                        marker=None,
                                        sort_key='id',
                                        sort_dir='asc')
        return Commissaire_OpenstackServiceCollection.convert_db_rec_list_to_collection(
            self.servicegroup_api, hsvcs)
