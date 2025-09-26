#include <Wire.h>
#include <MPU6050.h>
#include <SD.h>
#include <math.h>

// --- Thermistor Setup ---
const int ThermistorPin1 = A0;
const int ThermistorPin2 = A1;

float R1 = 10000.0; // 10k fixed resistor
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

// --- SD Setup ---
const int chipSelect = 8;
File dataFile;

// --- Accelerometer Setup ---
MPU6050 mpu;
const int INTERRUPT_PIN = 2;
const unsigned long MOTION_DURATION_MS = 5000;

volatile bool motionDetected = false;
bool motionActive = false;
unsigned long motionStartTime = 0;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // Thermistor Pins
  pinMode(ThermistorPin1, INPUT);
  pinMode(ThermistorPin2, INPUT);

  // MPU6050 Init
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed");
    while (1);
  }

  // MPU6050 Motion Config
  mpu.setIntMotionEnabled(true);
  mpu.setMotionDetectionThreshold(10);
  mpu.setMotionDetectionDuration(1);
  mpu.setInterruptLatch(true);
  mpu.setDHPFMode(MPU6050_DHPF_5);
  mpu.getIntStatus();  // Clear interrupts

  // Interrupt Pin
  pinMode(INTERRUPT_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), motionISR, RISING);

  // SD Card Init
  if (!SD.begin(chipSelect)) {
    Serial.println("SD card initialization failed!");
    while (1);
  }
  Serial.println("SD card initialized.");

  // Initialize files
  dataFile = SD.open("temps.csv", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Label,TempF,TempC");
    dataFile.close();
  }

  dataFile = SD.open("accel.csv", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Time(ms),AccelX(g),AccelY(g),AccelZ(g)");
    dataFile.close();
  }

  Serial.println("System ready. Waiting for motion...");
}

void loop() {
  // --- Log Temperature Every 500 ms ---
  static unsigned long lastTempLog = 0;
  if (millis() - lastTempLog >= 10000) {
    logTemperature(ThermistorPin1, "Thermistor 1");
    logTemperature(ThermistorPin2, "Thermistor 2");
    lastTempLog = millis();
  }

  // --- Motion Detection and Accelerometer Logging ---
  if (motionDetected && !motionActive) {
    motionDetected = false;
    motionActive = true;
    motionStartTime = millis();
    Serial.println("Motion detected! Starting accelerometer logging...");
  }

  if (motionActive) {
    unsigned long now = millis();
    if (now - motionStartTime <= MOTION_DURATION_MS) {
      int16_t ax, ay, az;
      mpu.getAcceleration(&ax, &ay, &az);
      float accX = ax / 16384.0;
      float accY = ay / 16384.0;
      float accZ = az / 16384.0;

      Serial.print("X: "); Serial.print(accX); Serial.print(" g\t");
      Serial.print("Y: "); Serial.print(accY); Serial.print(" g\t");
      Serial.print("Z: "); Serial.println(accZ); Serial.print(" g");

      dataFile = SD.open("accel.csv", FILE_WRITE);
      if (dataFile) {
        dataFile.print(millis()); dataFile.print(",");
        dataFile.print(accX, 3); dataFile.print(",");
        dataFile.print(accY, 3); dataFile.print(",");
        dataFile.println(accZ, 3);
        dataFile.close();
      }

      delay(200);
    } else {
      Serial.println("Timeout reached. Returning to motion detection...");
      motionActive = false;
      mpu.getIntStatus();  // Clear interrupt
    }
  }
}

void logTemperature(int pin, const char* label) {
  int Vo = analogRead(pin);
  float R2 = R1 * (1023.0 / (float)Vo - 1.0);
  float logR2 = log(R2);
  float T = 1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2);
  float Tc = T - 273.15;
  float Tf = (Tc * 9.0) / 5.0 + 32.0;

  Serial.print(label); Serial.print(": ");
  Serial.print(Tf, 2); Serial.print(" °F / ");
  Serial.print(Tc, 2); Serial.println(" °C");

  dataFile = SD.open("temps.csv", FILE_WRITE);
  if (dataFile) {
    dataFile.print(label); dataFile.print(",");
    dataFile.print(Tf, 2); dataFile.print(",");
    dataFile.println(Tc, 2);
    dataFile.close();
  }
}

void motionISR() {
  motionDetected = true;
}
