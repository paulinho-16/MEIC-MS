"""This file generates the routes mapped. 
For each od the path is prestabilished and saved in ROUTE_MAP_FILE.
"""

import sumolib
from configparser import ConfigParser, ExtendedInterpolation
import logging


logging.basicConfig(level=logging.INFO)
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("./src/config.ini")


def get_routes(in_vci_edges: list, out_vci_edges: list) -> list[str]:
    """ Generates a routes array. Where the content is the a string of edges.

    Args:
        ins (list): Entry edges of the VCI 
        outs (list): Exit edges of the VCI

    Returns:
        list[str]: ["edge1 edge2 edge3", "edge4 edge5 edge6"]
    """
    routes = []
    for ing in in_vci_edges:
        for outg in out_vci_edges:
            path_edges = complete_net.getShortestPath(ing, outg)[0]
            if path_edges:
                path_edges_string = " ".join(
                    list(map(lambda x: x.getID(), path_edges)))
                routes.append(path_edges_string)

    return routes


def get_entry_exit_nodes(nodes) -> tuple[list, list]:
    """Gets all the entry and exit nodes from all the nodes in a network. 

    Args:
        nodes (list): All the nodes in the network. 
    """
    entry_nodes: list = []
    exit_nodes: list = []

    for node in nodes:
        if not node.getIncoming() and node.getOutgoing():
            entry_nodes.append(node.getID())
        elif not node.getOutgoing() and node.getIncoming():
            exit_nodes.append(node.getID())
    return (entry_nodes, exit_nodes)


def gen_route_file(nodes: list) -> None:
    """Generates the route file containing the path od edges for each od. 

    Args:
        nodes (list): The list of nodes
        values (list): 
    """
    [entry_nodes, exit_nodes] = get_entry_exit_nodes(nodes)

    routes_file = open(config["data"]["ROUTE_MAP_FILE"], '+w')
    for origin in entry_nodes:
        for destination in exit_nodes:
            in_vci_edges: list = clean_net.getNode(origin).getOutgoing()
            out_vci_edges: list = clean_net.getNode(destination).getIncoming()
            routes: list[str] = get_routes(in_vci_edges, out_vci_edges)
            if origin != destination and routes:
                route = routes[0]
                routes_file.write(f"{origin} {destination} :: {route}\n")

    routes_file.close()


if '__main__' == __name__:
    clean_net = sumolib.net.readNet(config["data"]["CLEAN_NET_FILE"])
    complete_net = sumolib.net.readNet(config["data"]["COMPLETE_NET_FILE"])
    nodes = clean_net.getNodes()
    logging.info("Generating route mapping...")
    gen_route_file(nodes)
    logging.info("Route map file generated with success!")
