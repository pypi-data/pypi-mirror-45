..
      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

Vitrage API
-----------
|

.. contents:: Contents:
   :local:

Overview
********
**This document describes the Vitrage API v1.**

**The Vitrage API provides a RESTful JSON interface for interacting with Vitrage Service.**

List Versions
^^^^^^^^^^^^^

Lists the supported versions of the Vitrage API.

GET /
~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json

Path Parameters
===============

None.

Query Parameters
================

None.

Request Body
============

None.

Request Examples
================

::

    GET / HTTP/1.1
    Host: 135.248.19.18:8999
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7
    Accept: application/json



ResponseStatus code
===================

-  200 - OK

Response Body
=============

Returns a JSON object with a 'links' array of links of supported versions.

Response Examples
=================

::

    {
        "versions": [
            {
               "id": "v1.0",
              "links": [
                    {
                     "href": "http://135.248.19.18:8999/v1/",
                    "rel": "self"
                   }
              ],
              "status": "CURRENT",
              "updated": "2015-11-29"
            }
        ]

    }



Get  topology
^^^^^^^^^^^^^

Get the topology for the cluster.
Its possible to filter the edges vertices and depth of the
graph


POST /v1/topology/
~~~~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json

Path Parameters
===============

None.

Query Parameters
================

None

Request Body
============

Consists of a topology request definition which has the following properties:

* root - (string, optional) the root node to start. defaults to the openstack node
* depth - (int, optional) the depth of the topology graph. defaults to max depth
* graph_type-(string, optional) can be either tree or graph. defaults to graph
* query - (string, optional) a json query filter to filter the graph components. defaults to return all the graph
* all_tenants - (boolean, optional) shows the entities of all the tenants in the graph (in case the user has the permissions).

query expression
================
::

 query := expression
 expression := simple_expression|complex_expression
 simple_expression := {simple_operator: {field_name: value}}
 simple_operator := == | != | < | <= | > | >=
 complex_expression := {complex_operator: [expression, expression, ...]} | not_expression
 not_expression := {not: expression}
 complex_operator := and | or


Query example
=============

::

    POST /v1/topology/
    Host: 135.248.19.18:8999
    Content-Type: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7

    {
        "query" :"
         {
            \"or\": [
              {
                \"==\": {
                  \"vitrage_type\": \"nova.host\"
                }
              },
              {
                \"==\": {
                  \"vitrage_type\": \"nova.instance\"
                }
              },
              {
                \"==\": {
                  \"vitrage_type\": \"nova.zone\"
                }
              },
              {
                \"==\": {
                  \"vitrage_type\": \"openstack.cluster\"
                }
              }
            ]

         }",
         "graph_type" : "tree"
     }

Response Status Code
====================

-  200 - OK
-  400 - Bad request

Response Body
=============

Returns a JSON object that describes a graph with nodes
and links. If a tree representation is asked then returns
a Json tree with nodes and children.

An error of cannot represent as a tree will be return if the
graph is not a tree. (400 - Bad request)

Response Examples
=================

