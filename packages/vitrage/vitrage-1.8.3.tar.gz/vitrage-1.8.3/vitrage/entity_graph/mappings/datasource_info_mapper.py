# Copyright 2016 - Nokia
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

import os

from oslo_log import log

from vitrage.common.constants import EntityCategory
from vitrage.common.constants import VertexProperties as VProps
from vitrage.entity_graph.mappings.alarm_handler import AlarmHandler
from vitrage.entity_graph.mappings.resource_handler import \
    ResourceHandler
from vitrage.utils import file as file_utils

LOG = log.getLogger(__name__)


DEFAULT_INFO_MAPPER = 'default'


class DatasourceInfoMapper(object):
    OPERATIONAL_VALUES = 'operational_values'
    PRIORITY_VALUES = 'priority_values'
    UNDEFINED_DATASOURCE = 'undefined datasource'

    def __init__(self, conf):
        self.conf = conf
        self.category_normalizer = self._init_category_normalizer()
        self.datasources_state_confs = self._load_state_configurations()

    def vitrage_operational_state(self, datasource_name, state):
        return self._get_state_data(datasource_name,
                                    state,
                                    self.OPERATIONAL_VALUES)

    def state_priority(self, datasource_name, state):
        return self._get_state_data(datasource_name,
                                    state,
                                    self.PRIORITY_VALUES)

    def vitrage_aggregated_state(self, new_vertex, graph_vertex):
        datasource_name = new_vertex[VProps.VITRAGE_TYPE] if \
            VProps.VITRAGE_TYPE in new_vertex.properties else \
            graph_vertex[VProps.VITRAGE_TYPE]

        vitrage_category = new_vertex[VProps.VITRAGE_CATEGORY] if \
            VProps.VITRAGE_CATEGORY in new_vertex.properties else \
            graph_vertex[VProps.VITRAGE_CATEGORY]

        if datasource_name in self.datasources_state_confs or \
                datasource_name not in self.conf.datasources.types:
            value_properties = \
                self.category_normalizer[vitrage_category].value_properties()
            vitrage_operational_state, vitrage_aggregated_state, state_priority = \
                self._find_operational_state_and_priority(new_vertex,
                                                          graph_vertex,
                                                          value_properties[0],
                                                          datasource_name)
            value_properties.pop(0)

            for property_ in value_properties:
                t_operational_state, t_aggregated_state, t_state_priority = \
                    self._find_operational_state_and_priority(new_vertex,
                                                              graph_vertex,
                                                              property_,
                                                              datasource_name)
                if t_state_priority > state_priority:
                    vitrage_operational_state = t_operational_state
                    vitrage_aggregated_state = t_aggregated_state
                    state_priority = t_state_priority

            self.category_normalizer[vitrage_category].set_aggregated_value(
                new_vertex, vitrage_aggregated_state)
            self.category_normalizer[vitrage_category].set_operational_value(
                new_vertex, vitrage_operational_state)
        else:
            self.category_normalizer[vitrage_category].set_aggregated_value(
                new_vertex, self.UNDEFINED_DATASOURCE)
            self.category_normalizer[vitrage_category].set_operational_value(
                new_vertex, self.UNDEFINED_DATASOURCE)

    def get_datasource_priorities(self, datasource_name=None):
        if datasource_name:
            datasource_info = self.datasources_state_confs[datasource_name]
            return datasource_info[self.PRIORITY_VALUES]
        else:
            priorities_dict = \
                {key: self.datasources_state_confs[key][self.PRIORITY_VALUES]
                 for key in self.datasources_state_confs.keys()}
            return priorities_dict

    @staticmethod
    def _init_category_normalizer():
        return {
            EntityCategory.RESOURCE: ResourceHandler(),
            EntityCategory.ALARM: AlarmHandler()
        }

    def _load_state_configurations(self):
        valid_datasources_conf = {}
        erroneous_datasources_conf = []

        files = file_utils.list_files(
            self.conf.entity_graph.datasources_values_dir, '.yaml')

        for file_name in files:
            try:
                full_path = self.conf.entity_graph.datasources_values_dir \
                    + '/' + file_name
                operational_values, priority_values = \
                    self._retrieve_states_and_priorities_from_file(full_path)
                valid_datasources_conf[os.path.splitext(file_name)[0]] = {
                    self.OPERATIONAL_VALUES: operational_values,
                    self.PRIORITY_VALUES: priority_values
                }
            except Exception as e:
                LOG.exception("Exception: %s", e)
                datasource = os.path.splitext(file_name)[0]
                LOG.error('erroneous data sources is %s',
                          erroneous_datasources_conf.append(datasource))

        self._check_state_confs_exists(
            [key for key in valid_datasources_conf.keys()],
            erroneous_datasources_conf)

        return valid_datasources_conf

    def _retrieve_states_and_priorities_from_file(self, full_path):
        states = {}
        priorities = {}
        config = file_utils.load_yaml_file(full_path, with_exception=True)
        vitrage_category = config['category']

        for item in config['values']:
            aggregated_values = item['aggregated values']
            priority_value = int(aggregated_values['priority'])

            # original to operational value
            for original_state in aggregated_values['original values']:
                original_value = original_state['name']
                operational_value = original_state['operational_value']
                states[original_value.upper()] = operational_value
                priorities[original_value.upper()] = priority_value

        self._check_validity(vitrage_category, states, priorities, full_path)

        self._add_default_states(states, priorities, vitrage_category)

        return states, priorities

    def _add_default_states(self, states, priorities, category):
        default_values = self.category_normalizer[category].default_values()
        for original_val, operational_val, priority_val in default_values:
            states[original_val] = operational_val
            priorities[original_val] = priority_val

    def _check_validity(self, category, states, priorities, full_path):
        # check that all the operational values exists
        state_class_instance = \
            self.category_normalizer[category].get_value_class_instance()
        operational_values = DatasourceInfoMapper.\
            _get_all_local_variables_of_class(state_class_instance)
        for operational_value in states.values():
            if operational_value not in operational_values:
                raise ValueError('operational value %s for %s is not in %s',
                                 operational_value, full_path,
                                 state_class_instance.__class__.__name__)

    def _get_state_data(self, datasource_name, state, data_type):
        try:
            upper_state = state if not state else state.upper()

            if datasource_name in self.datasources_state_confs:
                values_conf = self.datasources_state_confs[
                    datasource_name][data_type]

                return values_conf[upper_state] if upper_state in values_conf \
                    else values_conf[None]
            else:
                values_conf = self.datasources_state_confs[
                    DEFAULT_INFO_MAPPER][data_type]

                return values_conf[upper_state] if upper_state in values_conf \
                    else values_conf[None]
        except Exception:
            LOG.error('Exception in datasource: %s', datasource_name)
            raise

    def _find_operational_state_and_priority(self,
                                             new_vertex,
                                             graph_vertex,
                                             property_,
                                             datasource_name):
        state = self._get_updated_property(new_vertex,
                                           graph_vertex,
                                           property_)

        upper_state = state if not state else state.upper()

        vitrage_operational_state = self.vitrage_operational_state(
            datasource_name, upper_state)

        state_priority = self.state_priority(datasource_name,
                                             upper_state)

        return vitrage_operational_state, upper_state, state_priority

    @staticmethod
    def _get_all_local_variables_of_class(class_instance):
        return [getattr(class_instance, attr) for attr in dir(class_instance)
                if not callable(attr) and not attr.startswith("__")]

    def _check_state_confs_exists(self,
                                  ok_datasources,
                                  error_datasources):

        datasource_types = self.conf.datasources.types
        datasources_with_state_conf = ok_datasources + error_datasources

        for datasource_type in datasource_types:
            if datasource_type not in datasources_with_state_conf:
                LOG.info("No state configuration file for: %s",
                         datasource_type)

    @staticmethod
    def _get_updated_property(new_vertex, graph_vertex, prop):
        if new_vertex and prop in new_vertex.properties:
            return new_vertex[prop]
        elif graph_vertex and prop in graph_vertex.properties:
            return graph_vertex[prop]

        return None
