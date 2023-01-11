import pandas as pd
from collections import defaultdict

from ..sumo.utils import read_routes_file
from ..sumo.gen_routes import gen_routes
from ..dataProcessing.calibration import evaluate


edges = set([])
sensor_edges  = set([])
od_sensors = defaultdict(list)  # {od_in_out: [sensor_id]}, maps what sensors are connected to an edge
sensor_real_data = defaultdict(list)  # {sensor_id + "_" + direction: [numCars]}, maps the numCars of each sensor across time
nodes = set([])
od_num_cars = defaultdict(list) # {od: [numCars1, numCars2,...]}, where the [numCars1, numCars2, ...] is the number of cars for each time. 
od_path = "./data/vci.od"


def get_detectors():
    with open ("./data/detectors.add.xml") as f:
        for line in f:
            splitted = line.strip().split("\"")
            if len(splitted) >= 2:
                sensor_id = splitted[1]
                sensor_edge = splitted[3].split("_")[0]

                # Attribute the direction of a sensor
                sensor_splitted = sensor_id.split("_")
                if sensor_splitted[1][0] == '0':
                    sensor_id = sensor_splitted[0] + "_C"
                elif sensor_splitted[1][0] == '1':
                    sensor_id = sensor_splitted[0] + "_D"

                sensor_edges.add((sensor_id, sensor_edge))

def get_od_value(od):
    m = float('inf') 
    # Get the total sample of numCars
    if len(od_sensors[od]) == 0:
        return
    total_time = len(sensor_real_data[od_sensors[od][0]])
    
    # For each time stamp get the numCars
    for i in range(total_time):
        for sensor_id in od_sensors[od]:
            if (sensor_real_data[sensor_id]):
                m = min(m, sensor_real_data[sensor_id][i])
        od_num_cars[od].append(m)
        m = float('inf')



def save2od(od_num_cars):
    """
    Create a new OD file. 
    The format is: 
            origin_destination   num_cars

    Parameters 
    ----------
    od_num_cars: dict -> {od: [numCars1, numCars2,...]}, where the [numCars1, numCars2, ...] is the number of cars for each time. 
    """
    with open(od_path, 'w') as od_file:
        for od, values in od_num_cars.items():
            for value in values:
                od_file.write(f"\t\t{od}   {value}\n")


if __name__ == "__main__":
    routes = read_routes_file()
    get_detectors()

    # Add the sensors of an od
    for od, route in routes.items():
        for (id, edge) in sensor_edges:
            if edge in route:
                od_sensors[od].append(id)

    real_data = pd.read_csv("./data/AEDL2013_2015/1P2015AEDL_MorningRushHour.csv", sep=",")

    for _, real_row in real_data.iterrows():
        sensor_real_data[f"{real_row['EQUIPMENTID']}_{real_row['LANE_BUNDLE_DIRECTION']}"].append(real_row["TOTAL_VOLUME"])
        
    # Add the num_cars
    for od in routes.keys():
        get_od_value(od)

    save2od(od_num_cars)
    
    # Generate the routes
    gen_routes(od_num_cars, routes)
    error = evaluate()
    print(f'Total Error: {error}')
