from xml.dom import minidom
from termcolor import colored
from queue import PriorityQueue
from tqdm import tqdm
from .utils import read_routes_file

complete_net_path = "./data/vci.net.xml"     # Netfile with complete VCI road network
route_path = "./data/vci.rou.xml"            # output
reroute_path = "./data/reroute.add.xml"
mandatory_edge_1 = "405899851"
mandatory_edge_2 = "478882411"

class PQEntry:
    def __init__(self, value):
        self.value = value

    def __cmp__(self, other):
         return cmp(float(self.value.getAttribute("depart")), float(other.value.getAttribute("depart")))

    def __lt__(self, other):
        return float(self.value.getAttribute("depart")) < float(other.value.getAttribute("depart"))

def gen_root():
    return minidom.Document()
    
def gen_vehicle(id: str, depart: int, doc):
    vehicle = doc.createElement("vehicle")
    vehicle.setAttribute("id", str(id))
    vehicle.setAttribute("depart", "{:.2f}".format(depart))
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
    vehicle_list = [] # PriorityQueue()

    for orig_dest, num_cars_list in tqdm(od_values.items()):
        route = routes[orig_dest]
        depart = 0
        for num_cars in num_cars_list:
            num_cars = int(num_cars)
            depart_interval = 300 // num_cars
            for _ in range(num_cars):
                vehicle = gen_vehicle(vehicle_id, depart, doc)
                route_element = gen_route(route, doc)
                vehicle.appendChild(route_element)
                vehicle_list.append((depart, vehicle)) # vehicle_list.put((depart, PQEntry(vehicle)))
                vehicle_id += 1
                depart += depart_interval

    print(f"Generated {vehicle_id + 1} vehicles. Now adding vehicles to the routes file")

    # for (depart, vehicle) in vehicle_list.queue:
    #     routes_element.appendChild(vehicle.value)
    vehicle_list = sorted(vehicle_list, key=lambda x: x[0])
    for (depart, vehicle) in vehicle_list:
        routes_element.appendChild(vehicle)

    doc.appendChild(routes_element)

    with open(route_path, "w") as f:
        doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="UTF-8")
    
    print("written")

if '__main__' == __name__:
    routes = read_routes_file()
    od_values = [0 for _ in range(1000)]
    gen_routes(od_values, routes)