::

 {
  "directed": true,
  "graph": {},
  "nodes": [
    {
      "vitrage_id": "96f6a30a-51eb-4e71-ae4a-0703b21ffa98",
      "name": "openstack.cluster",
      "graph_index": 0,
      "vitrage_category": "RESOURCE",
      "vitrage_operational_state": "OK",
      "state": "available",
      "vitrage_type": "openstack.cluster",
      "vitrage_sample_timestamp": "2018-06-11 08:43:33.757864+00:00",
      "vitrage_aggregated_state": "AVAILABLE",
      "vitrage_is_placeholder": false,
      "id": "OpenStack Cluster",
      "is_real_vitrage_id": true,
      "vitrage_is_deleted": false
    },
    {
      "vitrage_id": "12b11320-a6de-4ce5-892f-78fb1fa6bfef",
      "name": "nova",
      "update_timestamp": "2018-06-11 08:43:33.757864+00:00",
      "vitrage_category": "RESOURCE",
      "vitrage_operational_state": "OK",
      "state": "available",
      "vitrage_type": "nova.zone",
      "vitrage_sample_timestamp": "2018-06-11 08:43:33.757864+00:00",
      "graph_index": 1,
      "vitrage_aggregated_state": "AVAILABLE",
      "vitrage_is_placeholder": false,
      "id": "nova",
      "is_real_vitrage_id": true,
      "vitrage_is_deleted": false
    },
    {
      "vitrage_id": "c90cc1dd-409c-4354-92f8-79b993e584c0",
      "vitrage_is_deleted": false,
      "graph_index": 2,
      "vitrage_category": "RESOURCE",
      "vitrage_operational_state": "N/A",
      "vitrage_type": "nova.instance",
      "vitrage_sample_timestamp": "2018-06-11 08:33:33.457974+00:00",
      "vitrage_aggregated_state": null,
      "vitrage_is_placeholder": true,
      "id": "ce173654-c70d-4514-a3e9-1f9dd5c09dd8",
      "is_real_vitrage_id": true
    },
    {
      "vitrage_id": "94060508-5fea-4927-9a53-2b66864ab883",
      "vitrage_is_deleted": false,
      "graph_index": 3,
      "vitrage_category": "RESOURCE",
      "vitrage_operational_state": "N/A",
      "vitrage_type": "nova.instance",
      "vitrage_sample_timestamp": "2018-06-11 08:33:33.457992+00:00",
      "vitrage_aggregated_state": null,
      "vitrage_is_placeholder": true,
      "id": "3af9a215-e109-476a-aa55-6868990684e4",
      "is_real_vitrage_id": true
    },
    {
      "vitrage_id": "ae0886d8-ee90-41df-a80a-006fdb80105b",
      "graph_index": 4,
      "name": "vm-4",
      "update_timestamp": "2018-06-11 08:43:34.421455+00:00",
      "vitrage_category": "RESOURCE",
      "vitrage_operational_state": "OK",
      "state": "ACTIVE",
      "vitrage_type": "nova.instance",
      "vitrage_sample_timestamp": "2018-06-11 08:43:34.421455+00:00",
      "host_id": "devstack-rocky-8",
      "vitrage_aggregated_state": "ACTIVE",
      "vitrage_is_placeholder": false,
      "project_id": "aa792cde038b41858a0f1bcf8f9b092d",
      "id": "1233e48c-62ee-470e-8d4a-adff30211b5d",
      "is_real_vitrage_id": true,
      "vitrage_is_deleted": false
    },
    {
      "vitrage_id": "4d197913-0687-4300-afb7-7fd331d35cff",
      "graph_index": 5,
      "name": "vm-3",
      "update_timestamp": "2018-06-11 08:43:34.421490+00:00",
      "vitrage_category": "RESOURCE",
      "vitrage_operational_state": "OK",
      "state": "ACTIVE",
      "vitrage_type": "nova.instance",
      "vitrage_sample_timestamp": "2018-06-11 08:47:24.137324+00:00",
      "host_id": "devstack-rocky-8",
      "vitrage_aggregated_state": "ACTIVE",
      "vitrage_is_placeholder": false,
      "project_id": "aa792cde038b41858a0f1bcf8f9b092d",
      "id": "12cc6d3e-f801-4422-b2a0-43cedacb4eb5",
      "is_real_vitrage_id": true,
      "vitrage_is_deleted": false
    },
    {
      "vitrage_id": "5f9893b8-c622-4cb8-912d-534980f4e4f9",
      "name": "devstack-rocky-8",
      "update_timestamp": "2018-06-11 08:43:33.518059+00:00",
      "vitrage_category": "RESOURCE",
      "vitrage_operational_state": "OK",
      "state": "available",
      "vitrage_type": "nova.host",
      "vitrage_sample_timestamp": "2018-06-11 08:43:33.757864+00:00",
      "graph_index": 6,
      "vitrage_aggregated_state": "AVAILABLE",
      "vitrage_is_placeholder": false,
      "id": "devstack-rocky-8",
      "is_real_vitrage_id": true,
      "vitrage_is_deleted": false
    }
  ],
  "links": [
    {
      "relationship_type": "contains",
      "source": 0,
      "vitrage_is_deleted": false,
      "key": "contains",
      "target": 1
    },
    {
      "relationship_type": "contains",
      "source": 1,
      "vitrage_is_deleted": false,
      "key": "contains",
      "target": 6
    },
    {
      "relationship_type": "contains",
      "source": 6,
      "vitrage_is_deleted": false,
      "key": "contains",
      "target": 4
    },
    {
      "relationship_type": "contains",
      "source": 6,
      "vitrage_is_deleted": false,
      "key": "contains",
      "target": 5
    }
  ],
  "multigraph": true
 }

