import networkx as nx


class EdgeValidator:
    @staticmethod
    def add_edge(source_node, target_node, graph: nx.DiGraph, decision: str = None):
        source_node_dict = source_node[1]

        if "type" in source_node_dict and source_node_dict["type"] == "start":
            EdgeValidator._validate_start_node(source_node_dict, target_node, graph)
        elif "type" in source_node_dict and source_node_dict["type"] == "message":
            EdgeValidator._validate_message_node(source_node_dict, target_node, graph)
        elif "type" in source_node_dict and source_node_dict["type"] == "condition":
            EdgeValidator._validate_condition_node(source_node_dict, target_node, graph, decision)
        elif "type" in source_node_dict and source_node_dict["type"] == "end":
            EdgeValidator._validate_end_node(source_node_dict, target_node, graph)

    @staticmethod
    def _validate_start_node(source_node, target_node, graph: nx.DiGraph):
        if "outgoing_node" in source_node and source_node["outgoing_node"] is not None:
            raise ValueError("StartNode can have only one outgoing edge")
        elif EdgeValidator._count_incoming_edges(graph, source_node["id"]) > 0:
            raise ValueError("StartNode cannot have incoming edges")

    @staticmethod
    def _validate_message_node(source_node, target_node, graph: nx.DiGraph):
        if "outgoing_node" in source_node and source_node["outgoing_node"] is not None:
            raise ValueError("MessageNode can have only one outgoing edge")

    @staticmethod
    def _validate_condition_node(source_node, target_node, graph: nx.DiGraph, decision: str = None):
        if decision:
            if source_node.get(decision):
                raise ValueError("ConditionNode cannot have more than one yes or no node")

    @staticmethod
    def _validate_end_node(source_node, target_node, graph: nx.DiGraph):
        if graph.out_degree(source_node["id"]) > 0:
            raise ValueError("EndNode cannot have outgoing edges")

    @staticmethod
    def _count_incoming_edges(graph: nx.DiGraph, node_id):
        count = 0
        for _, edge_target in graph.in_edges([node_id]):
            count += 1
        return count
