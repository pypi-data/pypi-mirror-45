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

from sympy.logic.boolalg import Not
from sympy import Symbol

from oslo_log import log
from six.moves import reduce

from vitrage.common.constants import EdgeProperties as EProps
from vitrage.evaluator.actions.base import ActionType
from vitrage.evaluator.condition import convert_to_dnf_format
from vitrage.evaluator.condition import get_condition_common_targets
from vitrage.evaluator.condition import is_condition_include_positive_clause
from vitrage.evaluator.condition import parse_condition
from vitrage.evaluator.condition import SymbolResolver
from vitrage.evaluator.template_fields import TemplateFields
from vitrage.evaluator.template_validation.content. \
    add_causal_relationship_validator import AddCausalRelationshipValidator
from vitrage.evaluator.template_validation.content.base import \
    get_content_correct_result
from vitrage.evaluator.template_validation.content.base import \
    get_content_fault_result
from vitrage.evaluator.template_validation.content.base import \
    validate_template_id
from vitrage.evaluator.template_validation.content.execute_mistral_validator \
    import ExecuteMistralValidator
from vitrage.evaluator.template_validation.content.mark_down_validator \
    import MarkDownValidator
from vitrage.evaluator.template_validation.content.raise_alarm_validator \
    import RaiseAlarmValidator
from vitrage.evaluator.template_validation.content.set_state_validator \
    import SetStateValidator
from vitrage.evaluator.template_validation.status_messages import status_msgs

LOG = log.getLogger(__name__)


def content_validation(template):

    template_definitions = template[TemplateFields.DEFINITIONS]

    entities_index = {}
    entities = template_definitions[TemplateFields.ENTITIES]
    result = _validate_entities_definition(entities, entities_index)

    relationships_index = {}

    if result.is_valid_config and \
       TemplateFields.RELATIONSHIPS in template_definitions:

        relationships = template_definitions[TemplateFields.RELATIONSHIPS]
        result = _validate_relationships_definitions(relationships,
                                                     relationships_index,
                                                     entities_index)
    if result.is_valid_config:
        scenarios = template[TemplateFields.SCENARIOS]
        definitions_index = entities_index.copy()
        definitions_index.update(relationships_index)
        result = _validate_scenarios(scenarios, definitions_index)

    return result


def _validate_entities_definition(entities, entities_index):

    for entity in entities:

        entity_dict = entity[TemplateFields.ENTITY]
        result = _validate_entity_definition(entity_dict, entities_index)

        if not result.is_valid_config:
            return result

        entities_index[entity_dict[TemplateFields.TEMPLATE_ID]] = entity_dict

    return get_content_correct_result()


def _validate_entity_definition(entity_dict, entities_index):

    template_id = entity_dict[TemplateFields.TEMPLATE_ID]
    if template_id in entities_index:
        LOG.error('%s status code: %s' % (status_msgs[2], 2))
        return get_content_fault_result(2)

    return get_content_correct_result()


def _validate_relationships_definitions(relationships,
                                        relationships_index,
                                        entities_index):

    for relationship in relationships:

        relationship_dict = relationship[TemplateFields.RELATIONSHIP]
        result = _validate_relationship(relationship_dict,
                                        relationships_index,
                                        entities_index)
        if not result.is_valid_config:
            return result

        template_id = relationship_dict[TemplateFields.TEMPLATE_ID]
        relationships_index[template_id] = relationship_dict
    return get_content_correct_result()


def _validate_relationship(relationship, relationships_index, entities_index):

    template_id = relationship[TemplateFields.TEMPLATE_ID]
    if template_id in relationships_index or template_id in entities_index:
        LOG.error('%s status code: %s' % (status_msgs[2], 2))
        return get_content_fault_result(2)

    target = relationship[TemplateFields.TARGET]
    result = validate_template_id(entities_index, target)

    if result.is_valid_config:
        source = relationship[TemplateFields.SOURCE]
        result = validate_template_id(entities_index, source)

    return result


def _validate_scenarios(scenarios, definitions_index):

    for scenario in scenarios:

        scenario_values = scenario[TemplateFields.SCENARIO]

        condition = scenario_values[TemplateFields.CONDITION]
        result = _validate_scenario_condition(condition, definitions_index)

        if not result.is_valid_config:
            return result

        actions = scenario_values[TemplateFields.ACTIONS]
        result = _validate_scenario_actions(actions, definitions_index)

        if not result.is_valid_config:
            return result

    return get_content_correct_result()


