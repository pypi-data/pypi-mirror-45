===============================
Template Validation Status Code
===============================

Overview
--------
Status codes are received after executing Vitrage template validation.
The code describes the Vitrage template status: if the template is correct, the status code is 0. Otherwise the code describes the error in the template itself.

Description
-----------
The following describes all the possible status code and their messages:

+------------------+---------------------------------------------------------+-------------------------------+
| code             | message                                                 | Test Type                     |
+==================+=========================================================+===============================+
| 0                | Template validation is OK                               | content and syntax            |
+------------------+---------------------------------------------------------+-------------------------------+
| 1                | template_id field contains incorrect string value       | content                       |
+------------------+---------------------------------------------------------+-------------------------------+
| 2                | Duplicate template_id definition                        | content                       |
+------------------+---------------------------------------------------------+-------------------------------+
| 3                | template_id does not appear in the definition block     | content                       |
+------------------+---------------------------------------------------------+-------------------------------+
| 4                | Syntax error: [error message]                           | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 20               | definitions section must contain entities field         | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 21               | definitions section is a mandatory section              | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 41               | Entity definition must contain template_id field        | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 42               | Entity definition must contain category field           | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 43               | At least one entity must be defined                     | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 45               | Invalid entity category. Category must be from          | syntax                        |
|                  | types: [entities_categories]                            |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 46               | Entity field is required                                | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 60               | metadata section must contain id field                  | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 62               | metadata is a mandatory section                         | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 80               | scenarios is a mandatory section                        | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 81               | At least one scenario must be defined                   | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 82               | scenario field is required                              | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 83               | Entity definition must contain condition field          | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 84               | Entity definition must contain actions field            | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 85               | Failed to convert condition                             | content                       |
+------------------+---------------------------------------------------------+-------------------------------+
| 100              | Invalid relation type. Relation type must be from types:| syntax                        |
|                  | [relation_types]                                        |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 101              | Relationship field is required                          | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 102              | Relationship definition must contain source field       | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 103              | Relationship definition must contain target field       | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 104              | Relationship definition must contain template_id field  | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 120              | Invalid action type. Action type must be from types:    | content                       |
|                  | [action_types]                                          |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 121              | At least one action must be defined                     | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 122              | Action field is required                                | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 123              | Relationship definition must contain action_type field  | syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 124              | Relationship definition must contain action_target field| syntax                        |
+------------------+---------------------------------------------------------+-------------------------------+
| 125              | raise_alarm action must contain alarm_name field in     | content                       |
|                  | properties block                                        |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 126              | raise_alarm action must contain severity field in       | content                       |
|                  | properties block                                        |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 127              | raise_alarm action must contain target field in         | content                       |
|                  | target_action block                                     |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 128              | set_state action must contain state field in properties | content                       |
|                  | block                                                   |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 129              | set_state action must contain target field in           | content                       |
|                  | target_action block                                     |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 130              | add_causal_relationship action must contain target and  | content                       |
|                  | source field in target_action block                     |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 131              | mark_down action must contain target field in           | content                       |
|                  | target_action block.                                    |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 132              | add_causal_relationship action requires action_target to| content                       |
|                  | be ALARM                                                |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 133              | execute_mistral action must contain workflow field in   | content                       |
|                  | properties block                                        |                               |
+------------------+---------------------------------------------------------+-------------------------------+
| 134              | condition can not contain only 'not' clauses            | content                       |
+------------------+---------------------------------------------------------+-------------------------------+
| 135              | condition must contain a common entity for all 'or'     | content                       |
|                  | clauses                                                 |                               |
+------------------+---------------------------------------------------------+-------------------------------+
