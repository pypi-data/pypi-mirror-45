# Copyright 2015 - Alcatel-Lucent
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

import abc
from collections import namedtuple
import six

from oslo_log import log as logging

import vitrage.common.constants as cons
from vitrage.common.constants import DatasourceAction
from vitrage.common.constants import DatasourceOpts as DSOpts
from vitrage.common.constants import DatasourceProperties as DSProps
from vitrage.common.constants import EntityCategory
from vitrage.common.constants import GraphAction
from vitrage.common.constants import UpdateMethod
from vitrage.common.constants import VertexProperties as VProps
from vitrage.common.exception import VitrageTransformerError
from vitrage.datasources import OPENSTACK_CLUSTER
import vitrage.graph.utils as graph_utils
from vitrage.utils import datetime as datetime_utils
from vitrage.utils import opt_exists

LOG = logging.getLogger(__name__)

EntityWrapper = \
    namedtuple('EntityWrapper', ['vertex', 'neighbors', 'action'])

Neighbor = namedtuple('Neighbor', ['vertex', 'edge'])


TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


AVAILABLE = 'available'
CLUSTER_ID = 'OpenStack Cluster'


def extract_field_value(entity_event, *args):
    try:
        value = entity_event
        for key in args:
            value = value[key]

        return value
    except Exception:
        return None


def build_key(key_values):
    return TransformerBase.KEY_SEPARATOR.join(map(str, key_values))


def create_cluster_placeholder_vertex():
    key = build_key([cons.EntityCategory.RESOURCE,
                     OPENSTACK_CLUSTER,
                     CLUSTER_ID])

    metadata = {
        cons.VertexProperties.NAME: OPENSTACK_CLUSTER
    }

    return graph_utils.create_vertex(
        key,
        vitrage_category=cons.EntityCategory.RESOURCE,
        vitrage_type=OPENSTACK_CLUSTER,
        entity_id=CLUSTER_ID,
        entity_state=AVAILABLE,
        metadata=metadata
    )


def convert_timestamp_format(current_timestamp_format, timestamp):

    return datetime_utils.change_time_str_format(
        timestamp,
        current_timestamp_format,
        TIMESTAMP_FORMAT
    )


def is_update_event(event):
    return event[DSProps.DATASOURCE_ACTION] == DatasourceAction.UPDATE


