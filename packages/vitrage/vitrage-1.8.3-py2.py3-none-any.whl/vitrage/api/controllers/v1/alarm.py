# Copyright 2016 - Nokia Corporation
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

import json
import pecan

from oslo_log import log
from oslo_utils.strutils import bool_from_string
from osprofiler import profiler
from pecan.core import abort

from vitrage.api.controllers.rest import RootRestController
from vitrage.api.policy import enforce


LOG = log.getLogger(__name__)


@profiler.trace_cls("alarm controller",
                    info={}, hide_args=False, trace_private=False)
class AlarmsController(RootRestController):

    @pecan.expose('json')
    def index(self, vitrage_id, all_tenants=False):
        return self.get(vitrage_id, all_tenants)

    @pecan.expose('json')
    def get(self, vitrage_id, all_tenants=False):
        all_tenants = bool_from_string(all_tenants)
        if all_tenants:
            enforce("list alarms:all_tenants", pecan.request.headers,
                    pecan.request.enforcer, {})
        else:
            enforce("list alarms", pecan.request.headers,
                    pecan.request.enforcer, {})

        LOG.info('returns list alarms with vitrage id %s', vitrage_id)

        try:
            return self._get_alarms(vitrage_id, all_tenants)
        except Exception as e:
            LOG.exception('failed to get alarms %s', e)
            abort(404, str(e))

    @staticmethod
    def _get_alarms(vitrage_id=None, all_tenants=False):
        alarms_json = pecan.request.client.call(pecan.request.context,
                                                'get_alarms',
                                                vitrage_id=vitrage_id,
                                                all_tenants=all_tenants)
        LOG.info(alarms_json)

        try:
            alarms_list = json.loads(alarms_json)['alarms']
            return alarms_list

        except Exception as e:
            LOG.exception('failed to open file %s ', e)
            abort(404, str(e))
