/**
   BasicHTTPClient.ino

    Created on: 24.05.2015

*/

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>

WiFiMulti wifiMulti;

/*
   Serial = USB, Serial2 = standalone Arduino
   See board specific pinout for ESP32 and connect RX/TX there
*/

#define SSID "Purrkki"
#define PWD "kissakala"

bool isConnected = false;
String espconnectionstatus = "Not connected";

void setup() {

  Serial.begin(115200);
  delay(1000);
  wifiMulti.addAP("Purrkki", "kissakala");

}

void loop() {
  if (Serial) {
    if (!isConnected) {
      isConnected = true;
      Serial.println("Monsoon ESP32 connected");
      Serial.println("Firmware last updated on " __DATE__ " ," __TIME__);
      Serial.println("Access point: " SSID);
      Serial.println("Connection status: "+espconnectionstatus);
    } else {
      if (Serial.available()) {
        // todo ssid/pwd updating
      }
    }
  } else {
    isConnected = false;
  }

  //    // wait for WiFi connection
  //    if((wifiMulti.run() == WL_CONNECTED)) {
  //
  //        HTTPClient http;
  //
  //        Serial.print("[HTTP] begin...\n");
  //        // configure traged server and url
  //        //http.begin("https://www.howsmyssl.com/a/check", ca); //HTTPS
  //        http.begin("http://example.com/index.html"); //HTTP
  //
  //        Serial.print("[HTTP] GET...\n");
  //        // start connection and send HTTP header
  //        int httpCode = http.GET();
  //
  //        // httpCode will be negative on error
  //        if(httpCode > 0) {
  //            // HTTP header has been send and Server response header has been handled
  //            Serial.printf("[HTTP] GET... code: %d\n", httpCode);
  //
  //            // file found at server
  //            if(httpCode == HTTP_CODE_OK) {
  //                String payload = http.getString();
  //                Serial.println(payload);
  //            }
  //        } else {
  //            Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
  //        }
  //
  //        http.end();
  //    }
  //
  //    delay(5000);
}
