# Copyright 2016 - Alcatel-Lucent
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

import abc
import six

from oslo_log import log

from vitrage.common.constants import DatasourceAction
from vitrage.common.constants import DatasourceProperties as DSProps
from vitrage.common.constants import GraphAction
from vitrage.utils import datetime as datetime_utils

LOG = log.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class DriverBase(object):

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_all(self, datasource_action):
        pass

    def callback_on_fault(self, exception):
        pass

    @staticmethod
    def _get_end_message(entity_type):
        end_message = {
            DSProps.ENTITY_TYPE: entity_type,
            DSProps.DATASOURCE_ACTION: DatasourceAction.INIT_SNAPSHOT,
            DSProps.EVENT_TYPE: GraphAction.END_MESSAGE
        }
        return end_message

    def get_changes(self, datasource_action):
        pass

    @classmethod
    def make_pickleable(cls, entities, entity_type, datasource_action, *args):
        pickleable_entities = []

        for entity in entities:
            for field in args:
                entity.pop(field, None)

            cls._add_entity_type(entity, entity_type)
            cls._add_datasource_action(entity, datasource_action)
            cls._add_sampling_time(entity)
            pickleable_entities.append(entity)

        if datasource_action == DatasourceAction.INIT_SNAPSHOT:
            pickleable_entities.append(cls._get_end_message(entity_type))

        return pickleable_entities

    @staticmethod
    def _add_entity_type(entity, entity_type):
        if DSProps.ENTITY_TYPE not in entity:
            entity[DSProps.ENTITY_TYPE] = entity_type

    @staticmethod
    def _add_sampling_time(entity):
        entity[DSProps.SAMPLE_DATE] = str(datetime_utils.utcnow())

    @staticmethod
    def _add_datasource_action(entity, datasource_action):
        entity[DSProps.DATASOURCE_ACTION] = datasource_action

    def enrich_event(self, event, event_type):
        """Return the given event with extra fields

        We add extra data, which the transformer uses later on.
        For example, we can add a timestamp and change the message's structure
        :param event: the event received by oslo
        :param event_type: the event type of the event
        :return: the enriched event
        """

        pass

    @staticmethod
    @abc.abstractmethod
    def get_event_types():
        """Return a list of all event types relevant to this datasource

        Example:
        return ['compute.instance.update',
                'compute.instance.resume']

        It also supports prefixes- the event types which start
        with this prefix will be processed by this driver:
        Example:
        return ['compute.instance']



        :return: a list of event types
        :rtype: list of str
        """

        return []

    @staticmethod
    def properties_to_filter_out():
        """Return a list of properties to be removed from the event"""
        return []
