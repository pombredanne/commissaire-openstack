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

from oslo_versionedobjects import fields

from commissaire_openstack.objects import base


@base.Commissaire_OpenstackObjectRegistry.register
class Commissaire_OpenstackService(base.Commissaire_OpenstackPersistentObject, base.Commissaire_OpenstackObject,
                 base.Commissaire_OpenstackObjectDictCompat):
    # Version 1.0: Initial version
    VERSION = '1.0'

    fields = {
        'id': fields.IntegerField(),
        'host': fields.StringField(nullable=True),
        'binary': fields.StringField(nullable=True),
        'disabled': fields.BooleanField(),
        'disabled_reason': fields.StringField(nullable=True),
        'last_seen_up': fields.DateTimeField(nullable=True),
        'forced_down': fields.BooleanField(),
        'report_count': fields.IntegerField(),
    }

    @staticmethod
    def _from_db_object(commissaire_openstack_service, db_commissaire_openstack_service):
        """Converts a database entity to a formal object."""
        for field in commissaire_openstack_service.fields:
            commissaire_openstack_service[field] = db_commissaire_openstack_service[field]

        commissaire_openstack_service.obj_reset_changes()
        return commissaire_openstack_service

    @staticmethod
    def _from_db_object_list(db_objects, cls, context):
        """Converts a list of database entities to a list of formal objects."""
        return [Commissaire_OpenstackService._from_db_object(cls(context), obj)
                for obj in db_objects]

    @base.remotable_classmethod
    def get_by_host_and_binary(cls, context, host, binary):
        """Find a commissaire_openstack_service based on its hostname and binary.

        :param host: The host on which the binary is running.
        :param binary: The name of the binary.
        :param context: Security context.
        :returns: a :class:`Commissaire_OpenstackService` object.
        """
        db_commissaire_openstack_service = dbapi.Connection.get_commissaire_openstack_service_by_host_and_binary(
            context, host, binary)
        if db_commissaire_openstack_service is None:
            return None
        commissaire_openstack_service = None
        return commissaire_openstack_service

    @base.remotable_classmethod
    def list(cls, context, limit=None, marker=None,
             sort_key=None, sort_dir=None):
        """Return a list of Commissaire_OpenstackService objects.

        :param context: Security context.
        :param limit: maximum number of resources to return in a single result.
        :param marker: pagination marker for large data sets.
        :param sort_key: column to sort results by.
        :param sort_dir: direction to sort. "asc" or "desc".
        :returns: a list of :class:`Commissaire_OpenstackService` object.

        """
        db_commissaire_openstack_services = dbapi.Connection.get_commissaire_openstack_service_list(
            context, limit=limit, marker=marker, sort_key=sort_key,
            sort_dir=sort_dir)
        return Commissaire_OpenstackService._from_db_object_list(db_commissaire_openstack_services, cls,
                                               context)

    @base.remotable
    def create(self, context=None):
        """Create a Commissaire_OpenstackService record in the DB.

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: Commissaire_OpenstackService(context)
        """
        values = self.obj_get_changes()
        db_commissaire_openstack_service = dbapi.Connection.create_commissaire_openstack_service(values)
        self._from_db_object(self, db_commissaire_openstack_service)

    @base.remotable
    def destroy(self, context=None):
        """Delete the Commissaire_OpenstackService from the DB.

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: Commissaire_OpenstackService(context)
        """
        dbapi.Connection.destroy_commissaire_openstack_service(self.id)
        self.obj_reset_changes()

    @base.remotable
    def save(self, context=None):
        """Save updates to this Commissaire_OpenstackService.

        Updates will be made column by column based on the result
        of self.what_changed().

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: Commissaire_OpenstackService(context)
        """
        updates = self.obj_get_changes()
        dbapi.Connection.update_commissaire_openstack_service(self.id, updates)
        self.obj_reset_changes()

    @base.remotable
    def report_state_up(self, context=None):
        """Touching the commissaire_openstack_service record to show aliveness.

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: Commissaire_OpenstackService(context)
        """
        self.report_count += 1
        self.save()
