// Loovee @ 2015-8-26
#include <avr/sleep.h> // for debugging
#include <math.h>
const int B = 4275000;         // B value of the thermistor
const int R0 = 100000;         // R0 = 100k
const int pinTempSensor = A0;  // Grove - Temperature Sensor connect to A0
const int N = 10;
int count = 0;
int time_data[N];
float temp_data[N];
int del = 1000;


void setup() {
  Serial.begin(9600);
}

void loop() {
  int a = analogRead(pinTempSensor);
  float R = 1023.0 / a - 1.0;
  R = R0 * R;
  float temperature = 1.0 / (log(R / R0) / B + 1 / 298.15) - 273.15;  // convert to temperature via datasheet
  collect_temperature_data(temperature);
  Serial.print("temperature = ");
  Serial.println(temperature);
  delay(del);
}
float collect_temperature_data(float temp) {
  time_data[count] = count; // This takes a reoccuring update in the active mode.
  temp_data[count] = temp;
  count++;
  //Serial.println(temp_data[count]);
  if (count > 10){ // remove this if the recuring reading is not wanted.
    count = 0;
    stop();
  }

  int num = sizeof(temp_data)/sizeof(int);
  for (int x = 0; x<num;x++){
    Serial.print(temp_data[x]);
    Serial.print(' ');
  }
  Serial.println();
}
void stop(){
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  sleep_cpu();  // halts here, minimal power draw
}