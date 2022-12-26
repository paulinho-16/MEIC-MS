import pandas as pd
from sklearn.metrics import mean_absolute_error

if '__main__' == __name__:
    real_data = pd.read_csv("./data/AEDL2013_2015/1P2015AEDL_MorningRushHour.csv", sep=",")
    simulation_data = pd.read_csv("./data/Simulation/1P2015AEDL_MorningRushHour.csv", sep=",")

    minute = 0
    current_sensor = ""
    total_error = 0
    for _, real_row in real_data.iterrows():

        if current_sensor != real_row["EQUIPMENTID"]:
            current_sensor = real_row["EQUIPMENTID"]
            minute = 0
        else:
            minute += 300

        # TODO: verify C and D meaning
        if real_row["LANE_BUNDLE_DIRECTION"] == "C":
            sim_rows = simulation_data.loc[(str(simulation_data["id"]).startswith(str(real_row["EQUIPMENTID"]))) & (str(simulation_data["id"]).split("_")[1].startswith("1")) & (simulation_data["begin"] == minute)]
        else:
            sim_rows = simulation_data.loc[(str(simulation_data["id"]).startswith(str(real_row["EQUIPMENTID"]))) & (str(simulation_data["id"]).split("_")[1].startswith("0")) & (simulation_data["begin"] == minute)]

        print('------------')
        print(sim_rows)
        print(len(sim_rows))

        # TODO: somar sim_rows, que são todas no mesmo sentido
        sim_row = sim_rows.sum(axis=0)

        real_values = [real_row["TOTAL_VOLUME"], real_row["AVG_SPEED_ARITHMETIC"], real_row["AVG_SPEED_HARMONIC"]]
        simulation_values = [sim_row["nVehContrib"], sim_row["speed"], sim_row["harmonicMeanSpeed"]]

        error = mean_absolute_error(real_values, simulation_values)
        total_error += error

    print(f"Total error: {total_error}")