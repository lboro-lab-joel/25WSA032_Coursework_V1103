import serial
import time
 
SERIAL_PORT = "COM3" # the port that the pyphon script should read from.
BAUD_RATE   = 9600
OUTPUT_FILE = "temperature_data.csv"
 
print("Connecting to Arduino... (waiting ~1 minute for first cycle)")
 
ser  = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=10)
time.sleep(2)  # wait for Arduino to reset
 
lines = []
for raw in ser:
    line = raw.decode("utf-8", errors="replace").strip()
    print(line)
 
    # this is the way the file can identify where the reading finishes (made the script output # END when it serial prints it.)
    if line == "# END": 
        break
 
    if not line.startswith("#"):
        lines.append(line)
 
ser.close()
 
with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(lines))
 
print(f"\nSaved to {OUTPUT_FILE}")