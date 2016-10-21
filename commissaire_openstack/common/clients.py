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
from oslo_config import cfg
from oslo_log import log as logging

from commissaire_openstack.common import exception
from commissaire_openstack.common.i18n import _
from commissaire_openstack.common import keystone

common_security_opts = [
    cfg.StrOpt('ca_file',
               help=_('Optional CA cert file to use in SSL connections.')),
    cfg.StrOpt('cert_file',
               help=_('Optional PEM-formatted certificate chain file.')),
    cfg.StrOpt('key_file',
               help=_('Optional PEM-formatted file that contains the '
                      'private key.')),
    cfg.BoolOpt('insecure',
                default=False,
                help=_("If set, then the server's certificate will not "
                       "be verified."))]

commissaire_openstack_client_opts = [
    cfg.StrOpt('region_name',
               help=_('Region in Identity service catalog to use for '
                      'communication with the OpenStack service.')),
    cfg.StrOpt('endpoint_type',
               default='publicURL',
               help=_(
                   'Type of endpoint in Identity service catalog to use '
                   'for communication with the OpenStack service.'))]


glance_client_opts = [
    cfg.StrOpt('region_name',
               help=_('Region in Identity service catalog to use for '
                      'communication with the OpenStack service.')),
    cfg.StrOpt('endpoint_type',
               default='publicURL',
               help=_(
                   'Type of endpoint in Identity service catalog to use '
                   'for communication with the OpenStack service.')),
    cfg.StrOpt('api_version',
               default='2',
               help=_('Version of Glance API to use in glanceclient.'))]

cfg.CONF.register_opts(commissaire_openstack_client_opts, group='commissaire_openstack_client')
cfg.CONF.register_opts(glance_client_opts, group='glance_client')

cfg.CONF.register_opts(common_security_opts, group='glance_client')

LOG = logging.getLogger(__name__)


class OpenStackClients(object):
    """Convenience class to create and cache client instances."""

    def __init__(self, context):
        self.context = context
        self._keystone = None
        self._glance = None

    def url_for(self, **kwargs):
        return self.keystone().session.get_endpoint(**kwargs)

    def commissaire_openstack_url(self):
        endpoint_type = self._get_client_option('commissaire_openstack', 'endpoint_type')
        region_name = self._get_client_option('commissaire_openstack', 'region_name')
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
        return getattr(getattr(cfg.CONF, '%s_client' % client), option)

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
