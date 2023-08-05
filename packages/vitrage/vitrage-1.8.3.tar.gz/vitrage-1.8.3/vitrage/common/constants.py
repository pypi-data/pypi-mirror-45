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


class VertexProperties(object):
    VITRAGE_CATEGORY = 'vitrage_category'
    VITRAGE_TYPE = 'vitrage_type'
    VITRAGE_ID = 'vitrage_id'
    VITRAGE_STATE = 'vitrage_state'
    VITRAGE_IS_DELETED = 'vitrage_is_deleted'
    VITRAGE_IS_PLACEHOLDER = 'vitrage_is_placeholder'
    VITRAGE_SAMPLE_TIMESTAMP = 'vitrage_sample_timestamp'
    VITRAGE_AGGREGATED_STATE = 'vitrage_aggregated_state'
    VITRAGE_OPERATIONAL_STATE = 'vitrage_operational_state'
    VITRAGE_AGGREGATED_SEVERITY = 'vitrage_aggregated_severity'
    VITRAGE_OPERATIONAL_SEVERITY = 'vitrage_operational_severity'
    VITRAGE_RESOURCE_ID = 'vitrage_resource_id'
    ID = 'id'
    STATE = 'state'
    PROJECT_ID = 'project_id'
    UPDATE_TIMESTAMP = 'update_timestamp'
    NAME = 'name'
    SEVERITY = 'severity'
    IS_MARKED_DOWN = 'is_marked_down'
    INFO = 'info'
    GRAPH_INDEX = 'graph_index'
    RAWTEXT = 'rawtext'
    RESOURCE_ID = 'resource_id'
    RESOURCE_NAME = 'resource_name'
    VITRAGE_RESOURCE_ID = 'vitrage_resource_id'
    VITRAGE_RESOURCE_TYPE = 'vitrage_resource_type'
    RESOURCE = 'resource'
    IS_REAL_VITRAGE_ID = 'is_real_vitrage_id'


class EdgeProperties(object):
    RELATIONSHIP_TYPE = 'relationship_type'
    VITRAGE_IS_DELETED = 'vitrage_is_deleted'
    UPDATE_TIMESTAMP = 'update_timestamp'


class EdgeLabel(object):
    ON = 'on'
    CONTAINS = 'contains'
    CAUSES = 'causes'
    ATTACHED = 'attached'
    ATTACHED_PUBLIC = 'attached_public'
    ATTACHED_PRIVATE = 'attached_private'
    CONNECT = 'connect'
    MANAGED_BY = 'managed_by'
    COMPRISED = 'comprised'

    @staticmethod
    def labels():
        return [EdgeLabel.__dict__[label]
                for label in vars(EdgeLabel)
                if not label.startswith(('_', 'labels'))]


class DatasourceAction(object):
    SNAPSHOT = 'snapshot'
    INIT_SNAPSHOT = 'init_snapshot'
    UPDATE = 'update'


class UpdateMethod(object):
    NONE = 'none'
    PULL = 'pull'
    PUSH = 'push'


class EntityCategory(object):
    RESOURCE = 'RESOURCE'
    ALARM = 'ALARM'

    @staticmethod
    def categories():
        return [EntityCategory.__dict__[category]
                for category in vars(EntityCategory)
                if not category.startswith(('_', 'categories'))]


class DatasourceProperties(object):
    ENTITY_TYPE = 'vitrage_entity_type'
    DATASOURCE_ACTION = 'vitrage_datasource_action'
    SAMPLE_DATE = 'vitrage_sample_date'
    EVENT_TYPE = 'vitrage_event_type'


class GraphAction(object):
    CREATE_ENTITY = 'create_entity'
    DELETE_ENTITY = 'delete_entity'
    UPDATE_ENTITY = 'update_entity'
    DELETE_RELATIONSHIP = 'delete_relationship'
    UPDATE_RELATIONSHIP = 'update_relationship'
    REMOVE_DELETED_ENTITY = 'remove_deleted_entity'
    END_MESSAGE = 'end_message'


class NotifierEventTypes(object):
    ACTIVATE_DEDUCED_ALARM_EVENT = 'vitrage.deduced_alarm.activate'
    DEACTIVATE_DEDUCED_ALARM_EVENT = 'vitrage.deduced_alarm.deactivate'
    ACTIVATE_ALARM_EVENT = 'vitrage.alarm.activate'
    DEACTIVATE_ALARM_EVENT = 'vitrage.alarm.deactivate'
    ACTIVATE_MARK_DOWN_EVENT = 'vitrage.mark_down.activate'
    DEACTIVATE_MARK_DOWN_EVENT = 'vitrage.mark_down.deactivate'
    EXECUTE_EXTERNAL_ACTION = 'vitrage.execute_external_action'


class TemplateTopologyFields(object):
    """yaml fields for topology definitions"""
    METADATA = 'metadata'
    DESCRIPTION = 'description'
    NAME = 'name'

    DEFINITIONS = 'definitions'

    ENTITIES = 'entities'
    ENTITY = 'entity'
    TYPE = 'type'
    ID = 'id'

    RELATIONSHIPS = 'relationships'
    RELATIONSHIP = 'relationship'
    RELATIONSHIP_TYPE = 'relationship_type'
    SOURCE = 'source'
    TARGET = 'target'


class EventProperties(object):
    TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
    TYPE = 'type'
    TIME = 'time'
    DETAILS = 'details'


class DatasourceOpts(object):
    TRANSFORMER = 'transformer'
    DRIVER = 'driver'
    UPDATE_METHOD = 'update_method'
    CHANGES_INTERVAL = 'changes_interval'
    CONFIG_FILE = 'config_file'
