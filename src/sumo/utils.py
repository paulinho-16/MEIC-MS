import random

od_path = "./data/vci.od"
route_txt = "./data/routes_map.txt"

def get_random_from_list(l: int): 
    return l[random.randrange(len(l))]

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

def read_od(od_path=od_path):
    """
    Read OD FiLe
    """
    od_lines = open(od_path, "r").readlines()
    od = list(map(strip_line, od_lines))
    od = od[find_od_start(od):]
    return list(map(lambda x: x.split(), od))

def read_od_dict(od_path=od_path): 
    data = {}
    od_list = read_od(od_path)

    for element in od_list:
        origin, destination, num_cars = element
        key = origin + '_' + destination
        data[key] = num_cars

    return data

def read_routes_file():
    f = open(route_txt, "r")
    data = {}
    for line in f.readlines():
        [nodes, values] = line.split("::")
        key = "_".join(list(nodes.strip().split()))
        data[key] = values.strip()

    f.close()
    return data