Show RCA
^^^^^^^^

Shows the root cause analysis on an alarm.

GET /v1/rca/
~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json

Path Parameters
===============

None.

Query Parameters
================

alarm id - (string(255)) get rca on this alarm.

Request Body
============

* all_tenants - (boolean, optional) shows the rca of all tenants (in case the user has the permissions).

Request Examples
================

::

    GET /v1/rca/alarm_id=ALARM%3Anagios%3Ahost0%3ACPU%20load HTTP/1.1
    Host: 135.248.19.18:8999
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7
    Accept: application/json



Response Status code
====================

-  200 - OK

Response Body
=============

Returns a JSON object represented as a graph with all the alarms that either causing the alarm or caused by the requested alarm.

Response Examples
=================

::

 {
  "directed": true,
  "graph": {

  },
  "nodes": [
    {
      "vitrage_category": "ALARM",
      "vitrage_type": "nagios",
      "name": "CPU load",
      "state": "Active",
      "severity": "WARNING",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "info": "WARNING - 15min load 1.66 at 32 CPUs",
      "resource_type": "nova.host",
      "resource_name": "host-0",
      "resource_id": "host-0",
      "id": 0,
      "vitrage_id": "a2760124-a174-46a1-926f-0d0d12a94a20"
    },
    {
      "vitrage_category": "ALARM",
      "vitrage_type": "vitrage",
      "name": "Machine Suboptimal",
      "state": "Active",
      "severity": "WARNING",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "resource_type": "nova.instance",
      "resource_name": "vm0",
      "resource_id": "20d12a8a-ea9a-89c6-5947-83bea959362e",
      "id": 1,
      "vitrage_id": "4c0a2724-edce-4125-a74c-bf74d4413967"
    },
    {
      "vitrage_category": "ALARM",
      "vitrage_type": "vitrage",
      "name": "Machine Suboptimal",
      "state": "Active",
      "severity": "WARNING",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "resource_type": "nova.instance",
      "resource_name": "vm1",
      "resource_id": "275097cf-954e-8e24-b185-9514e24b8591",
      "id": 2,
      "vitrage_id": "625f2914-cb0e-453a-977a-900aa7756524"
    }
  ],
  "links": [
    {
      "source": 0,
      "target": 1,
      "relationship": "causes"
    },
    {
      "source": 0,
      "target": 2,
      "relationship": "causes"
    }
  ],
  "multigraph": false,
  "inspected_index": 0
 }


List Alarms
^^^^^^^^^^^

Shows the alarms on a resource or all alarms

GET /v1/alarm/
~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json

Path Parameters
===============

None.

Query Parameters
================

vitrage_id - (string(255)) get alarm on this resource can be 'all' for all alarms.

Request Body
============

* all_tenants - (boolean, optional) shows the alarms of all tenants (in case the user has the permissions).

Request Examples
================

::

    GET /v1/alarm/?vitrage_id=all
    Host: 135.248.19.18:8999
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7
    Accept: application/json

Response Status code
====================

-  200 - OK

Response Body
=============

Returns a JSON object with all the alarms requested.

Response Examples
=================