def _validate_scenario_condition(condition, definitions_index):
    try:
        dnf_result = convert_to_dnf_format(condition)
    except Exception:
        LOG.error('%s status code: %s' % (status_msgs[85], 85))
        return get_content_fault_result(85)

    # not condition validation
    not_condition_result = \
        _validate_not_condition(dnf_result, definitions_index)
    if not not_condition_result.is_valid_config:
        return not_condition_result

    # template id validation
    values_to_replace = ' and ', ' or ', ' not ', 'not ', '(', ')'
    condition_vars = reduce(lambda cond, v: cond.replace(v, ' '),
                            values_to_replace,
                            condition)

    for condition_var in condition_vars.split(' '):

        if len(condition_var.strip()) == 0:
            continue

        result = validate_template_id(definitions_index, condition_var)
        if not result.is_valid_config:
            return result

    # condition structure validation
    condition_structure_result = \
        validate_condition_structure(parse_condition(condition),
                                     definitions_index)
    if not condition_structure_result.is_valid_config:
        return condition_structure_result

    return get_content_correct_result()


def validate_condition_structure(condition_dnf, definitions_index):
    result = validate_condition_includes_positive_clause(condition_dnf)
    if not result.is_valid_config:
        return result

    common_targets = get_condition_common_targets(condition_dnf,
                                                  definitions_index,
                                                  TemplateSymbolResolver())

    return get_content_correct_result() if common_targets \
        else get_content_fault_result(135)


def validate_condition_includes_positive_clause(condition):
    return get_content_correct_result() if \
        is_condition_include_positive_clause(condition) \
        else get_content_fault_result(134)


class TemplateSymbolResolver(SymbolResolver):
    def is_relationship(self, symbol):
        return TemplateFields.RELATIONSHIP_TYPE in symbol

    def get_relationship_source_id(self, relationship):
        return relationship[TemplateFields.SOURCE]

    def get_relationship_target_id(self, relationship):
        return relationship[TemplateFields.TARGET]

    def get_entity_id(self, entity):
        return entity[TemplateFields.TEMPLATE_ID]


def _validate_not_condition(dnf_result, definitions_index):
    """Not operator validation

    Not operator can appear only on edges.

    :param dnf_result:
    :param definitions_index:
    :return:
    """

    if isinstance(dnf_result, Not):
        for arg in dnf_result.args:
            if isinstance(arg, Symbol):
                definition = definitions_index.get(str(arg), None)
                if not (definition and
                        definition.get(EProps.RELATIONSHIP_TYPE)):
                    msg = status_msgs[86] + ' template id: %s' % arg
                    LOG.error('%s status code: %s' % (msg, 86))
                    return get_content_fault_result(86, msg)
            else:
                res = _validate_not_condition(arg, definitions_index)
                if not res.is_valid_config:
                    return res
        return get_content_correct_result()

    for arg in dnf_result.args:
        if not isinstance(arg, Symbol):
            res = _validate_not_condition(arg, definitions_index)
            if not res.is_valid_config:
                return res

    return get_content_correct_result()


def _validate_scenario_actions(actions, definitions_index):

    for action in actions:
        result = _validate_scenario_action(action[TemplateFields.ACTION],
                                           definitions_index)
        if not result.is_valid_config:
            return result

    return get_content_correct_result()


def _validate_scenario_action(action, definitions_index):

    action_type = action[TemplateFields.ACTION_TYPE]

    action_validators = {
        ActionType.RAISE_ALARM: RaiseAlarmValidator(),
        ActionType.SET_STATE: SetStateValidator(),
        ActionType.ADD_CAUSAL_RELATIONSHIP: AddCausalRelationshipValidator(),
        ActionType.MARK_DOWN: MarkDownValidator(),
        ActionType.EXECUTE_MISTRAL: ExecuteMistralValidator(),
    }

    if action_type not in action_validators:
        LOG.error('%s status code: %s' % (status_msgs[120], 120))
        return get_content_fault_result(120)

    return action_validators[action_type].validate(action, definitions_index)
