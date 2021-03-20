#include "thingProperties.h"
#include <WiFiNINA.h>

const int LED = LED_BUILTIN;

const String WEB_HOST = SECRET_SERVER_HOST

WiFiServer server(80);
WiFiClient client;
WiFiSSLClient sslClient;
int status = WL_IDLE_STATUS;

void printWiFiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}

void setupIOT() {
  pinMode(LED, OUTPUT);
  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }

  String fv = WiFi.firmwareVersion();
  if (fv < "1.0.0") {
    Serial.println("Please upgrade the firmware");
  }

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(SECRET_SSID);                   // print the network name (SSID);

    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(SECRET_SSID, SECRET_PASS);
    // wait 10 seconds for connection:
    delay(10000);
  }
  printWiFiStatus();                        // you're connected now, so print out the status
}


void updateMetrics(int temperature, int moisture, int lux, int humidity) {
  sslClient.stop();

  if (sslClient.connect(WEB_HOST, 443)) {

    String queryString = String("") +
      "?temperature=" + temperature +
      "&moisture=" + moisture +
      "&lux=" + lux +
      "&humidity=" + humidity;
    // send the HTTP PUT request:
    sslClient.println("GET " + WEB_HOST + "/metrics" + queryString + " HTTP/1.1");
    sslClient.println("Host: script.google.com");
    sslClient.println("User-Agent: ArduinoWiFi/1.1");
    sslClient.println("Accept: */*");
    sslClient.println("Connection: close");
    sslClient.println();
  } else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
  }
}
