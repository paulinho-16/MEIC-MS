
from configparser import ConfigParser, ExtendedInterpolation
import logging
import pandas as pd
# disable chained assignments
pd.options.mode.chained_assignment = None

logging.basicConfig(level=logging.INFO)
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("./src/config.ini")


def get_filtered_by_hour(df: pd.DataFrame, start_hour: str, end_hour: str) -> pd.DataFrame:
    """Get records between start_hour and end_hour

    Args:
        df (pd.DataFrame): The Dataframe
        start_hour (str): The start hour
        end_hour (str): The end hour

    Returns:
        pd.DataFrame: The data frame alread filtered.
    """
    # Split AGG_PERIOD_START in two columns
    df[['DATE', 'HOUR']] = df['AGG_PERIOD_START'].str.split(
        ' ', n=1, expand=True)
    # Filter the hours
    df = df.loc[pd.to_timedelta(df['HOUR']).between(start_hour, end_hour)]
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove unecessary columns: TOTAL_VOLUME, AVG_LENGTH, AVG_SPACING, LIGHT_VEHICLE_RATE, VOLUME_CLASSE_X, AXLE_CLASS_VOLUMES 

    Args:
        df (pd.DataFrame): The dataframe to be cleaned,. 

    Returns:
        pd.DataFrame: The cleaned DataFrame
    """

    df["TOTAL_VOLUME"] = df["VOLUME_CLASSE_A"] + df["VOLUME_CLASSE_B"]

    to_delete = ["DATE", "AGG_PERIOD_START", "AGGREGATE_BY_LANE_BUNDLEID", "AGG_PERIOD_LEN_MINS", "AVG_LENGTH", "AVG_SPACING", "LIGHT_VEHICLE_RATE",
                 "VOLUME_CLASSE_A", "VOLUME_CLASSE_B", "VOLUME_CLASSE_C", "VOLUME_CLASSE_D", "VOLUME_CLASSE_0", "AXLE_CLASS_VOLUMES", "AGG_ID"]

    # Remove unecessary columns
    for i in to_delete:
        del df[i]

    # remove rows with OCCUPANCY = -1
    df = df[df["OCCUPANCY"] != -1]

    return df

# Group the data by the EQUIPMENTID, HOUR, LANE_BUNDLE_DIRECTION


def group_data(df: pd.DataFrame) -> pd.DataFrame:
    """Group data by the EQUIPMENTID, HOUR and LANE_BUNDLE_DIRECTION and get the mean of the other components.

    Args:
        df (pd.DataFrame): The dataframe to be analysed

    Returns:
        pd.DataFrame: The grouped dataframe
    """
    df = df.groupby(["EQUIPMENTID", "HOUR", "LANE_BUNDLE_DIRECTION"]).mean()

    df["NR_LANES"] = round(df["NR_LANES"]).astype(int)
    df["TOTAL_VOLUME"] = round(df["TOTAL_VOLUME"]).astype(int)

    return df


if '__main__' == __name__:
    df = pd.read_csv("", sep=",")
    morning_rush_hour = get_filtered_by_hour(df, "08:00:00", "10:30:00")
    evening_rush_hour = get_filtered_by_hour(df, "17:00:00", "20:00:00")

    morning_rush_hour = clean_data(morning_rush_hour)
    evening_rush_hour = clean_data(evening_rush_hour)

    morning_rush_hour = group_data(morning_rush_hour)
    evening_rush_hour = group_data(evening_rush_hour)

    morning_rush_hour.to_csv(config["data"]["REAL_MORNING_FILE"], sep=",")
    evening_rush_hour.to_csv(config["data"]["REAL_EVENING_FILE"], sep=",")
