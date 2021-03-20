#include "arduino_secrets.h"

#include "env.h"
#include "iot.h"
#define UPDATE_INTERVAL 36000000

bool awake = true;

void setup() {
  Serial.begin(9600);
  delay(1000);
  setupENV();
  setupIOT();
}


void loop() {
  updateMetrics(readTemperature(), readMoisture(), readLux(), readHumidity());
  goToSleep();
}

void goToSleep() {
  delay(UPDATE_INTERVAL);
}
