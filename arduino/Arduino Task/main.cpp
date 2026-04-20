// Loovee @ 2015-8-26
#include <avr/sleep.h> // for debugging
#include <math.h>
const int B = 4275000;         // B value of the thermistor
const int R0 = 100000;         // R0 = 100k
const int pinTempSensor = A0;  // Grove - Temperature Sensor connect to A0
const int N = 10;
const float pi = 3.1415926535;
int count = 0;
int time_data[N];
float temp_data[N];
float real[N];
float imaginary[N];
int del = 1000; //How often the reading will be taken.


void setup() {
  Serial.begin(9600);
}

void loop() {
  int a = analogRead(pinTempSensor);
  float R = 1023.0 / a - 1.0;
  R = R0 * R;
  float temperature = 1.0 / (log(R / R0) / B + 1 / 298.15) - 273.15; 
  collect_temperature_data(temperature);
  Serial.print("temperature = ");
  Serial.println(temperature);
  float freq = apply_dft()
  Serial.print(freq);
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
    Serial.print(temp_data[x]); //Debugging purposes
    Serial.print(' ');
  }
  Serial.println();

}

float apply_dft(){
  for(int k=0; k<N; k++){
    real[k] = 0; //I needed this because arduino doesnt store complex numbers.
    imag[k] = 0;

    for(int n=0, n<N, n++){
      float angle = 2*pi*k*n/N
      real[k] = temp_data[n]*cos(angle)
      imag[k] = temp_data[n]*cos(angle)
    }
  }
  magnitude[k] = sqrt(real[k]*real[k] + imag[k]*imag[k]); //As mentioned in task 2.
  freqValues[k] = (float)k * fs / N;  //The Frequency of the bin (frequency interval)

  float dominantFreq = 0; //Where the dominant frequency will be stored.
  float maxMag = 0;

  //This finds the highest magnitude of the frequency
  for (int k = 1; k < N/2; k++) {  // start at 1 (skip DC), stop at N/2 (Nyquist for efficiency)
      if (magnitude[k] > maxMag) {
          maxMag = magnitude[k];
          dominantFreq = freqValues[k];
          return dominantFreq
      }
}
}
  
void stop(){
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  sleep_cpu();  // halts here.
}