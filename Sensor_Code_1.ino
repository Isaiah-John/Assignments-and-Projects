#include <Wire.h>       // I2C communication library (used by MPU6050)
#include <MPU6050.h>    // Library needed to interact with the IMU we are using
#include <math.h> // For log() computing for thermistor resistance conversion
#include <SD.h>

MPU6050 mpu;        //Creates mpu object for to control the IMU

// Motion detection
const int INTERRUPT_PIN = 2;      // sets Digital pin 2 to be used for interrupt signals on the IMU
const unsigned long MOTION_DURATION_MS = 5000;  // Motion recording lasts 5 seconds

volatile bool motionDetected = false;
bool motionActive = false;
unsigned long motionStartTime = 0;

// Thermistor setup
const int ThermistorPin1 = A0;
const int ThermistorPin2 = A1;

float R1 = 10000.0;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

// SD variables
const int chipSelect = 10;
File dataFile;

void motionISR();
void printTemperature(int pin, const char* label);

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // MPU6050 setup
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed");
    while (1);
  }

  mpu.setIntMotionEnabled(true);
  mpu.setMotionDetectionThreshold(10);
  mpu.setMotionDetectionDuration(1);
  mpu.setInterruptLatch(true);
  mpu.setDHPFMode(MPU6050_DHPF_5);
  mpu.getIntStatus();

  pinMode(INTERRUPT_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), motionISR, RISING);

  Serial.println("System ready. Waiting for motion...");

  if (!SD.begin(chipSelect)) {
  Serial.println("SD card initialization failed!");
  while (1);
  } 
  Serial.println("SD card initialized.");

}

void loop() {
  if (motionDetected && !motionActive) {
    motionDetected = false;
    motionActive = true;
    motionStartTime = millis();
    Serial.println("\n--- Motion Detected! Starting measurements ---");
    dataFile = SD.open("datalog.csv", FILE_WRITE);
    if (dataFile) {
      dataFile.println("Time(ms),AccelX(g),AccelY(g),AccelZ(g),TempC,TempF");
        dataFile.close();
    }

  }

  if (motionActive) {
    unsigned long now = millis();
    if (now - motionStartTime <= MOTION_DURATION_MS) {
      // Read acceleration
      int16_t ax, ay, az;
      mpu.getAcceleration(&ax, &ay, &az);
      float accX = ax / 16384.0;
      float accY = ay / 16384.0;
      float accZ = az / 16384.0;

      Serial.print("Accel (g) -> X: "); Serial.print(accX, 3);
      Serial.print(" | Y: "); Serial.print(accY, 3);
      Serial.print(" | Z: "); Serial.println(accZ, 3);

        dataFile = SD.open("datalog1.csv", FILE_WRITE);
      if (dataFile) {
        dataFile.print(millis()); dataFile.print(",");
        dataFile.print(accX, 3); dataFile.print(",");
        dataFile.print(accY, 3); dataFile.print(",");
        dataFile.print(accZ, 3); dataFile.print(",");
        dataFile.close();
      } else {
        Serial.println("Error opening datalog.csv");
      }
}

      // Read and print both thermistor temps
      printTemperature(ThermistorPin1, "Thermistor 1");
      printTemperature(ThermistorPin2, "Thermistor 2");


      


      delay(200);  // Sampling delay
    } else {
      Serial.println("--- Timeout reached. Returning to motion detection ---");
      motionActive = false;
      mpu.getIntStatus(); // Clear interrupt
    }
  }

void printTemperature(int pin, const char* label) {
  int Vo = analogRead(pin);
  float R2 = R1 * (1023.0 / (float)Vo - 1.0);
  float logR2 = log(R2);
  float T = 1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2);
  float Tc = T - 273.15;
  float Tf = (Tc * 9.0) / 5.0 + 32.0;

  Serial.print(label);
  Serial.print(" Temperature: ");
  Serial.print(Tc, 2); Serial.print(" °C / ");
  Serial.print(Tf, 2); Serial.println(" °F");

   dataFile = SD.open("datalog.csv", FILE_WRITE);
      if (dataFile) {
        dataFile.print(Tc, 2); dataFile.print(",");
        dataFile.println(Tf, 2);
        dataFile.close();
      } else{
        Serial.println("Error opening datalog.csv");
      }
}

void motionISR() {
  motionDetected = true;
}
