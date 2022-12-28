import pandas as pd
import sumolib
import subprocess
from sklearn.metrics import mean_absolute_error
from ..sumo import gen_od
from ..sumo import gen_routes 

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

if '__main__' == __name__:
    od_values = [1 for _ in range(1666)]
    
    # TODO: loop de IA para correr várias vezes e calibrar

    net = sumolib.net.readNet(clean_net_file)
    nodes = net.getNodes()
    gen_od.generate_od(nodes, od_values)
    gen_routes.gen_routes()
    subprocess.call(["make", "repair_paths"])

    subprocess.call(["sumo.exe", "./data/vci.sumocfg"])

    subprocess.call(["make", "data"])

    real_data = pd.read_csv("./data/AEDL2013_2015/1P2015AEDL_MorningRushHour.csv", sep=",")
    simulation_data = pd.read_csv("./data/Simulation/1P2015AEDL_MorningRushHour.csv", sep=",")

    total_error = calculate_error(real_data, simulation_data)
    print(f"Total error: {total_error}")