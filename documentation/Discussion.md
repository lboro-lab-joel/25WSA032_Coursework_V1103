The experiment:
Warmed up the sensor by hand, and let it cool to room temperature

The graph example I will be taking is in the temperature_analysis.png in file location F530917_25WSA032_Coursework_V1103.


Time-Domain Behaviour:
Temperature started at ~23.3, and rose to ~24.1 at around 18s.
plot 5 confirms this with the spike at the change rate between 0-10 seconds, and then sustaining negative values as it cooled
The signal is smooth, minimal noise.

Frequency- Domain
Plot 2 shows dominant energy at low frequencies, (~0.05Hz)
Spike near 1.0Hz shows the initial rapid warming, fast change in temperature results in high frequency content in DFT
most mid range frequencies are near 0, confirming there are no rapid periodic oscillations.

System behavior
The dominant frequency ~0.05Hz would trigger the Idle or Power Down mode correctly,
The rapid initial warning pushed it into ACTIVE MODE
Moving average would correctly track the warming trend.

Data Quality
This captured 1 minute of the sensor data, although the brief recommended 3 minutes.I had issues with the amount of storage available on the arduino itself, so needed to cut down the sample time to make up for it. It can be run 3 times to get the values for 3 minutes worth.
1Hz sampling was enough to show the smaller changes in temperature, no details were missed.