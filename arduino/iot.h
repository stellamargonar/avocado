#include "thingProperties.h"

void setupIOT() {
  // This delay gives the chance to wait for a Serial Monitor without blocking if none is found
  delay(5000);

  // Defined in thingProperties.h
  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  /*
     The following function allows you to obtain more information
     related to the state of network and IoT Cloud connection and errors
     the higher number the more granular information you’ll get.
     The default is 0 (only errors).
     Maximum is 4
  */
  setDebugMessageLevel(3);
  ArduinoCloud.printDebugInfo();

}


void updateIOT(int new_temperature, int new_moisture) {
  temperature = new_temperature;
  moisture = new_moisture;
  // lux = new_lux;
  ArduinoCloud.update();
}
