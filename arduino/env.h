#include <Arduino_MKRENV.h>

// I2CSoilMoistureSensor - Version: Latest
#include <I2CSoilMoistureSensor.h>
#include <Wire.h>

I2CSoilMoistureSensor moistureSensor;

int MOISTURE_PIN = 0;

void setupENV() {
  if (! ENV.begin()) {
    Serial.println("MKR ENV shield not found");
    while (1);
  }
}

void setupMoisture() {
  Wire.begin();
  moistureSensor.begin();
}

int readTemperature() {
  return ENV.readTemperature();
}

int readLux() {
  return ENV.readLux();
}

int readHumidity() {
  return ENV.readHumidity();
}

int readMoisture() {
  return analogRead(MOISTURE_PIN);
}
