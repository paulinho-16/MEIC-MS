"""Generates SUMO .rou.xml file.
"""

from configparser import ConfigParser, ExtendedInterpolation
import logging 
from xml.dom import minidom
from .utils import read_routes_file, read_od_dict


logging.basicConfig(level=logging.INFO)
config: ConfigParser = ConfigParser(interpolation=ExtendedInterpolation())
config.read("./src/config.ini")


def gen_root() -> minidom.Document:
    return minidom.Document()

def gen_vehicle(id: int, depart: int, doc: minidom.Document) -> minidom.Element:
    """Generates the xml for each vechile.

    Args:
        id (str): Vehicle id 
        depart (int): Time of departure
        doc (minidom.Document): The xml document

    Returns: 
        Element: the xml element of the vehicle.        
    """
    vehicle = doc.createElement("vehicle")
    vehicle.setAttribute("id", str(id))
    vehicle.setAttribute("depart", "{:.2f}".format(depart))
    return vehicle

        
def gen_route(edges: str, doc: minidom.Document) -> minidom.Element:
    """Generates the route xml element

    Args:
        edges (str): The edges id separated by space
        doc (minidom.Document): The xml document

    Returns:
        minidom.Element: The route xml element
    """
    route = doc.createElement("route")
    route.setAttribute("edges", edges)
    return route

def gen_routes(od_volume: dict[str, int], od_route: dict[str, str]):
    """Generates the xml with the routes of each vehicle.

    Args:
        od_volume (dict[str, int]): maps the ods (i.e., origin_destination) to the number of vehicles.
        od_route (dict[str, str]): maps the ods  (i.e., origin_destination) to the routes as strings.
    """
    doc: minidom.Document = gen_root()
    routes_element: minidom.Element = doc.createElement("routes")
    vehicle_id: int = 0
    vehicle_list: list = [] 

    for orig_dest, num_cars in od_volume.items():
        route: str = od_route[orig_dest]
        depart: int = 0
        depart_interval: int = 300 // num_cars
        for _ in range(num_cars):
            vehicle: minidom.Element = gen_vehicle(vehicle_id, depart, doc)
            route_element: minidom.Element = gen_route(route, doc)
            vehicle.appendChild(route_element)
            vehicle_list.append((depart, vehicle)) # vehicle_list.put((depart, PQEntry(vehicle)))
            vehicle_id += 1
            depart += depart_interval

    print(f"Generated {vehicle_id + 1} vehicles. Now adding vehicles to the routes file")

    vehicle_list: list = sorted(vehicle_list, key=lambda x: x[0])
    for (depart, vehicle) in vehicle_list:
        routes_element.appendChild(vehicle)

    doc.appendChild(routes_element)

    with open(config["data"]["SUMO_ROUTE_FILE"], "w") as f:
        doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="UTF-8")
    


if '__main__' == __name__:
    od_routes: dict[str, str] = read_routes_file()  # maps ods (i.e., origin_destination) to routes (edges separated by space).
    od_volume: dict[str, int] = read_od_dict() # maps ods 
    gen_routes(od_volume, od_routes)
