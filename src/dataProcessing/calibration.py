import pandas as pd
import sumolib
import subprocess
from sklearn.metrics import mean_absolute_error
from .algorithms import hill_climbing, genetic_algorithm
from ..sumo.utils import read_od_dict
from ..sumo.utils import read_routes_file

clean_net_file = "./data/porto_clean.net.xml"

def calculate_error(real_data, simulation_data):
    minute = 0
    current_sensor = ""
    total_error = 0
    for _, real_row in real_data.iterrows():
        if current_sensor != real_row["EQUIPMENTID"]:
            current_sensor = real_row["EQUIPMENTID"]
            minute = 0 
        else:
            minute += 300
        
        if real_row["LANE_BUNDLE_DIRECTION"] == "D":
            sim_rows = simulation_data.loc[(simulation_data["id"].str.startswith(str(real_row["EQUIPMENTID"]))) & ((simulation_data["id"].str.split("_").str[1]).str.startswith("1")) & (simulation_data["begin"] == minute)]
        else:
            sim_rows = simulation_data.loc[(simulation_data["id"].str.startswith(str(real_row["EQUIPMENTID"]))) & ((simulation_data["id"].str.split("_").str[1]).str.startswith("0")) & (simulation_data["begin"] == minute)]

        # Consider the values of all the lanes in the same direction
        function_dictionary = {'nVehContrib': 'sum', 'speed': 'mean', 'harmonicMeanSpeed': 'mean'}
        sim_rows = sim_rows.groupby('begin').agg(function_dictionary).reset_index()
        
        if sim_rows.empty: # TODO: após ignorar sensores nas entradas/saídas, tirar isto
            continue
        
        sim_row = sim_rows.iloc[0]

        real_values = [real_row["TOTAL_VOLUME"], real_row["AVG_SPEED_ARITHMETIC"], real_row["AVG_SPEED_HARMONIC"]]
        simulation_values = [sim_row["nVehContrib"], sim_row["speed"], sim_row["harmonicMeanSpeed"]]

        error = mean_absolute_error(real_values, simulation_values)
        total_error += error
    
    return total_error

def evaluate() -> float:
    p = subprocess.Popen(("sumo", "./data/vci.sumocfg"))
    p.wait()

    p = subprocess.Popen(("make", "data"))
    p.wait()

    real_data = pd.read_csv("./data/AEDL2013_2015/1P2015AEDL_MorningRushHour.csv", sep=",")
    simulation_data = pd.read_csv("./data/simulation/1P2015AEDL_MorningRushHour.csv", sep=",")

    total_error = calculate_error(real_data, simulation_data)
    print(f"Total error: {total_error}")
    
    return total_error

if '__main__' == __name__:
    # net = sumolib.net.readNet(clean_net_file)
    # nodes = net.getNodes()
    
    od = read_od_dict()
    routes = read_routes_file()
    
    p = subprocess.Popen(("make", "repair_paths"))
    p.wait()

    # best_od_values = hill_climbing(routes, od, evaluate)
    best_od_values = genetic_algorithm(routes, od, evaluate, 100)