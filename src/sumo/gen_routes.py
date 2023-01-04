from xml.dom import minidom
from termcolor import colored

from .utils import read_routes_file

complete_net_path = "./data/vci.net.xml"     # Netfile with complete VCI road network
route_path = "./data/vci.rou.xml"            # output
reroute_path = "./data/reroute.add.xml"
mandatory_edge_1 = "405899851"
mandatory_edge_2 = "478882411"

def gen_root():
    return minidom.Document()
    
def gen_vehicle(id : str, doc):
    vehicle = doc.createElement("vehicle")
    vehicle.setAttribute("id", str(id))
    vehicle.setAttribute("depart", "{:.2f}".format(id))
    return vehicle
        
def create_rerouter_element(origin, destination, index, additionals, doc): 
    rerouter = doc.createElement("rerouter")
    rerouter.setAttribute("id", f"rerouter_{index}")
    rerouter.setAttribute("edges", f"{origin}")
    interval = doc.createElement("interval")
    interval.setAttribute("end", "1e6")
    destProbReroute = doc.createElement("destProbReroute")
    destProbReroute.setAttribute("id", f"{destination}")
    interval.appendChild(destProbReroute)
    rerouter.appendChild(interval)
    additionals.appendChild(rerouter)

def gen_route(edges, doc):
    route = doc.createElement("route")
    route.setAttribute("edges", edges)
    return route

def gen_routes(od_values, routes):
    doc = gen_root()
    routes_element = doc.createElement("routes")
    vehicle_id = 0

    for orig_dest, num_cars_list in od_values.items():
        route = routes[orig_dest]

        for num_cars in num_cars_list:
            num_cars = int(num_cars)
            depart_interval = 300/num_cars
            for _ in range(num_cars):
                vehicle = gen_vehicle(vehicle_id, doc)
                route_element = gen_route(route, doc)
                vehicle.appendChild(route_element)
                routes_element.appendChild(vehicle)
                vehicle_id += 1

    doc.appendChild(routes_element)

    with open(route_path, "w") as f:
        doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="UTF-8")

if '__main__' == __name__:
    routes = read_routes_file()
    od_values = [0 for _ in range(1000)]
    gen_routes(od_values, routes)