::


  [
     {
       "vitrage_category": "ALARM",
       "vitrage_type": "nagios",
       "name": "CPU load",
       "state": "Active",
       "severity": "WARNING",
       "update_timestamp": "2015-12-01T12:46:41Z",
       "info": "WARNING - 15min load 1.66 at 32 CPUs",
       "resource_type": "nova.host",
       "resource_name": "host-0",
       "resource_id": "host-0",
       "id": 0,
       "vitrage_id": "517bf941-0bec-4f7c-9870-8b79fc5086d1",
       "normalized_severity": "WARNING"
     },
     {
       "vitrage_category": "ALARM",
       "vitrage_type": "vitrage",
       "name": "Machine Suboptimal",
       "state": "Active",
       "severity": "CRITICAL",
       "update_timestamp": "2015-12-01T12:46:41Z",
       "resource_type": "nova.instance",
       "resource_name": "vm0",
       "resource_id": "20d12a8a-ea9a-89c6-5947-83bea959362e",
       "id": 1,
       "vitrage_id": "3e9f8ca2-1562-4ff8-be08-93427f5328f6",
       "normalized_severity": "CRITICAL"
     },
     {
       "vitrage_category": "ALARM",
       "vitrage_type": "vitrage",
       "name": "Machine Suboptimal",
       "state": "Active",
       "severity": "CRITICAL",
       "update_timestamp": "2015-12-01T12:46:41Z",
       "resource_type": "nova.instance",
       "resource_name": "vm1",
       "resource_id": "275097cf-954e-8e24-b185-9514e24b8591",
       "id": 2,
       "vitrage_id": "0320ba74-ab51-42e8-b60f-525b0ee63da4",
       "normalized_severity": "CRITICAL"
     },
     {
       "vitrage_category": "ALARM",
       "vitrage_type": "aodh",
       "name": "Memory overload",
       "state": "Active",
       "severity": "WARNING",
       "update_timestamp": "2015-12-01T12:46:41Z",
       "info": "WARNING - 15min load 1.66 at 32 CPUs",
       "resource_type": "nova.host",
       "resource_name": "host-0",
       "resource_id": "host-0",
       "id": 3,
       "vitrage_id": "4ee7916d-f8e7-4364-83b0-a7d1fe6ce8c3",
       "normalized_severity": "WARNING"
     }
 ]

Template Validate
^^^^^^^^^^^^^^^^^

An API for validating templates

POST /v1/template/
~~~~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json
-  User-Agent (String)
-  Content-Type (String): application/json

Path Parameters
===============

None.

Query Parameters
================

-  path (string(255), required) - the path to template file or directory

Request Body
============

None

Request Examples
================

::

    POST /v1/template/?path=[file/dir path]
    Host: 135.248.18.122:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    Content-Type: application/json
    Accept: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7

Response Status code
====================

None

Response Body
=============

Returns a JSON object that is a list of results.
Each result describes a full validation (syntax and content) of one template file.

Response Examples
=================

::

    {
      "results": [
        {
          "status": "validation failed",
          "file path": "/tmp/templates/basic_no_meta.yaml",
          "description": "Template syntax validation",
          "message": "metadata is a mandatory section.",
          "status code": 62
        },
        {
          "status": "validation OK",
          "file path": "/tmp/templates/basic.yaml",
          "description": "Template validation",
          "message": "Template validation is OK",
          "status code": 4
        }
      ]
    }

Template List
=============

List all templates loaded from /etc/vitrage/templates, both those that passed validation and those that did not.

GET /v1/template/
~~~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json
-  User-Agent (String)

Path Parameters
===============

None

Query Parameters
================

None

Request Body
============

None

Request Examples
================

::

    GET /v1/template/
    Host: 135.248.18.122:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    Accept: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7

Response Status code
====================

None

Response Body
=============

Returns list of all templates loaded from /etc/vitrage/templates, both those that passed validation and those that did not.

Response Examples
=================