@six.add_metaclass(abc.ABCMeta)
class TransformerBase(object):

    KEY_SEPARATOR = ':'
    QUERY_RESULT = 'graph_query_result'
    METADATA = 'metadata'

    # graph actions which need to refer them differently
    GRAPH_ACTION_MAPPING = {}

    def __init__(self, transformers, conf):
        self.conf = conf
        self.transformers = transformers

    def transform(self, entity_event):
        """Transform an entity event into entity wrapper.

        Entity event is received from driver and it need to be
        transformed into entity wrapper. The wrapper contains:
            1. Entity Vertex - The vertex itself with all fields
            2. Neighbor list - neighbor placeholder vertex and an edge
            3. Action type - CREATE/UPDATE/DELETE

        :param entity_event: a general event from the driver
        :return: entity wrapper
        :rtype:EntityWrapper
        """

        if not self._is_end_message(entity_event):
            entity_vertex = self._create_entity_vertex(entity_event)
            neighbors = self._create_neighbors(entity_event)
            action = self._extract_graph_action(entity_event)

            return EntityWrapper(entity_vertex, neighbors, action)
        else:
            return EntityWrapper(self._create_end_vertex(entity_event),
                                 None,
                                 GraphAction.END_MESSAGE)

    def _create_entity_vertex(self, entity_event):
        if is_update_event(entity_event) and \
                opt_exists(self.conf, self.get_vitrage_type()) and \
                opt_exists(self.conf[self.get_vitrage_type()],
                           DSOpts.UPDATE_METHOD):
            update_method = \
                self.conf[self.get_vitrage_type()].update_method.lower()
            if update_method == UpdateMethod.PUSH:
                return self._create_update_entity_vertex(entity_event)
            elif update_method == UpdateMethod.PULL:
                return self._create_snapshot_entity_vertex(entity_event)
            elif update_method == UpdateMethod.NONE:
                return None
            else:
                LOG.error('Update event arrived for dataresource that is '
                          'defined without updates')
        else:
            return self._create_snapshot_entity_vertex(entity_event)

    @abc.abstractmethod
    def _create_snapshot_entity_vertex(self, entity_event):
        pass

    @abc.abstractmethod
    def _create_update_entity_vertex(self, entity_event):
        pass

    def _create_neighbors(self, entity_event):
        """Extracts entity neighbors received from a given entity event.

         Extracting entity neighbors from a given event provided
         by driver

         :param entity_event: an event provided by driver
         :return: neighbors - a list of neighbors where each item in the list
                              is a tuple of (vertex, edge)
         :rtype: list
         """

        if is_update_event(entity_event):
            return self._create_update_neighbors(entity_event)
        else:
            return self._create_snapshot_neighbors(entity_event)

    def _create_snapshot_neighbors(self, entity_event):
        return []

    def _create_update_neighbors(self, entity_event):
        return []

    @abc.abstractmethod
    def _create_entity_key(self, entity_event):
        """Create entity key from given event

        By given an entity event, return a entity key which
        consisting key fields

        :param entity_event: event that returns from the driver
        :return: key
        """
        pass

    def _create_neighbor(self,
                         entity_event,
                         neighbor_id,
                         neighbor_datasource_type,
                         relationship_type,
                         neighbor_category=EntityCategory.RESOURCE,
                         is_entity_source=True,
                         metadata=None):
        metadata = {} if metadata is None else metadata
        # create placeholder vertex
        entity_vitrage_id = self._create_entity_key(entity_event)
        vitrage_sample_timestamp = entity_event[DSProps.SAMPLE_DATE]
        properties = {
            VProps.ID: neighbor_id,
            VProps.VITRAGE_TYPE: neighbor_datasource_type,
            VProps.VITRAGE_CATEGORY: neighbor_category,
            VProps.VITRAGE_SAMPLE_TIMESTAMP: vitrage_sample_timestamp,
            self.METADATA: metadata
        }
        neighbor_vertex = \
            self.create_neighbor_placeholder_vertex(**properties)

        # connect placeholder vertex to entity vertex
        edge_direction = self._get_edge_direction(entity_vitrage_id,
                                                  neighbor_vertex.vertex_id,
                                                  is_entity_source)
        relationship_edge = graph_utils.create_edge(
            source_id=edge_direction[0],
            target_id=edge_direction[1],
            relationship_type=relationship_type)

        return Neighbor(neighbor_vertex, relationship_edge)

    @staticmethod
    def _get_edge_direction(entity_id,
                            neighbor_id,
                            is_entity_source):
        source_id = entity_id
        target_id = neighbor_id

        if not is_entity_source:
            source_id = neighbor_id
            target_id = entity_id

        return source_id, target_id

    def _key_values(self, *args):
        return (EntityCategory.RESOURCE,) + args

    def create_neighbor_placeholder_vertex(self, **kwargs):
        if VProps.VITRAGE_TYPE not in kwargs:
            LOG.error("Can't create placeholder vertex. Missing property TYPE")
            raise ValueError('Missing property TYPE')

        if VProps.ID not in kwargs:
            LOG.error("Can't create placeholder vertex. Missing property ID")
            raise ValueError('Missing property ID')

        metadata = {}
        if self.METADATA in kwargs:
            metadata = kwargs[self.METADATA]

        key_fields = self._key_values(kwargs[VProps.VITRAGE_TYPE],
                                      kwargs[VProps.ID])

        return graph_utils.create_vertex(
            build_key(key_fields),
            vitrage_category=kwargs[VProps.VITRAGE_CATEGORY],
            vitrage_type=kwargs[VProps.VITRAGE_TYPE],
            vitrage_sample_timestamp=kwargs[VProps.VITRAGE_SAMPLE_TIMESTAMP],
            vitrage_is_placeholder=kwargs.get(VProps.VITRAGE_IS_PLACEHOLDER,
                                              True),
            entity_id=kwargs[VProps.ID],
            metadata=metadata)

    def _extract_graph_action(self, entity_event):
        """Extract graph action.

        Decides what action (from constants.GraphAction) the processor need
        to perform according to the data received from the event.

        :param entity_event: event that returns from the driver
        :return: the action that the processor needs to perform
        :rtype: str
        """
        if DSProps.EVENT_TYPE in entity_event and \
            entity_event[DSProps.EVENT_TYPE] in GraphAction.__dict__.values():
            return entity_event[DSProps.EVENT_TYPE]

        datasource_action = entity_event[DSProps.DATASOURCE_ACTION]

        if DatasourceAction.UPDATE == datasource_action:
            return self.GRAPH_ACTION_MAPPING.get(
                entity_event.get(DSProps.EVENT_TYPE, None),
                GraphAction.UPDATE_ENTITY)

        if DatasourceAction.SNAPSHOT == datasource_action:
            return GraphAction.UPDATE_ENTITY

        if DatasourceAction.INIT_SNAPSHOT == datasource_action:
            return GraphAction.CREATE_ENTITY

        raise VitrageTransformerError(
            'Invalid action type: (%s)' % datasource_action)

    @staticmethod
    def _create_end_vertex(entity_event):
        entity_type = entity_event[DSProps.ENTITY_TYPE]
        return graph_utils.create_vertex('END_MESSAGE:' + entity_type,
                                         vitrage_type=entity_type)

    @staticmethod
    def _is_end_message(entity_event):

        ds_action = entity_event[DSProps.DATASOURCE_ACTION]
        is_snapshot_event = ds_action == DatasourceAction.INIT_SNAPSHOT
        event_type = entity_event.get(DSProps.EVENT_TYPE, None)
        return is_snapshot_event and event_type == GraphAction.END_MESSAGE

    @staticmethod
    def _format_update_timestamp(update_timestamp, sample_timestamp):
        return update_timestamp if update_timestamp else sample_timestamp

    @staticmethod
    def get_enrich_query(event):
        """Allow running a query on the graph vertices

        The result of the query specified here will be added to the event in
        the 'QUERY_RESULT' field.

         Example:
         -------
          query = {'vitrage_type': 'nova.instance'}
          Before transform is called the result of running the query against
          the topology graph will be updated to event[QUERY_RESULT]
          To contain the list of all the vertices with
          vitrage_type=nova.instance
        """
        return None

    @abc.abstractmethod
    def get_vitrage_type(self):
        """Returns the vitrage_type of the datasource

        :return: datasource type
        :rtype: String
        """
        pass
