import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


def car_flow(df, start_hour, end_hour): 
    # Split AGG_PERIOD_START in two columns
    df[['DATE', 'HOUR']] = df['AGG_PERIOD_START'].str.split(' ', 1, expand=True)

    # Filter the hours 
    df = df.loc[pd.to_timedelta(df['HOUR']).between(start_hour, end_hour)]
    df = df.groupby("DATE").sum()

    fig, ax = plt.subplots()
    df.plot(y = 'TOTAL_VOLUME', ax = ax, use_index=True) 
    plt.show()
    print(df.head())


df = pd.read_csv("../data/vci/1P2015AEDL.csv", sep=",") 
car_flow(df, "08:00:00", "10:30:00")
car_flow(df, "17:00:00", "20:00:00")