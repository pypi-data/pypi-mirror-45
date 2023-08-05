# Copyright 2016 - ZTE, Nokia
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

from vitrage.common.constants import DatasourceOpts as DSOpts
from vitrage.common.constants import DatasourceProperties as DSProps
from vitrage.common.constants import UpdateMethod
from vitrage.datasources.aodh import AODH_DATASOURCE
from vitrage.datasources.aodh.properties import AodhEventType
from vitrage.datasources.aodh.properties import AodhProperties as AodhProps
from vitrage.tests import base
from vitrage.tests.mocks import mock_driver
from vitrage.tests.unit.datasources.aodh.mock_driver import MockAodhDriver


class AodhDriverTest(base.BaseTest):

    OPTS = [
        cfg.StrOpt(DSOpts.UPDATE_METHOD,
                   default=UpdateMethod.PUSH),
    ]

    # noinspection PyPep8Naming
    @classmethod
    def setUpClass(cls):
        cls.conf = cfg.ConfigOpts()
        cls.conf.register_opts(cls.OPTS, group=AODH_DATASOURCE)

    def test_enrich_event(self):

        aodh_driver = MockAodhDriver(self.conf)

        # 1. alarm creation with 'ok' state
        # prepare data
        detail_data = {"type": "creation",
                       AodhProps.DETAIL: self._extract_alarm_data()}
        generators = \
            mock_driver.simple_aodh_alarm_notification_generators(
                alarm_num=1,
                update_events=1,
                update_vals=detail_data)
        alarm = mock_driver.generate_sequential_events_list(generators)[0]
        alarm_info = alarm.copy()

        # action
        entity = aodh_driver.enrich_event(alarm, AodhEventType.CREATION)

        # Test assertions
        # alarm with status OK should not be handled
        self.assertIsNone(entity)

        # 2.alarm state transition from 'ok' to 'alarm'
        detail_data = {"type": "state transition",
                       AodhProps.DETAIL: {AodhProps.STATE: "alarm"}}
        alarm.update(detail_data)
        entity = aodh_driver.enrich_event(alarm,
                                          AodhEventType.STATE_TRANSITION)

        # Test assertions
        # alarm state change: ok->alarm, need to be added
        self.assertIsNotNone(entity)
        self._validate_aodh_entity_comm_props(entity, alarm_info)
        self.assertEqual(entity[AodhProps.STATE],
                         alarm[AodhProps.DETAIL][AodhProps.STATE])
        self.assertEqual(entity[AodhProps.SEVERITY],
                         alarm[AodhProps.SEVERITY])
        self.assertEqual(entity[DSProps.EVENT_TYPE],
                         AodhEventType.STATE_TRANSITION)

        # 3. delete alarm which is 'alarm' state
        # prepare data
        detail_data = {"type": "deletion"}
        alarm.update(detail_data)

        # action
        entity = aodh_driver.enrich_event(alarm, AodhEventType.DELETION)

        # Test assertions
        self.assertIsNotNone(entity)
        self._validate_aodh_entity_comm_props(entity, alarm_info)
        self.assertEqual(entity[DSProps.EVENT_TYPE],
                         AodhEventType.DELETION)

        # 4. alarm creation with 'alarm' state
        # prepare data
        detail_data = {"type": "creation",
                       AodhProps.DETAIL:
                           self._extract_alarm_data(state="alarm")}
        generators = \
            mock_driver.simple_aodh_alarm_notification_generators(
                alarm_num=1,
                update_events=1,
                update_vals=detail_data)
        alarm = mock_driver.generate_sequential_events_list(generators)[0]
        alarm_info = alarm.copy()

        # action
        entity = aodh_driver.enrich_event(alarm, AodhEventType.CREATION)

        # Test assertions
        # alarm with status 'alarm' need to be added
        self.assertIsNotNone(entity)
        self._validate_aodh_entity_comm_props(entity, alarm_info)
        self.assertEqual(entity[AodhProps.STATE],
                         alarm[AodhProps.DETAIL][AodhProps.STATE])
        self.assertEqual(entity[AodhProps.SEVERITY],
                         alarm[AodhProps.SEVERITY])
        self.assertIsNone(entity[AodhProps.RESOURCE_ID])
        self.assertEqual("*", entity[AodhProps.EVENT_TYPE])
        self.assertEqual(entity[DSProps.EVENT_TYPE],
                         AodhEventType.CREATION)

        # 5. alarm rule change
        # prepare data
        detail_data = {"type": "rule change",
                       AodhProps.DETAIL: {
                           "severity": "critical",
                           AodhProps.RULE:
                               {"query": [{"field": "traits.resource_id",
                                           "type": "",
                                           "value": "1",
                                           "op": "eq"}],
                                "event_type": "instance.update"}}}
        alarm.update(detail_data)

        # action
        entity = aodh_driver.enrich_event(alarm,
                                          AodhEventType.RULE_CHANGE)

        # Test assertions
        # alarm rule change: need to be update
        self.assertIsNotNone(entity)
        self._validate_aodh_entity_comm_props(entity, alarm_info)
        self.assertEqual(entity[AodhProps.SEVERITY],
                         alarm[AodhProps.DETAIL][AodhProps.SEVERITY])
        self.assertEqual(
            entity[AodhProps.EVENT_TYPE],
            alarm[AodhProps.DETAIL][AodhProps.RULE][AodhProps.EVENT_TYPE])
        self.assertEqual("1", entity[AodhProps.RESOURCE_ID])
        self.assertEqual(entity[DSProps.EVENT_TYPE],
                         AodhEventType.RULE_CHANGE)

        # 6. alarm state change from 'alarm' to 'ok'
        # prepare data
        detail_data = {"type": "state transition",
                       AodhProps.DETAIL: {AodhProps.STATE: "ok"}}
        alarm.update(detail_data)

        # action
        entity = aodh_driver.enrich_event(alarm,
                                          AodhEventType.STATE_TRANSITION)

        # Test assertions
        # alarm state change: alarm->OK, need to be deleted
        self.assertIsNotNone(entity)
        self._validate_aodh_entity_comm_props(entity, alarm_info)
        self.assertEqual(entity[DSProps.EVENT_TYPE],
                         AodhEventType.STATE_TRANSITION)

        # 7. delete alarm which is 'ok' state
        # prepare data
        detail_data = {"type": "deletion"}
        alarm.update(detail_data)

        # action
        entity = aodh_driver.enrich_event(alarm, AodhEventType.DELETION)

        # Test assertions
        self.assertIsNone(entity)

    def _extract_alarm_data(self,
                            state="ok",
                            type="event",
                            rule=None):

        if rule is None:
            rule = {"query": [], "event_type": "*"}
        return {AodhProps.DESCRIPTION: "test",
                AodhProps.TIMESTAMP: "2016-11-09T01:39:13.839584",
                AodhProps.ENABLED: True,
                AodhProps.STATE_TIMESTAMP: "2016-11-09T01:39:13.839584",
                AodhProps.ALARM_ID: "7e5c3754-e2eb-4782-ae00-7da5ded8568b",
                AodhProps.REPEAT_ACTIONS: False,
                AodhProps.PROJECT_ID: "c365d18fcc03493187016ae743f0cc4d",
                AodhProps.NAME: "test",
                AodhProps.SEVERITY: "low",
                AodhProps.TYPE: type,
                AodhProps.STATE: state,
                AodhProps.RULE: rule}

    def _validate_aodh_entity_comm_props(self, entity, alarm):

        self.assertEqual(entity[AodhProps.ALARM_ID],
                         alarm[AodhProps.ALARM_ID])
        self.assertEqual(entity[AodhProps.PROJECT_ID],
                         alarm[AodhProps.PROJECT_ID])
        self.assertEqual(entity[AodhProps.TIMESTAMP],
                         alarm[AodhProps.TIMESTAMP])
        self.assertEqual(entity[AodhProps.DESCRIPTION],
                         alarm[AodhProps.DETAIL][AodhProps.DESCRIPTION])
        self.assertEqual(entity[AodhProps.ENABLED],
                         alarm[AodhProps.DETAIL][AodhProps.ENABLED])
        self.assertEqual(entity[AodhProps.NAME],
                         alarm[AodhProps.DETAIL][AodhProps.NAME])
        self.assertEqual(entity[AodhProps.REPEAT_ACTIONS],
                         alarm[AodhProps.DETAIL][AodhProps.REPEAT_ACTIONS])
        self.assertEqual(entity[AodhProps.TYPE],
                         alarm[AodhProps.DETAIL][AodhProps.TYPE])
