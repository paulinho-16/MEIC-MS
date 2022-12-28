from xml.dom import minidom 
import pandas as pd 
from collections import defaultdict 

simulation_file = "./data/simulation.out.xml"
output_file = "./data/simulation/1P2015AEDL_MorningRushHour.csv"

def get_data(): 
    f = minidom.parse(simulation_file)
    return f.getElementsByTagName("interval")

def create_dict(elements): 
    attributes = ["begin", "end", "id", "nVehContrib", "flow", "occupancy", "speed", "harmonicMeanSpeed", "length", "nVehEntered"]
    res = defaultdict(list)

    for att in attributes: 
        for ele in elements: 
            res[att].append(ele.attributes[att].value)

    return res

def create_csv(d: dict):
    df = pd.DataFrame.from_dict(d)
    df.to_csv(output_file, index=False)
    
if __name__ == "__main__":
    data = get_data()
    d = create_dict(data)
    create_csv(d)