from typing import List
from yaramo.model import Node, Edge, Signal, Topology, SignalFunction, SignalKind, DbrefGeoNode
import re



class CLI:

    def __init__(self) -> None:
        self.topology = Topology()        

    def __find_node_with_identifier(self,_identifier):
        for _node in self.topology.nodes.values():
            if _node.name == _identifier:
                return _node
        return None


    def __find_edge_by_nodes(self,_node_a: Node, _node_b: Node):
        for _edge in self.topology.edges.values():
            if _edge.is_node_connected(_node_a) and _edge.is_node_connected(_node_b):
                return _edge
        return None

    def run(self):
        print("Welcome to the PlanPro Generator")
        print("Usage:")
        print("Create a node (end or point): node <id> <x> <y> [description]")
        print("Create an edge: edge <node id a> <node id b> [coords x1,y1 [x2,y2 ...]]")
        print("Create a signal: signal <node id from> <node id to> <distance to node from> <function> <kind> [<name>]")
        print(f"\tWhere <function> is one of {[member.name for member in SignalFunction]}")
        print(f"\t and where <kind> is one of {[member.name for member in SignalKind]}")
        print("Generate and exit CLI: exit")
        print()

        self.topology.name = input("Please enter the file name (without suffix): ")

        command = ""
        while command != "exit":
            command = input("#: ").strip()

            if command == "":
                continue
            elif re.match(r'^node [a-zA-Z_0-9]+ -?\d+(\.\d+)? -?\d+(\.\d+)?( [a-zA-Z_0-9]+)?$', command):
                splits = command.split(" ")
                identifier = splits[1]
                x = float(splits[2]) + 4533770.0
                y = float(splits[3]) + 5625780.0
                desc = ""
                if len(splits) > 4:
                    desc = splits[4]

                if self.__find_node_with_identifier(identifier) is None:
                    node = Node(name=identifier)
                    node.geo_node = DbrefGeoNode(x, y)
                    self.topology.nodes[node.uuid] = node
                else:
                    print(f"Node with id {identifier} already exists. Please use a different id.")
            elif re.match(r'edge [a-zA-Z_0-9]+ [a-zA-Z_0-9]+( coords (-?\d+(\.\d+)?,-?\d+(\.\d+)?)+)?', command):
                splits = command.split(" ")
                node_a_id = splits[1]
                node_b_id = splits[2]

                node_a = self.__find_node_with_identifier(node_a_id)
                node_b = self.__find_node_with_identifier(node_b_id)

                if node_a is None:
                    print(f"Node with ID {node_a_id} does not exists. Please create it first.")
                elif node_b is None:
                    print(f"Node with ID {node_b_id} does not exists. Please create it first.")
                else:
                    if self.__find_edge_by_nodes(node_a, node_b) is None:
                        edge = Edge(node_a, node_b)
                        node_a.connected_nodes.append(node_b)
                        node_b.connected_nodes.append(node_a)
                        edge.update_length()
                        self.topology.edges[edge.uuid] =edge

                        # Intermediate nodes
                        for i in range(4, len(splits)):
                            intermediate_node = splits[i]
                            x = float(intermediate_node.split(",")[0]) + 4533770.0
                            y = float(intermediate_node.split(",")[1]) + 5625780.0
                            geo_node = DbrefGeoNode(x, y)
                            edge.intermediate_geo_nodes.append(geo_node)
                    else:
                        print(f"The nodes {node_a_id} and {node_b_id} are already connected.")
            elif re.match(r'signal [a-zA-Z_0-9]+ [a-zA-Z_0-9]+ -?\d+(\.\d+)? .+ \S+( \S)?', command):
                splits = command.split(" ")
                node_a_id = splits[1]
                node_b_id = splits[2]
                distance = float(splits[3])
                function = splits[4]
                kind = splits[5]
                element_name = None
                if len(splits) > 6:
                    element_name = splits[6]

                if not SignalFunction[function]:
                    print(f"Function {function} is not supported. Choose any from: {[member.name for member in SignalFunction]}")
                    continue
                if not SignalKind[kind]:
                    print(f"Kind {kind} is not supported. Choose any from: {[member.name for member in SignalKind]}")
                    continue

                node_a = self.__find_node_with_identifier(node_a_id)
                node_b = self.__find_node_with_identifier(node_b_id)
                if node_a is None:
                    print(f"Node with ID {node_a_id} does not exists. Please create it first.")
                    continue
                if node_b is None:
                    print(f"Node with ID {node_b_id} does not exists. Please create it first.")
                    continue

                edge = self.__find_edge_by_nodes(node_a, node_b)
                if edge is None:
                    print(f"The nodes {node_a_id} and {node_b_id} are not connected. Please connect them first.")
                    continue

                if distance > edge.length:
                    print("Distance is greater than edge length. Choose a smaller distance.")
                    continue

                effective_direction = "in"
                if edge.node_b.uuid == node_a_id and edge.node_a.uuid == node_b_id:
                    effective_direction = "gegen"

                signal = Signal(edge, distance, effective_direction, function, kind, name=element_name)
                self.topology.signals[signal.uuid] = signal
            elif command != "exit":
                print("Command does not exists")

        print("Bye.")
        return

