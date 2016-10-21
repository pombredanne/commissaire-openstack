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

class TaskState(fields.Enum):
    ALL = (
        IMAGE_PULLING, CONTAINER_CREATING,
    ) = (
        'image_pulling', 'container_creating',
    )

    def __init__(self):
        super(TaskState, self).__init__(
            valid_values=TaskState.ALL)


class TaskStateField(fields.BaseEnumField):
    AUTO_TYPE = TaskState()


class ListOfIntegersField(fields.AutoTypedField):
    AUTO_TYPE = fields.List(fields.Integer())
