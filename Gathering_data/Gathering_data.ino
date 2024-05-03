/*
  Arduino BMI270 - Simple Accelerometer

  This example reads the acceleration values from the BMI270
  sensor and continuously prints them to the Serial Monitor
  or Serial Plotter.

  The circuit:
  - Arduino Nano 33 BLE Sense Rev2

  created 10 Jul 2019
  by Riccardo Rizzo

  This example code is in the public domain.
*/

#include "Arduino_BMI270_BMM150.h"

void setup() {
  Serial.begin(115200);
  while (!Serial);
  // Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  /*
  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Acceleration in G's");
  Serial.println("X\tY\tZ");
  */


}

unsigned long current_time;
unsigned long previous_time = 0;

void loop() {
  float ax, ay, az, gx, gy, gz;
  unsigned long sampling_time;

  if (IMU.accelerationAvailable()) {// && IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    //IMU.readGyroscope(gx, gy, gz);
    current_time = millis();
    sampling_time = current_time - previous_time;
    //Serial.print("sampling rate: "); Serial.print(IMU.accelerationSampleRate()); Serial.print(" Hz     ");
    //Serial.print("time interval: ");
     Serial.print(sampling_time); Serial.println(" ms     ");
    
    /*
    Serial.print(ax); Serial.print(',');
    Serial.print(ay); Serial.print(',');
    Serial.print(az); Serial.print(',');
    Serial.print(gx); Serial.print(',');
    Serial.print(gy); Serial.print(',');
    Serial.println(gz); 
    */
  }
 // if (IMU.gyroscopeAvailable()) {// && IMU.gyroscopeAvailable()) {
    //IMU.readAcceleration(ax, ay, az);
    //IMU.readGyroscope(gx, gy, gz);
    //current_time = millis();
   // sampling_time2 = current_time2 - previous_time2;
    //Serial.print("sampling rate: "); Serial.print(IMU.accelerationSampleRate()); Serial.print(" Hz     ");
    //Serial.print("time interval: ");
    // Serial.print(sampling_time2); Serial.println(" ms     ");
    
    /*
    Serial.print(ax); Serial.print(',');
    Serial.print(ay); Serial.print(',');
    Serial.print(az); Serial.print(',');
    Serial.print(gx); Serial.print(',');
    Serial.print(gy); Serial.print(',');
    Serial.println(gz); 
    */
 // }



  previous_time = current_time;
}
