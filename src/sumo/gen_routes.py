"""Generates SUMO .rou.xml file.

Returns:
    _type_: _description_
"""

from xml.dom import minidom
from tqdm import tqdm
from .utils import read_routes_file, read_od_dict

route_path = "./data/vci.rou.xml"            # output


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

def gen_routes(od_volume: dict[str, int], od_route: dict[str, str]):
    doc = gen_root()
    routes_element = doc.createElement("routes")
    vehicle_id = 0
    vehicle_list = [] 

    for orig_dest, num_cars_list in od_values.items():
        route = routes[orig_dest]
        depart = 0
        for num_cars in num_cars_list:
            if num_cars == 0:
                continue
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
    od_routes: dict[str, str] = read_routes_file()
    od_volume: dict[str, int] = read_od_dict()
    gen_routes(od_volume, od_routes)
