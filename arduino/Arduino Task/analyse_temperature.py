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