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

def read_od(): 
    """
    Read OD FiLe
    """
    od_lines = open(od_path, "r").readlines()
    od = list(map(strip_line, od_lines))
    return list(map(lambda x: x.split(), od))

def read_od_dict() -> dict[str, int]: 
    """Reads the od file

    Returns:
        dict[str, str]: Keys as the od_minute (i.e., origin_destination_timestamp), the values as the number of cars
    """
    data = {}
    od_list = read_od()

    minute = 0
    current_od = None
    for element in od_list:
        od, num_cars = element
        if current_od != od:
            minute = 0
            current_od = od

        key = od + '_' + str(minute)
        data[key] = int(num_cars)
        minute += 300

    return data
    
def read_routes_file() -> dict[str, str]:
    """Read the routes file

    Returns:
        dict: The dictionary has the form {origin_destination: "edge1 edge2,...", ...}
    """
    f = open(route_txt, "r")
    data = {}
    for line in f.readlines():
        [nodes, values] = line.split("::")
        key = "_".join(list(nodes.strip().split()))
        data[key] = values.strip()

    f.close()
    return data

if __name__ == '__main__':
    print(read_od())