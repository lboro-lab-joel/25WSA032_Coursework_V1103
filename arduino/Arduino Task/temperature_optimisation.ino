// Loovee @ 2015-8-26
#include <avr/sleep.h> // for debugging
#include <avr/wdt.h>
#include <math.h>

const int B = 4275000;         // B value of the thermistor
const int R0 = 100000;         // R0 = 100k
const int pinTempSensor = A0;  // Grove - Temperature Sensor connect to A0

const int N = 10;
const FS_DEFAULT = 1 //sampling frequency
const FS_MIN = 0.5
const FS_MAX = 4

const float pi = 3.1415926535;
int count = 0;

int time_data[N];
float temp_data[N];
float realPart[N];
float imagPart[N];
float magnitude[N];
float freqValues[N];

int del = 1000; //How often the reading will be taken.
int sampleCount = 0;
int idleCycleCount = 0
float fs = FS_DEFAULT; //setting the initial sampling rate

void setup() {
  Serial.begin(9600);
}

void loop() {
  int a = analogRead(pinTempSensor);
  float R = 1023.0 / a - 1.0;
  R = R0 * R;
  float temperature = 1.0 / (log(R / R0) / B + 1 / 298.15) - 273.15; 
  
  
  bool bufferFull = collect_temperature_data(temperature);
  if (bufferFull){
    //Runing the analysis itself
    float dominantFreq = apply_dft()
    Powermode mode = decide_power_mode(dominantFreq);
    //Myquist's theorm adjustment
    float newFs = dominantFreq * 2;
    if (newFs < FS_MIN) newFs = FS_MIN;
    if (newFs > FS_MIN) newFs = FS_MAX;    
    fs = newFs;
    delayMs = (int)(1000/fs);

  }
  if (mode == IDLE){
    idleCycleCount++;
  }
  else{
    idleCycleCount = 0;
  }

  if (idleCycleCount >= 5){
    mode = POWER_DOWN;
  }
  send_data_to_pc();

  if (mode == POWER_DOWN){
    enterSleep();
  }
  delay (delayMs)
}

bool collect_temperature_data(float temp) {
  time_data[sampleCount] = sampleCount * (1/fs); // Actual time in seconds (recurring)
  temp_data[sampleCount] = temp;
  sampleCount++;

  //Serial.println(temp_data[count]);
  if (sampleCount > 10){ // remove this if the recuring reading is not wanted.
    sampleCount = 0;
    return True;
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
    realPart[k] = 0; //I needed this because arduino doesnt store complex numbers.
    imagPart[k] = 0;

    for(int n=0; n<N; n++){
      float angle = 2*pi*k*n/N
      realPart[k] += temp_data[n]*cos(angle)
      imagPart[k] -= temp_data[n]*sin(angle) 
    }
  }
  magnitude[k] = sqrt(realPart[k]*realPart[k] + imag[k]*imag[k]); //As mentioned in task 2.
  freqValues[k] = (float)k * fs / N;  //The Frequency of the bin (frequency interval)

  float dominantFreq = 0; //Where the dominant frequency will be stored.
  float maxMag = 0;

  //This finds the highest magnitude of the frequency
  for (int k = 1; k < N/2; k++) {  // start at 1 (skip DC), stop at N/2 (Nyquist for efficiency)
      if (magnitude[k] > maxMag) {
          maxMag = magnitude[k];
          dominantFreq = freqValues[k];
      }
  }
  return dominantFreq
}

//Defining the thrresholds to the modes
const float FREQ_ACTIVE_THRESHOLD = 0.5;
const float FREQ_IDLE_THRESHOLD = 0.1

enum PowerMode{ 
  ACTIVE,
  IDLE,
  POWER_DOWN
};

PowerMode decide_power_mode(float dominantFreq) { // returns the mode based on the dominant frequensy (active, idle or power down)
  if (dominantFreq > FREQ_ACTIVE_THRESHOLD) {
    return ACTIVE;
  } else if (dominantFreq > FREQ_IDLE_THRESHOLD) {
    return IDLE;
  } else {
    return POWER_DOWN;
  }
}

//Putting Arduino into low-power sleep mode
void enterSleep() {
  Serial.println("# Entering Power Down sleep...");
  Serial.flush();                        // make sure serial output is sent before sleeping

  wdt_enable(WDTO_8S);                   // watchdog wakes us after 8 seconds
  WDTCSR |= (1 << WDIE);                 // enable watchdog interrupt (not reset)

  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  sleep_cpu();                           // sleeps here until watchdog fires

  sleep_disable();                       // continues here after waking
  wdt_disable();                         // turn off watchdog until next sleep
}

// Watchdog interrupt service routine — just wakes the CPU, does nothing else
ISR(WDT_vect) { }

void send_data_to_pc(){
  //CSV header
  Serial.println("Time, Temperature, Frequency, Magnitude");

for(int i = 0; i< N; i++){
  Serial.print(time_data[i],2); // 2 decimal places
  Serial.print(",");
  Serial.print(temp_data[i],2);
  Serial.print(",");
  Serial.print(freqValues[i],4); // 4 decimal places for small values
  Serial.print(",");
  Serial.print(magnitude[i],2);
}
  Serial.println("# END"); // indicationn of end of transmission
}