from configparser import ConfigParser, ExtendedInterpolation
import logging
import pandas as pd
from sklearn.metrics import mean_absolute_error

logging.basicConfig(level=logging.INFO)
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read("./src/config.ini")


def get_simulation_row(real_row: pd.Series, simulation_data: pd.DataFrame, minute: int) -> pd.DataFrame:
    """Generate the simulation row corresponding to the real data row, grouping all the rows of a given direction.

    Args:
        real_row (pd.DataFrame): real data from VCI sensors
        simulation_data (pd.DataFrame): simulated data from SUMO sensors
        minute (int): period of 5 min in which the data was collected

    Returns:
        pd.DataFrame: the corresponding simulation row.
    """
    if real_row["LANE_BUNDLE_DIRECTION"] == "D":
        sim_rows: pd.DataFrame = simulation_data.loc[(simulation_data["id"].str.startswith(str(real_row["EQUIPMENTID"]))) & (
            (simulation_data["id"].str.split("_").str[1]).str.startswith("1")) & (simulation_data["begin"] == minute)]
    else:
        sim_rows: pd.DataFrame = simulation_data.loc[(simulation_data["id"].str.startswith(str(real_row["EQUIPMENTID"]))) & (
            (simulation_data["id"].str.split("_").str[1]).str.startswith("0")) & (simulation_data["begin"] == minute)]

    # Consider the values of all the lanes in the same direction
    function_dictionary: dict[str, str] = {
        'nVehContrib': 'sum', 'speed': 'mean', 'harmonicMeanSpeed': 'mean'}
    return sim_rows.groupby('begin').agg(function_dictionary).reset_index()


def calculate_error(real_data: pd.DataFrame, simulation_data: pd.DataFrame) -> float:
    """Calculate simulation error based on real data.

    Args:
        real_data (pd.DataFrame): real data from VCI sensors
        simulation_data (pd.DataFrame): simulated data from SUMO sensors

    Returns:
        float: the total error of the simulation.
    """
    minute: int = 0
    current_sensor: str = ""
    total_error: float = 0

    for _, real_row in real_data.iterrows():
        if current_sensor != real_row["EQUIPMENTID"]:
            current_sensor = real_row["EQUIPMENTID"]
            minute: int = 0
        else:
            minute += 300

        sim_row: pd.DataFrame = get_simulation_row(real_row, simulation_data, minute)
        
        if sim_row.empty: # for real sensors that are not being used in the simulation
            continue

        sim_row: pd.Series = sim_row.iloc[0]
        real_values = [real_row["TOTAL_VOLUME"],
                       real_row["AVG_SPEED_ARITHMETIC"], real_row["AVG_SPEED_HARMONIC"]]
        simulation_values = [sim_row["nVehContrib"],
                             sim_row["speed"], sim_row["harmonicMeanSpeed"]]

        error: float = mean_absolute_error(real_values, simulation_values)
        total_error += error

    return total_error


def evaluate() -> float:
    """Calculate simulation error based on real data.

        Returns: 
            float: Returns the error
    """
    real_data: pd.DataFrame = pd.read_csv(
        config["data"]["REAL_MORNING_FILE"], sep=",")
    simulation_data: pd.DataFrame = pd.read_csv(
        config["data"]["SIMULATION_PROCESSED_FILE"], sep=",")

    total_error: float = calculate_error(real_data, simulation_data)
    print(f"Total error: {total_error}")

    return total_error


if '__main__' == __name__:
    evaluate()