::

    +--------------------------------------+---------------------------------------+--------+--------------------------------------------------+----------------------+
    | uuid                                 | name                                  | status | status details                                   | date                 |
    +--------------------------------------+---------------------------------------+--------+--------------------------------------------------+----------------------+
    | 67bebcb4-53b1-4240-ad05-451f34db2438 | vm_down_causes_suboptimal_application | failed | Entity definition must contain template_id field | 2016-06-29T12:24:16Z |
    | 4cc899e6-f6cb-43d8-94a0-6fa937e41ae2 | host_cpu_load_causes_vm_problem       | pass   | Template validation is OK                        | 2016-06-29T12:24:16Z |
    | 0548367e-711a-4c08-9bdb-cb61f96fed04 | switch_connectivity_issues            | pass   | Template validation is OK                        | 2016-06-29T12:24:16Z |
    | 33cb4400-f846-4c64-b168-530824d38f3e | host_nic_down                         | pass   | Template validation is OK                        | 2016-06-29T12:24:16Z |
    | a04cd155-0fcf-4409-a27c-c83ba8b20a3c | disconnected_storage_problems         | pass   | Template validation is OK                        | 2016-06-29T12:24:16Z |
    +--------------------------------------+---------------------------------------+--------+--------------------------------------------------+----------------------+


Template Show
^^^^^^^^^^^^^

Shows the template body for given template ID

GET /v1/template/[template_uuid]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Headers
=======

-  User-Agent (string)
-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json

Path Parameters
===============

- template uuid

Query Parameters
================

None

Request Body
============

None

Request Examples
================

::

    GET /v1/template/a0bdb89a-fe4c-4b27-adc2-507b7ec44c24
    Host: 135.248.19.18:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7
    Accept: application/json



Response Status code
====================

-  200 - OK
-  404 - failed to show template with uuid: [template_uuid]

Response Body
=============

Returns a JSON object which represents the template body

Response Examples
=================

