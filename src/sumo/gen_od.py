import sumolib
from .utils import get_random_from_list

taz_filepath = "./data/vci.taz.xml"
save_path = "./data/vci.od"
routes_map = "./data/routes_map.txt"
complete_net_file = "./data/vci.net.xml"
clean_net_file = "./data/porto_clean.net.xml"

def get_routes(ins: list, outs: list) -> list:
    """
    Generates a routes array. Where the content is the a string of edges.

    Parameters
    ----------
    ins: entry edges of the VCI 
    outs: exit edges of the VCI

    Return
    ------
    routes: list -> ["edge1 edge2 edge3", "edge4 edge5 edge6"]
    """
    routes = []
    for ing in ins:
        for outg in outs:
            path_edges = complete_net.getShortestPath(ing, outg)[0]
            if path_edges:
                path_edges_string = " ".join(list(map(lambda x: x.getID(), path_edges)))
                routes.append(path_edges_string)

    return routes


def get_entry_exit_nodes(nodes):
    """
    Gets all the entry and exit nodes from all the nodes in a network. 

    Parameters
    ----------
    nodes: list -> All the nodes in the network. 
    """
    entry_nodes = []
    exit_nodes = []
    
    for node in nodes:
        if not node.getIncoming() and node.getOutgoing():
            entry_nodes.append(node.getID())
        elif not node.getOutgoing() and node.getIncoming():
            exit_nodes.append(node.getID())
    return entry_nodes, exit_nodes


def generate_od(nodes: list, values: list) -> None:
    """
    Generate the OD at the first time. 

    Parameters
    ----------
    nodes: list -> Nodes in the network 
    values: list -> The number of cars for each entry 
    """
    [entry_nodes, exit_nodes] = get_entry_exit_nodes(nodes)
    routes_file = open(routes_map, '+w')
    with open(save_path, 'w') as od_file:
        i = 0
        for origin in entry_nodes:
            for destination in exit_nodes:
                routes = get_routes(clean_net.getNode(origin).getOutgoing(), clean_net.getNode(destination).getIncoming())
                if origin != destination and routes:
                    od_file.write(f"\t\t{origin}_{destination}   {values[i]}\n")
                    route = get_random_from_list(routes)
                    routes_file.write(f"{origin} {destination} :: {route}\n")
                    i += 1

    routes_file.close()

def generate_od2(values: dict) -> None:
    with open(save_path, 'w') as od_file:
        for orig_dest, num_cars in values.items():
            od_file.write(f"\t\t{orig_dest}   {num_cars}\n")


if '__main__' == __name__:
    clean_net = sumolib.net.readNet(clean_net_file)
    complete_net = sumolib.net.readNet(complete_net_file)
    nodes = clean_net.getNodes()
    edges = clean_net.getEdges()
    
    od_values = [0 for _ in range(1000)]
    generate_od(nodes, od_values)