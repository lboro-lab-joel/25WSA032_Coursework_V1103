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

# DFT Magnitude vs Frequency (skip DC frequency = 0)
ax = axes[0, 1]
mask = frequency > 0
ax.stem(frequency[mask], magnitude[mask], linefmt = "steelblue", markerfmt = "C0o", basefmt = "grey")
ax.set_title("Plot 2: Magnitude vs Frequency (DFT)")
ax.set_xlabel("Freqency (Hz)")
ax.set_ylabel("Magnitude")
ax.grid(True, linestyle = "--", alpha = 0.5)

# Raw vs Smoothed Temperature - using mean
ax = axes[1, 0]
smoothed = pd.Series(temperature).rolling(window=MA_WINDOW, min_periods=1).mean()
ax.plot(time, temperature, color="steelblue", alpha=0.5, label="Raw")
ax.plot(time, smoothed,    color="crimson",   linewidth=2, label=f"Smoothed (window={MA_WINDOW})")
ax.set_title("Plot 3: Raw vs Smoothed Temperature")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Temperature (°C)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)

#Histogram of temperature readings
ax = axes[1,1]
ax.hist(temperature, bins = 20, color = "steelblue", edgecolor = "white")
ax.set_title("Plot 4: Histogram of temperature readings")
ax.set_xlabel("Temperature (*C)")
ax.set_ylabel("Count")
ax.grid(True, linestyle = "--", alpha = 0.5, axis = "y")

# Temperature change rate against time
ax = axes[2,0]
change_rate = np.diff(temperature) # difference between consecutive samples
ax.plot(time[:-1], change_rate, color = "darkorange")
ax.axhline(0, color = "grey", linestyle = "--", linewidth = 0.8)
ax.set_title("Plot5; Temperature Chnage Rate vs Time")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Change Rate (*C/ sample)")
ax.grid(True, linestyle = "--", alpha  = 0.5)

#Hiding the 6th plot
axes[2,1].set_visible(False)


# Saving the plot as a PNG to show the program can output graphical files.
plt.tight_layout()
plt.savefig("temperature_analysis.png", dpi = 150, bbox_inches = "tight")
print("Saved to temperature_analysis.png")
plt.show()