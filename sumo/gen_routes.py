import random
import sumolib
from xml.dom import minidom
from termcolor import colored

complete_net_path = "./data/porto_clean_laterals.net.xml"   # Netfile with more than the VCI
route_path = "./data/porto.rou.xml"                         # output
od_path = "./data/porto.od"                             # OD file 
reroute_path = "./data/reroute.add.xml"
mandatory_edge_1 = "405899851"
mandatory_edge_2 = "478882416"

def gen_root():
    return minidom.Document()

def get_random(l: list): 
    return l[random.randrange(len(l))]
    
def gen_vehicle(id : str):
    vehicle = doc.createElement("vehicle")
    vehicle.setAttribute("id", str(id))
    vehicle.setAttribute("depart", "{:.2f}".format(id))
    return vehicle

def gen_reroute_hash(edges, h):
    """
    Creates hashmap containing the rerouter edges.
    """
    keys = h.keys()
    
    for edge in edges: 
        if edge in keys: 
            return h

    h[edges[0]] = edges[-1]
    return h

def gen_reroute(h):
    doc = gen_root()
    additionals = doc.createElement("additionals")
    
    with open(reroute_path, 'w') as reroute_file:
        for i, key in enumerate(h.keys()):
            rerouter = doc.createElement("rerouter")
            rerouter.setAttribute("id", f"rerouter_{i}")
            rerouter.setAttribute("edges", f"{key}")
            interval = doc.createElement("interval")
            interval.setAttribute("end", "1e6")
            destProbReroute = doc.createElement("destProbReroute")
            destProbReroute.setAttribute("id", f"{h[key]}")
            interval.appendChild(destProbReroute)
            rerouter.appendChild(interval)
            additionals.appendChild(rerouter)

            rerouter = doc.createElement("rerouter")
            rerouter.setAttribute("id", f"rerouter_{i*2+1}")
            rerouter.setAttribute("edges", f"{h[key]}")
            interval = doc.createElement("interval")
            interval.setAttribute("end", "1e6")
            destProbReroute = doc.createElement("destProbReroute")
            destProbReroute.setAttribute("id", f"{key}")
            interval.appendChild(destProbReroute)
            rerouter.appendChild(interval)
            additionals.appendChild(rerouter)
    
        doc.appendChild(additionals)
        doc.writexml(reroute_file, indent='\t', addindent='\t', newl='\n', encoding="UTF-8")

def gen_route(net, nodes):
    route_path = ""
    # Get edges from nodes 
    outgoing_edge = net.getNode(nodes[0]).getOutgoing()
    outgoing_edge_random = get_random(outgoing_edge)
    incoming_edge = net.getNode(nodes[1]).getIncoming()
    incoming_edge_random = get_random(incoming_edge)
    
    path_edges = net.getFastestPath(outgoing_edge_random, incoming_edge_random)[0]

    # Get path 
    for edge in path_edges:
        route_path += edge.getID() + " "

    route = doc.createElement("route")
    route.setAttribute("edges", route_path)
    return [route, route_path.split(" ")[:-1]]

def strip_line(line): 
    line = line.replace("\n", "")
    line = line.replace("\r", "")
    line = line.strip()
    return line

def find_od_start(od_list): 
    """"
    Finds where the start and end points are defined in the od file. 
    This is only possible if there's a comment "* start" right before the start of the origin and destination points. 
    """
    for i, v in enumerate(od_list):
        if v == "* start":
            return i + 1
    return -1


def read_od(): 
    """
    Read OD FiLe
    """
    od_lines = open(od_path, "r").readlines()
    od = list(map(strip_line, od_lines))
    od = od[find_od_start(od):]
    return list(map(lambda x: x.split(), od))


if '__main__' == __name__:
    doc = gen_root()
    routes = doc.createElement("routes")
    net = sumolib.net.readNet(complete_net_path)
    od_file = read_od()
    # hash to build the circular file
    hash_reroute = {}

    for id in range(500):
        try:
            nodes = random.sample(od_file, 1)[0]
            [route, route_list] = gen_route(net, nodes)
            hash_reroute = gen_reroute_hash(route_list, hash_reroute)
        except Exception as e: 
            print(colored(f"[ERR] Not possible generate path, skipping...:: {e}", "yellow"))
            continue

        vehicle = gen_vehicle(id)
        vehicle.appendChild(route)
        routes.appendChild(vehicle)

    doc.appendChild(routes)

    gen_reroute(hash_reroute)

    with open(route_path, "w") as f:
        doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="UTF-8")
