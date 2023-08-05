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

import networkx as nx
from networkx.readwrite import json_graph
from pecan import rest

from vitrage.datasources import OPENSTACK_CLUSTER


class RootRestController(rest.RestController):

    @staticmethod
    def as_tree(graph, root=OPENSTACK_CLUSTER, reverse=False):
        linked_graph = json_graph.node_link_graph(graph)
        if 0 == nx.number_of_nodes(linked_graph):
            return {}
        if reverse:
            linked_graph = linked_graph.reverse()
        return json_graph.tree_data(linked_graph, root=root)
