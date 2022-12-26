import pandas as pd 
import matplotlib.pyplot as plt
# disable chained assignments
pd.options.mode.chained_assignment = None

def get_records(df, start_hour, end_hour):
    # Split AGG_PERIOD_START in two columns
    df[['DATE', 'HOUR']] = df['AGG_PERIOD_START'].str.split(' ', n=1, expand=True)
    # Filter the hours
    df = df.loc[pd.to_timedelta(df['HOUR']).between(start_hour, end_hour)]
    return df

def car_flow(df):
    df = df.groupby("DATE").sum(numeric_only=False)

    fig, ax = plt.subplots()
    df.plot(y = 'TOTAL_VOLUME', ax = ax, use_index=True) 
    plt.show()

# Remove unecessary columns: TOTAL_VOLUME, AVG_LENGTH, AVG_SPACING, LIGHT_VEHICLE_RATE, VOLUME_CLASSE_X, AXLE_CLASS_VOLUMES 
def clean_data(df):
    df["TOTAL_VOLUME"] = df["VOLUME_CLASSE_A"] + df["VOLUME_CLASSE_B"]
    
    to_delete = ["DATE", "AGG_PERIOD_START", "AGGREGATE_BY_LANE_BUNDLEID", "AGG_PERIOD_LEN_MINS", "AVG_LENGTH", "AVG_SPACING", "LIGHT_VEHICLE_RATE", "VOLUME_CLASSE_A", "VOLUME_CLASSE_B", "VOLUME_CLASSE_C", "VOLUME_CLASSE_D", "VOLUME_CLASSE_0", "AXLE_CLASS_VOLUMES", "AGG_ID"]
    
    for i in to_delete:
        del df[i]

    # remove rows with OCCUPANCY = -1
    df = df[df["OCCUPANCY"] != -1]

    return df

# Group the data by the EQUIPMENTID, HOUR, LANE_BUNDLE_DIRECTION
def group_data(df):
    df = df.groupby(["EQUIPMENTID", "HOUR", "LANE_BUNDLE_DIRECTION"]).mean()

    df["NR_LANES"] = round(df["NR_LANES"]).astype(int)
    df["TOTAL_VOLUME"] = round(df["TOTAL_VOLUME"]).astype(int)
    
    return df

if '__main__' == __name__:
    df = pd.read_csv("./data/AEDL2013_2015/1P2015AEDL.csv", sep=",")
    morning_rush_hour = get_records(df, "08:00:00", "10:30:00")
    evening_rush_hour = get_records(df, "17:00:00", "20:00:00")

    #car_flow(morning_rush_hour)
    #car_flow(evening_rush_hour)
    
    morning_rush_hour = clean_data(morning_rush_hour)
    evening_rush_hour = clean_data(evening_rush_hour)

    morning_rush_hour = group_data(morning_rush_hour)
    evening_rush_hour = group_data(evening_rush_hour)

    morning_rush_hour.to_csv("./data/AEDL2013_2015/1P2015AEDL_MorningRushHour.csv", sep=",")
    evening_rush_hour.to_csv("./data/AEDL2013_2015/1P2015AEDL_EveningRushHour.csv", sep=",")