# Copyright 2016 - Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg
from oslo_log import log
from oslo_utils import importutils as utils

from vitrage import keystone_client

LOG = log.getLogger(__name__)

OPTS = [
    cfg.StrOpt('aodh_version', default='2', help='Aodh version'),
    cfg.StrOpt('nova_version', default='2.11', help='Nova version'),
    cfg.StrOpt('cinder_version', default='2', help='Cinder version'),
    cfg.StrOpt('glance_version', default='2', help='Glance version'),
    cfg.StrOpt('heat_version', default='1', help='Heat version'),
    cfg.StrOpt('mistral_version', default='2', help='Mistral version'),
]

_client_modules = {
    'ceilometer': 'ceilometerclient.client',
    'nova': 'novaclient.client',
    'cinder': 'cinderclient.client',
    'glance': 'glanceclient.client',
    'neutron': 'neutronclient.v2_0.client',
    'heat': 'heatclient.v1.client',
    'mistral': 'mistralclient.api.v2.client',
}


def driver_module(driver):
    mod_name = _client_modules[driver]
    module = utils.import_module(mod_name)
    return module


def ceilometer_client(conf):
    """Get an instance of ceilometer client"""
    auth_config = conf.service_credentials
    try:
        cm_client = driver_module('ceilometer')
        client = cm_client.get_client(
            version=conf.aodh_version,
            session=keystone_client.get_session(conf),
            region_name=auth_config.region_name,
            interface=auth_config.interface,
        )
        LOG.info('Ceilometer client created')
        return client
    except Exception as e:
        LOG.exception('Create Ceilometer client - Got Exception: %s', e)


def nova_client(conf):
    """Get an instance of nova client"""
    auth_config = conf.service_credentials
    try:
        n_client = driver_module('nova')
        client = n_client.Client(
            version=conf.nova_version,
            session=keystone_client.get_session(conf),
            region_name=auth_config.region_name,
            endpoint_type='publicURL',
        )
        LOG.info('Nova client created')
        return client
    except Exception as e:
        LOG.exception('Create Nova client - Got Exception: %s', e)


def cinder_client(conf):
    """Get an instance of cinder client"""
    auth_config = conf.service_credentials
    try:
        cin_client = driver_module('cinder')
        client = cin_client.Client(
            version=conf.cinder_version,
            session=keystone_client.get_session(conf),
            region_name=auth_config.region_name,
            interface=auth_config.interface,
        )
        LOG.info('Cinder client created')
        return client
    except Exception as e:
        LOG.exception('Create Cinder client - Got Exception: %s', e)


def glance_client(conf):
    """Get an instance of glance client"""
    auth_config = conf.service_credentials
    try:
        glan_client = driver_module('glance')
        client = glan_client.Client(
            version=conf.glance_version,
            session=keystone_client.get_session(conf),
            region_name=auth_config.region_name,
            interface=auth_config.interface,
        )
        LOG.info('Glance client created')
        return client
    except Exception as e:
        LOG.exception('Create Glance client - Got Exception: %s', e)


def neutron_client(conf):
    """Get an instance of neutron client"""
    auth_config = conf.service_credentials
    try:
        ne_client = driver_module('neutron')
        client = ne_client.Client(
            session=keystone_client.get_session(conf),
            region_name=auth_config.region_name,
            interface=auth_config.interface,
        )
        LOG.info('Neutron client created')
        return client
    except Exception as e:
        LOG.exception('Create Neutron client - Got Exception: %s', e)


def heat_client(conf):
    """Get an instance of heat client"""
    # auth_config = conf.service_credentials
    try:
        session = keystone_client.get_session(conf)
        endpoint = session.get_endpoint(service_type='orchestration',
                                        interface='publicURL')
        he_client = driver_module('heat')
        client = he_client.Client(session=session, endpoint=endpoint)
        LOG.info('Heat client created')
        return client
    except Exception as e:
        LOG.exception('Create Heat client - Got Exception: %s', e)


def mistral_client(conf):
    """Get an instance of Mistral client"""
    try:
        session = keystone_client.get_session(conf)
        endpoint = session.get_endpoint(service_type='workflowv2',
                                        endpoint_type='internalURL')
        args = {
            'mistral_url': endpoint,
            'session': session
        }
        client = driver_module('mistral').Client(**args)
        LOG.info('Mistral client created')
        return client
    except Exception as e:
        LOG.exception('Create Mistral client - Got Exception: %s', e)
