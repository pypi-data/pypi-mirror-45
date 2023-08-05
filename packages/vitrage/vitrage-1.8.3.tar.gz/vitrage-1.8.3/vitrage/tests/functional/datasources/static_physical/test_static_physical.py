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

from oslo_config import cfg

from vitrage.common.constants import DatasourceProperties as DSProps
from vitrage.common.constants import EntityCategory
from vitrage.common.constants import VertexProperties as VProps
from vitrage.datasources.nagios import NAGIOS_DATASOURCE
from vitrage.datasources import NOVA_HOST_DATASOURCE
from vitrage.datasources import NOVA_INSTANCE_DATASOURCE
from vitrage.datasources import NOVA_ZONE_DATASOURCE
from vitrage.datasources.static_physical import STATIC_PHYSICAL_DATASOURCE
from vitrage.datasources.static_physical import SWITCH
from vitrage.tests.functional.datasources.base import \
    TestDataSourcesBase
from vitrage.tests.mocks import mock_driver


class TestStaticPhysical(TestDataSourcesBase):

    DATASOURCES_OPTS = [
        cfg.ListOpt('types',
                    default=[NAGIOS_DATASOURCE,
                             NOVA_HOST_DATASOURCE,
                             NOVA_INSTANCE_DATASOURCE,
                             NOVA_ZONE_DATASOURCE,
                             STATIC_PHYSICAL_DATASOURCE],
                    help='Names of supported driver data sources'),

        cfg.ListOpt('path',
                    default=['vitrage.datasources'],
                    help='base path for data sources')
    ]

    # noinspection PyPep8Naming
    @classmethod
    def setUpClass(cls):
        super(TestStaticPhysical, cls).setUpClass()
        cls.conf = cfg.ConfigOpts()
        cls.conf.register_opts(cls.PROCESSOR_OPTS, group='entity_graph')
        cls.conf.register_opts(cls.DATASOURCES_OPTS, group='datasources')
        cls.load_datasources(cls.conf)

    def test_static_physical_validity(self):
        # Setup
        processor = self._create_processor_with_graph(self.conf, uuid=True)
        transformers = processor.transformer_manager.transformers
        transformers[SWITCH] = transformers[STATIC_PHYSICAL_DATASOURCE]
        self.assertEqual(self._num_total_expected_vertices(),
                         len(processor.entity_graph))

        spec_list = mock_driver.simple_switch_generators(
            switch_num=1,
            host_num=1,
            snapshot_events=1)
        static_events = mock_driver.generate_random_events_list(spec_list)
        static_physical_event = static_events[0]
        static_physical_event[DSProps.ENTITY_TYPE] = SWITCH
        static_physical_event['relationships'][0]['name'] = \
            self._find_entity_id_by_type(processor.entity_graph,
                                         NOVA_HOST_DATASOURCE)

        # Action
        processor.process_event(static_physical_event)

        # Test assertions
        self.assertEqual(self._num_total_expected_vertices() + 1,
                         len(processor.entity_graph))

        static_physical_vertices = processor.entity_graph.get_vertices(
            vertex_attr_filter={
                VProps.VITRAGE_CATEGORY: EntityCategory.RESOURCE,
                VProps.VITRAGE_TYPE: SWITCH
            })
        self.assertEqual(1, len(static_physical_vertices))

        static_physical_neighbors = processor.entity_graph.neighbors(
            static_physical_vertices[0].vertex_id)
        self.assertEqual(1, len(static_physical_neighbors))

        self.assertEqual(NOVA_HOST_DATASOURCE,
                         static_physical_neighbors[0][VProps.VITRAGE_TYPE])
