# Copyright 2017 - Nokia
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

from vitrage.common.constants import EdgeLabel
from vitrage.common.constants import EntityCategory
from vitrage.common.constants import GraphAction
from vitrage.common.constants import VertexProperties as VProps
from vitrage.datasources.alarm_properties import AlarmProperties as AlarmProps
from vitrage.datasources.nova.host import NOVA_HOST_DATASOURCE
from vitrage.tests.unit.datasources.test_transformer_base import \
    BaseTransformerTest


# noinspection PyProtectedMember
class BaseAlarmTransformerTest(BaseTransformerTest):

    def _validate_alarm_vertex_props(self,
                                     vertex,
                                     expected_name,
                                     expected_datasource_name,
                                     expected_sample_time):
        self._validate_base_vertex_props(vertex,
                                         expected_name,
                                         expected_datasource_name)

        self.assertEqual(EntityCategory.ALARM, vertex[VProps.VITRAGE_CATEGORY])
        self.assertEqual(expected_sample_time,
                         vertex[VProps.VITRAGE_SAMPLE_TIMESTAMP])

        if self._is_erroneous(vertex):
            self.assertEqual(AlarmProps.ACTIVE_STATE, vertex[VProps.STATE])
        else:
            self.assertEqual(AlarmProps.INACTIVE_STATE, vertex[VProps.STATE])

    def _validate_host_neighbor(self,
                                wrapper,
                                alarm_id,
                                host_name):

        self.assertEqual(1, len(wrapper.neighbors))
        host_neighbor = wrapper.neighbors[0]

        host_transformer = self.transformers[NOVA_HOST_DATASOURCE]
        properties = {
            VProps.ID: host_name,
            VProps.VITRAGE_TYPE: NOVA_HOST_DATASOURCE,
            VProps.VITRAGE_CATEGORY: EntityCategory.RESOURCE,
            VProps.VITRAGE_SAMPLE_TIMESTAMP:
                wrapper.vertex[VProps.VITRAGE_SAMPLE_TIMESTAMP],
        }
        expected_neighbor = host_transformer.\
            create_neighbor_placeholder_vertex(**properties)

        self.assertEqual(expected_neighbor, host_neighbor.vertex)

        # Validate neighbor edge
        edge = host_neighbor.edge
        self.assertEqual(edge.source_id, alarm_id)
        self.assertEqual(edge.target_id, host_neighbor.vertex.vertex_id)
        self.assertEqual(edge.label, EdgeLabel.ON)

    def _validate_graph_action(self, wrapper):
        if self._is_erroneous(wrapper.vertex):
            self.assertEqual(GraphAction.UPDATE_ENTITY, wrapper.action)
        else:
            self.assertEqual(GraphAction.DELETE_ENTITY, wrapper.action)

    @abc.abstractmethod
    def _is_erroneous(self, vertex):
        pass
