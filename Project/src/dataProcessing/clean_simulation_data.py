from collections import defaultdict
from configparser import ConfigParser, ExtendedInterpolation
import logging
import pandas as pd
from xml.dom import minidom

logging.basicConfig(level=logging.INFO)
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("./src/config.ini")


def get_data():
    f = minidom.parse(config["data"]["SIMULATION_OUTPUT_FILE"])
    return f.getElementsByTagName("interval")


def create_dict(elements):
    attributes = ["begin", "end", "id", "nVehContrib", "flow",
                  "occupancy", "speed", "harmonicMeanSpeed", "length", "nVehEntered"]
    res = defaultdict(list)

    for att in attributes:
        for ele in elements:
            res[att].append(ele.attributes[att].value)

    return res


def create_csv(d: dict):
    df = pd.DataFrame.from_dict(d)
    df.to_csv(config["data"]["SIMULATION_PROCESSED_FILE"], index=False)


if __name__ == "__main__":
    data = get_data()
    d = create_dict(data)
    create_csv(d)
