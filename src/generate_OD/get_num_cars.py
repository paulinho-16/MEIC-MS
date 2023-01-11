"""This file is responsible for generating an OD file, based on the number of cars of real data. 
For one sensor that has a flow x, this flow is splitted among the pairs (origin, destination) equally. 
"""


from configparser import ConfigParser, ExtendedInterpolation
import pandas as pd

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("./src/config.ini")

def get_volume_per_hour() -> float:
    """Get the total volume per hour by summing all the total volume lines and dividing by 3, which is the number of hours.

    Returns:
        float: the volume per hour
    """
    start_hour = float(config["runtime"]["HOUR_START"])
    end_hour = float(config["runtime"]["HOUR_END"])
    df = pd.read_csv(config["runtime"]["REAL_DATA"])
    return df['TOTAL_VOLUME'].sum()/(end_hour-start_hour)



if __name__ == '__main__':
    pass