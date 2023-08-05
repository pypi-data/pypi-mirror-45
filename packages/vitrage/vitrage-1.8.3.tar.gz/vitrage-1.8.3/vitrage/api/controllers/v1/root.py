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

from vitrage.api.controllers.v1 import alarm
from vitrage.api.controllers.v1 import event
from vitrage.api.controllers.v1 import rca
from vitrage.api.controllers.v1 import resource
from vitrage.api.controllers.v1 import template
from vitrage.api.controllers.v1 import topology


class V1Controller(object):
    topology = topology.TopologyController()
    resources = resource.ResourcesController()
    alarm = alarm.AlarmsController()
    rca = rca.RCAController()
    template = template.TemplateController()
    event = event.EventController()
