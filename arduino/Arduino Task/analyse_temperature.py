import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = "temperature_data.csv"
MA_WINDOW = 10

# df = dataframe - holds all the data into a table
df = pd.read_csv(DATA_FILE, comment = "#", skipinitialspace=True)
df.columns = df.columns.str.strip()

time = df["Time"].to_numpy(dtype = float)
temperature = df["Temperature"].to_numpy(dtype = float)
frequency = df["Frequency"].to_numpy(dtype = float)
magnitude = df["Magnitude"].to_numpy(dtype = float)

DATA_FILE = "temperature_data.csv"
MA_WINDOW = 10 # window size

#This is the code to fit the differnet graphs
fig, axes = plt.subplots(3, 2, figsize=(14, 12))
fig.suptitle("Arduino Temperature Monitoring — Data Analysis", fontsize=14)

# Temperature against Time
ax = axes[0, 0]
ax.plot(time, temperature, color = "steelblue")
ax.set_title("Plot 1: Temperature vs Time")
ax.set_xlabel("Time(s)")
ax.set_ylabel("Temperature (*C)")
ax.grid(True, linestyle = "--", alpha = 0.5)