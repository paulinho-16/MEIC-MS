from ..sumo.utils import read_routes_file
from collections import defaultdict
import pandas as pd

class Nodes:
    def __init__(self, id_, flow = 0, sensor = -1) -> None:
        self.children = []
        self.id = id_
        self.sensor = sensor
        self.flow = flow


edges = set([])
sensor_edges  = set([])
od_sensors = defaultdict(list)  # {od_in_out: [sensor_id]}, maps what sensors are connected to an edge
sensor_real_data = defaultdict(list)  # {sensor_id + "_" + direction: [numCars]}, maps the numCars of each sensor across time
nodes = set([])
od_num_cars = defaultdict(list) # {od: [numCars1, numCars2,...]}

def get_detectors():
    with open ("./data/detectors.add.xml") as f:
        for line in f:
            splitted = line.strip().split("\"")
            if len(splitted) >= 2:
                sensor_id = splitted[1]
                sensor_edge = splitted[3].split("_")[0]

                # Attribute the direction of a sensor. 
                sensor_splitted = sensor_id.split("_")
                if sensor_splitted[1][0] == '0':
                    sensor_id = sensor_splitted[0] + "_C"
                elif sensor_splitted[1][0] == '1':
                    sensor_id = sensor_splitted[0] + "_D"

                sensor_edges.add((sensor_id, sensor_edge))

def get_od_value(od):
    m = 0 
    # Get the total sample of numCars
    total_time = len(sensor_real_data[od_sensors[od][0]])
    # For each time stamp get the numCars
    for i in range(total_time):
        for sensor_id in od_sensors[od]:
            m = min(m, sensor_real_data[sensor_id][i])
        m = 0
        od_num_cars[od].append(m)

if __name__ == "__main__":
    routes = read_routes_file()
    get_detectors()
    for od, route in routes.items():
        for (id, edge) in sensor_edges:
            if edge in route:
                od_sensors[od].append(id)

    real_data = pd.read_csv("./data/AEDL2013_2015/1P2015AEDL_MorningRushHour.csv", sep=",")

    for _, real_row in real_data.iterrows():
        sensor_real_data[f"{real_row['EQUIPMENTID']}_{real_row['LANE_BUNDLE_DIRECTION']}"].append(real_row["TOTAL_VOLUME"])

    
    for od in routes.keys():
        get_od_value(od)
    
    gen_routes(od_num_cars, routes) # TODO: mudar gen_routes por causa do primeiro parámetro