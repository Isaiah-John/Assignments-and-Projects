#include <Wire.h>
#include <MPU6050.h>
#include <SD.h>
#include <math.h>
#include "TimerOne.h"

// --- Thermistor Setup ---
const int tecThermistorPin = A1;       // TEC monitor
const int chamberThermistorPin = A0;   // Chamber monitor
const float seriesResistor = 10000.0;  // Ohms
const float nominalResistance = 10000.0;
const float nominalTemperature = 25.0;
const float bCoefficient = 3470.0;

// --- Accelerometer Setup ---
MPU6050 mpu;

// --- SD Setup ---
const int chipSelect = 8;
File tempsFile;
File accelFile;
File charlieFile;

// --- TEC Control ---
const int tecPwmPin = 9;
const int targetTemp = 15; // Celsius
const int tempTolerance = 3;
int dutyCycle = 0;

unsigned long lastLogTime = 0;
unsigned long lastFlushTime = 0;
const unsigned long flushInterval = 1000;

bool tecOverheat = false;
bool peltierOn = false;

void setup() {
  Wire.begin();

  pinMode(tecThermistorPin, INPUT);
  pinMode(chamberThermistorPin, INPUT);
  pinMode(tecPwmPin, OUTPUT);
  Timer1.initialize(100);
  Timer1.pwm(tecPwmPin, 0);

  mpu.initialize();
  if (!mpu.testConnection()) {
    while (1);
  }

  if (!SD.begin(chipSelect)) {
    while (1);
  }

  tempsFile = SD.open("temps.csv", FILE_WRITE);
  if (tempsFile) {
    tempsFile.println(F("Time(ms),TEC monitor (C),Chamber monitor (C)"));
    tempsFile.flush();
  }

  accelFile = SD.open("accel.csv", FILE_WRITE);
  if (accelFile) {
    accelFile.println(F("Time(ms),AccelX(g),AccelY(g),AccelZ(g)"));
    accelFile.flush();
  }

  charlieFile = SD.open("charlie.csv", FILE_WRITE);
  if (charlieFile) {
    charlieFile.println(F("Time(ms),TECTemp(C),ChamberTemp(C),AccelX(g),AccelY(g),AccelZ(g),DutyCycle"));
    charlieFile.flush();
  }
}

void loop() {
  if (millis() - lastLogTime >= 1000) {
    lastLogTime = millis();

    float tecTemp = readThermistor(tecThermistorPin);
    float chamberTemp = readThermistor(chamberThermistorPin);

    int16_t ax, ay, az;
    mpu.getAcceleration(&ax, &ay, &az);
    float accX = ax / 16384.0;
    float accY = ay / 16384.0;
    float accZ = az / 16384.0;

    // TEC Control Logic
    if (!tecOverheat) {
      if (tecTemp >= 37.0 && !peltierOn) {
        dutyCycle = 200;
        Timer1.setPwmDuty(tecPwmPin, dutyCycle);
        peltierOn = true;
      } else if (tecTemp <= 36.0 && peltierOn) {
        Timer1.setPwmDuty(tecPwmPin, 0);
        dutyCycle = 0;
        peltierOn = false;
      }
    }

    if (tempsFile) {
      tempsFile.print(millis()); tempsFile.print(",");
      tempsFile.print(tecTemp, 2); tempsFile.print(",");
      tempsFile.println(chamberTemp, 2);
    }

    if (accelFile) {
      accelFile.print(millis()); accelFile.print(",");
      accelFile.print(accX, 3); accelFile.print(",");
      accelFile.print(accY, 3); accelFile.print(",");
      accelFile.println(accZ, 3);
    }

    if (charlieFile) {
      charlieFile.print(millis()); charlieFile.print(",");
      charlieFile.print(tecTemp, 2); charlieFile.print(",");
      charlieFile.print(chamberTemp, 2); charlieFile.print(",");
      charlieFile.print(accX, 3); charlieFile.print(",");
      charlieFile.print(accY, 3); charlieFile.print(",");
      charlieFile.print(accZ, 3); charlieFile.print(",");
      charlieFile.println(dutyCycle);
    }
  }

  if (millis() - lastFlushTime >= flushInterval) {
    if (tempsFile) tempsFile.flush();
    if (accelFile) accelFile.flush();
    if (charlieFile) charlieFile.flush();
    lastFlushTime = millis();
  }
}

float readThermistor(int pin) {
  int adcValue = analogRead(pin);
  float voltage = adcValue * (5.0 / 1023.0);
  float resistance = seriesResistor * ((5.0 / voltage) - 1.0);

  float steinhart;
  steinhart = resistance / nominalResistance;
  steinhart = log(steinhart);
  steinhart /= bCoefficient;
  steinhart += 1.0 / (nominalTemperature + 273.15);
  steinhart = 1.0 / steinhart;
  steinhart -= 273.15;

  return steinhart;
}