::

    {
      "scenarios": [
        {
          "scenario": {
            "actions": [
              {
                "action": {
                  "action_target": {
                    "target": "instance"
                  },
                  "properties": {
                    "alarm_name": "exploding_world",
                    "severity": "CRITICAL"
                  },
                  "action_type": "raise_alarm"
                }
              }
            ],
            "condition": "alarm_1_on_host and host_contains_instance"
          }
        },
        {
          "scenario": {
            "actions": [
              {
                "action": {
                  "action_target": {
                    "source": "alarm_1",
                    "target": "alarm_2"
                  },
                  "action_type": "add_causal_relationship"
                }
              }
            ],
            "condition": "alarm_1_on_host and alarm_2_on_instance and host_contains_instance"
          }
        }
      ],
      "definitions": {
        "relationships": [
          {
            "relationship": {
              "relationship_type": "on",
              "source": "alarm_1",
              "target": "host",
              "template_id": "alarm_1_on_host"
            }
          },
          {
            "relationship": {
              "relationship_type": "on",
              "source": "alarm_2",
              "target": "instance",
              "template_id": "alarm_2_on_instance"
            }
          },
          {
            "relationship": {
              "relationship_type": "contains",
              "source": "host",
              "target": "instance",
              "template_id": "host_contains_instance"
            }
          }
        ],
        "entities": [
          {
            "entity": {
              "vitrage_category": "ALARM",
              "vitrage_type": "nagios",
              "name": "check_libvirtd",
              "template_id": "alarm_1"
            }
          },
          {
            "entity": {
              "vitrage_category": "RESOURCE",
              "vitrage_type": "nova.host",
              "template_id": "host"
            }
          },
          {
            "entity": {
              "vitrage_category": "RESOURCE",
              "vitrage_type": "nova.instance",
              "template_id": "instance"
            }
          },
          {
            "entity": {
              "vitrage_category": "ALARM",
              "vitrage_type": "vitrage",
              "name": "exploding_world",
              "template_id": "alarm_2"
            }
          }
        ]
      },
      "metadata": {
        "name": "first_deduced_alarm_ever"
    }

Event Post
^^^^^^^^^^
Post an event to Vitrage message queue, to be consumed by a datasource driver.

POST /v1/event/
~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json
-  User-Agent (String)
-  Content-Type (String): application/json

Path Parameters
===============

None.

Query Parameters
================

None.

Request Body
============

An event to be posted. Will contain the following fields:

- time: a timestamp of the event. In case of a monitor event, should specify when the fault has occurred.
- type: the type of the event.
- details: a key-value map of metadata.

A dict of some potential details, copied from the Doctor SB API reference:

- hostname: the hostname on which the event occurred.
- source: the display name of reporter of this event. This is not limited to monitor, other entity can be specified such as 'KVM'.
- cause: description of the cause of this event which could be different from the type of this event.
- severity: the severity of this event set by the monitor.
- status: the status of target object in which error occurred.
- monitorID: the ID of the monitor sending this event.
- monitorEventID: the ID of the event in the monitor. This can be used by operator while tracking the monitor log.
- relatedTo: the array of IDs which related to this event.

Request Examples
================

::

    POST /v1/event/
    Host: 135.248.18.122:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    Content-Type: application/json
    Accept: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7


::

    {
        'event': {
            'time': '2016-04-12T08:00:00',
            'type': 'compute.host.down',
            'details': {
                'hostname': 'compute-1',
                'source': 'sample_monitor',
                'cause': 'link-down',
                'severity': 'critical',
                'status': 'down',
                'monitor_id': 'monitor-1',
                'monitor_event_id': '123',
            }
        }
    }



Response Status code
====================

-  200 - OK
-  400 - Bad request

Response Body
=============

Returns an empty response body if the request was OK.
Otherwise returns a detailed error message (e.g. 'missing time parameter').

Resource list
^^^^^^^^^^^^^
List the resources with specified type or all the resources.

GET /v1/resources/
~~~~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json
-  User-Agent (String)
-  Content-Type (String): application/json

Path Parameters
===============

None.

Query Parameters
================

* resource_type - (string, optional) the type of resource, defaults to return all resources.
* all_tenants - (boolean, optional) shows the resources of all tenants (in case the user has the permissions).

Request Body
============

None.

Request Examples
================

::

    GET /v1/resources/?all_tenants=False&resource_type=nova.host
    Host: 135.248.18.122:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    Content-Type: application/json
    Accept: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7


Response Status code
====================

-  200 - OK
-  404 - Bad request

Response Body
=============

Returns a list with all the resources requested.

Response Examples
=================

::

  [
    {
      "vitrage_id": "6b4a4272-0fef-4b35-9c3c-98bc8e71cd38",
      "vitrage_aggregated_state": "AVAILABLE",
      "state": "available",
      "vitrage_type": "nova.host",
      "id": "cloud",
      "metadata": {
        "name": "cloud",
        "update_timestamp": "2017-04-24 04:27:47.501777+00:00"
      }
    }
  ]


Resource show
^^^^^^^^^^^^^
Show the details of specified resource.

GET /v1/resources/[vitrage_id]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Headers
=======

-  X-Auth-Token (string, required) - Keystone auth token
-  Accept (string) - application/json
-  User-Agent (String)
-  Content-Type (String): application/json

Path Parameters
===============

- vitrage_id.

Query Parameters
================

None.

Request Body
============

None.

Request Examples
================

::

    GET /v1/resources/`<vitrage_id>`
    Host: 127.0.0.1:8999
    User-Agent: keystoneauth1/2.3.0 python-requests/2.9.1 CPython/2.7.6
    Accept: application/json
    X-Auth-Token: 2b8882ba2ec44295bf300aecb2caa4f7

Response Status code
====================

-  200 - OK
-  404 - Bad request

Response Body
=============

Returns details of the requested resource.

Response Examples
=================

::

    {
      "vitrage_category": "RESOURCE",
      "vitrage_is_placeholder": false,
      "vitrage_is_deleted": false,
      "name": "vm-1",
      "update_timestamp": "2015-12-01T12:46:41Z",
      "state": "ACTIVE",
      "project_id": "0683517e1e354d2ba25cba6937f44e79",
      "vitrage_type": "nova.instance",
      "id": "dc35fa2f-4515-1653-ef6b-03b471bb395b",
      "vitrage_id": "11680c27-86a2-41a7-89db-863e68b1c2c9"
    }
