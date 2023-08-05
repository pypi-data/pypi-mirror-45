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

from oslo_log import log
import oslo_messaging
from oslo_service import service as os_service
from oslo_utils import importutils

from vitrage import messaging
from vitrage.opts import register_opts

LOG = log.getLogger(__name__)


class VitrageNotifierService(os_service.Service):

    def __init__(self, conf):
        super(VitrageNotifierService, self).__init__()
        self.conf = conf
        self.notifiers = self.get_notifier_plugins(conf)
        self._init_listeners(self.conf)

    def start(self):
        LOG.info("Vitrage Notifier Service - Starting...")

        super(VitrageNotifierService, self).start()
        for listener in self.listeners:
            listener.start()

        LOG.info("Vitrage Notifier Service - Started!")

    def stop(self, graceful=False):
        LOG.info("Vitrage Notifier Service - Stopping...")

        for listener in self.listeners:
            listener.stop()
            listener.wait()

        super(VitrageNotifierService, self).stop(graceful)

        LOG.info("Vitrage Notifier Service - Stopped!")

    @staticmethod
    def get_notifier_plugins(conf):
        notifiers = []
        conf_notifier_names = conf.notifiers
        if not conf_notifier_names:
            LOG.info('There are no notifier plugins in configuration')
            return []
        for notifier_name in conf_notifier_names:
            register_opts(conf, notifier_name, conf.notifiers_path)
            LOG.info('Notifier plugin %s started', notifier_name)
            notifiers.append(importutils.import_object(
                conf[notifier_name].notifier,
                conf))
        return notifiers

    def _init_listeners(self, conf):
        self.listeners = []
        transport = messaging.get_transport(conf)

        self._init_notifier(transport=transport,
                            topic=conf.entity_graph.notifier_topic,
                            endpoint=VitrageDefaultEventEndpoint(
                                self.notifiers))

        for notifier in self.notifiers:
            if notifier.use_private_topic():
                self._init_notifier(transport=transport,
                                    topic=notifier.get_notifier_name(),
                                    endpoint=notifier)

    def _init_notifier(self, transport, topic, endpoint):
        LOG.debug('Initializing notifier with topic %s', topic)

        self.listeners.append(messaging.get_notification_listener(
            transport, [oslo_messaging.Target(topic=topic)], [endpoint]))


class VitrageDefaultEventEndpoint(object):

    def __init__(self, notifiers):
        self.notifiers = notifiers

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        """Endpoint for alarm notifications"""
        LOG.info('Vitrage Event Info: publisher_id %s', publisher_id)
        LOG.info('Vitrage Event Info: event_type %s', event_type)
        LOG.info('Vitrage Event Info: metadata %s', metadata)
        LOG.info('Vitrage Event Info: payload %s', payload)
        for plugin in self.notifiers:
            plugin.process_event(payload, event_type)
