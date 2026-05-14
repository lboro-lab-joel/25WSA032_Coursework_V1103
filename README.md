# READ ME

This file is in the 'root of your project.
You can use this to provide top-level documentation of your project

Hardware:
Arduino IDE
Grove Temperature Sensor
USB Cable connecting the sensors
Wire connecting sensor to the UNO

Software:
Arduino IDE (for uploading the sketch)
Python
Python libraries (pyserial, pandas, matplotlib, numpy)

FOLDER STRUCTURE:

File path - F530917_25WSA032_Coursework_V1103\arduino\temperature_optimisation contains the temperature_optimisation.ino
File path - F530917_25WSA032_Coursework_V1103\robots contains the robot_optimisation.py file (run with the run.ps1 file)

documentation\ - contains the task briefs, Discussion (part of Task 4 with Arduino), setup and checklist

How to run all the code:

Task 2 - Arduino
Open temperature_optimisation.ino
Select board Arduino UNO and correct port
Click Upload
Close the serial monitor

Task 3 - Python
Run the file run.ps1 within the robots\ folder.
It should output the KPI's baseline and optimised table and print out the comparison table

Task 4 - Analysis (Using the Arduino)
Run capture_serial.py to collect the data from the Arduino (Steps mentioned in the how_to_run_code.md file in documentation\)
Run analyse_temperature.py
Output graphs will appear on screen and will also save as a png in temperature_analysis_live.png, the data stored in temperature_data.csv (both located at \F530917_25WSA032_Coursework_V1103, the root folder)
(Note - the graphs will be there for the session, running a new session will overwrite the picture of the previous)