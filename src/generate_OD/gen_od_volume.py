"""This file is responsible for generating an OD file, based on the number of cars of real data. 
For one sensor that has a flow x, this flow is splitted among the pairs (origin, destination) equally. 
"""


from collections import defaultdict
from configparser import ConfigParser, ExtendedInterpolation
import logging
import pandas as pd

from ..sumo.utils import read_routes_file


logging.basicConfig(level=logging.INFO)
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("./src/config.ini")


def get_volume_per_hour() -> pd.DataFrame:
    """Get the total volume per hour and for each sensor by summing all the total volume lines and dividing by 3, which is the number of hours.

    Returns:
        pd.DataFrame: contains the total volume per hour of each sensor
    """
    start_hour = float(config["runtime"]["HOUR_START"])
    end_hour = float(config["runtime"]["HOUR_END"])
    df = pd.read_csv(config["runtime"]["REAL_DATA"])
    df["EQUIPMENTID"] = df["EQUIPMENTID"].astype(
        str) + "_" + df["LANE_BUNDLE_DIRECTION"]
    df = df.groupby(by=["EQUIPMENTID"]).sum(numeric_only=True)
    df["TOTAL_VOLUME"] /= (end_hour - start_hour)
    return df


def get_sensor_locations() -> set[tuple[str, str]]:
    """Gets the edges where each sensor is located.

    Returns:
        set[tuple[str, str]]: A set containing at each pair the (sensor_id, sensor_edge)
    """

    sensor_edges = set([])
    with open(config["data"]["SENSORS_FILE"]) as f:
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
    return sensor_edges


def gen_sensor_ods(sensor_edges: set[tuple[str, str]], routes: dict[str, str]) -> dict[list]:
    """Gets what are the sensors that an od path passes by.

    Args:
        sensor_edges (set[tuple]): A set containing tuple as elements. ("origin_destination", edge).
        routes (dict[str, str]): Keys as the "origin_destination" od and the values as a string containing the path of an od as the a string of edges sliptted by space. 

    Returns:
        dict[list]: Values as a list of ods (i.e., ["origin_destination"]). Keys as the sensor's ids.
    """

    sensor_ods = defaultdict(list)
    for (id, edge) in sensor_edges:
        for od, route in routes.items():
            if edge in route:
                sensor_ods[id].append(od)
    return sensor_ods


def gen_od_volume(sensor_volumes: pd.DataFrame, sensor_ods: dict[str, list[str]]) -> dict[str, float]:
    """Distributes the volume of a sensor by each od whose path passes through the sensor.

    Args:
        sensor_volumes (pd.DataFrame): The DataFrame containing the equipment total volume.
        sensor_ods (dict[str, list]): A dictionary mapping the sensor_id to the ods (i.e., "origin_destination") whose path passes through the sensor. 

    Returns:
        dict[str, float]: Keys as the od and values as the volume for this sensor in an hour.
    """
    od_volume = defaultdict(float)
    for (sensor_id, od_list) in sensor_ods.items():
        total_elements = len(od_list)
        sensor_volume: pd.Series = sensor_volumes.loc[sensor_volumes.index ==
                                                      sensor_id, "TOTAL_VOLUME"]
        if sensor_volume.empty:
            continue
        volume_per_od = sensor_volume[0]/total_elements
        for od in od_list:
            od_volume[od] += volume_per_od
    return od_volume


def save2od(od_volume: dict[str, float]) -> None:
    """Saves the dictionary as od. 

    Args:
        od_volume (dict[str, float]): Keys as the ods (i.e., "origin_destination"), values as the volume.
    """
    with open(config["data"]["OD_FILE"], 'w') as od_file:
        for od, volume in od_volume.items():
            od_file.write(f"{od} {round(volume)}\n")


if __name__ == '__main__':
    # Keys as "origin_destination" and values as a string with edges.
    sensor_volumes: pd.DataFrame = get_volume_per_hour()
    routes: dict[str, str] = read_routes_file()
    sensor_edges: set[tuple[str, str]] = get_sensor_locations()
    sensor_ods: dict[str, list[str]] = gen_sensor_ods(sensor_edges, routes)
    od_volume: dict[str, float] = gen_od_volume(sensor_volumes, sensor_ods)
    logging.info("Saving OD...")
    save2od(od_volume)
    logging.info("OD saved with success!")
