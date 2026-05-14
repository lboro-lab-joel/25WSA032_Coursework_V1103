Python:
The way to run the python code is to use run.ps1 .The code has been adapted to run the robot_optimisation code and bring pack KPI's in the output box, with baseline and optimised KPI tables and a Final table that compares both.

Arduino:
This comes as multiple steps, as I needed to use multiple files to do each of the processes.

Close 

The order is uploading the file temperature_optimisation(insert filepath) into the arduino. I had better results using the Arduino IDE to upload the code to the arduino, but if there is no problems with the VScode setup on your end then hopefully it should be fine.
If you go Arduino IDE route:

Upload the code to the Arduino, start the serial monitor, where it should wait a little while (approx 1min), then it should print all the results at once with # END being visible at the end of the Serial Monitor. This tests to see if it works. stop the serial monitor and close the Arduino IDE

Now go back to VScode, open capture_serial.py located at (insert file location). run the file as you would a standard python file, click run or F5. It should do the same thing as the Arduino code where it should wait a little while (approx 1min), except the difference is the values are now stored in a CSV. The CSV file will be generated automatically. The end should say "Saved to temperature_data.csv"

Once it has said the values have been stored, run the analyse_temperature.py file (insert file location), and this should generate 5 graphs according to the brief. This will also save those graphs into temperature_analysis.png, which can be further analysed.
