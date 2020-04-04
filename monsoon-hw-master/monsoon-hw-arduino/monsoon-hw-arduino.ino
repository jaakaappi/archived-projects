#include <SoftwareSerial.h>

const String SYSTEM_NAME = "test";
const int PLANT_COUNT = 1;

typedef struct {
  String name;
  int sensorPin;
  int pumpPin;
  int humidityLowLimit;
  int wateringDuration;
} Plant;

Plant plants[] = {
  {"test", 1, 1, 1, 1}
};

int lastMeasurementTime = 0;
int measurementPeriod = 0;

SoftwareSerial espSerial(10, 11);

void setup() {
  Serial.begin(115200);
  while (!Serial) {}
  Serial.println("== Monsoon booting! ==");
  preparePins();
  waitConnectToESP();
  measureWaterAndReport();
  Serial.println("== Monsoon ready! ==");
}

void loop() {
  if (abs(millis()-lastMeasurementTime) >= measurementPeriod) {
    measureWaterAndReport();
  }
}

void preparePins() {
  Serial.write("Started to prepare pins");
  for (int i = 0; i < PLANT_COUNT; i++) {
    pinMode(plants[i].sensorPin, INPUT);
    pinMode(plants[i].pumpPin, OUTPUT);
  }
  Serial.write("Pins prepared");
}

void waitConnectToESP() {
  Serial.println("Connecting to ESP");
  espSerial.begin(115200);
  delay(200);
  Serial.println("ESP connected");
}

void registerSystem() {
  Serial.println("register " + SYSTEM_NAME + " " + PLANT_COUNT);
}

void measureWaterAndReport() {
  Serial.write("Measuring");
  for (int i = 0; i < PLANT_COUNT; i++) {
    int humidity = measure(plants[i]);
    if (humidity < plants[i].humidityLowLimit) {
      water(plants[i]);
      report(plants[i], humidity, true);
      Serial.println(plants[i].name+" humidity "+humidity+", watered\n");
    } else {
      report(plants[i], humidity, false);
      Serial.println(plants[i].name+" humidity "+humidity+"\n");
    }
  }
  lastMeasurementTime = millis();
  Serial.println("Measurements complete");
}

int measure(Plant plant) {
  return analogRead(plant.sensorPin);
}

void water(Plant plant) {
  digitalWrite(plant.pumpPin, HIGH);
  delay(plant.wateringDuration);
  digitalWrite(plant.pumpPin, LOW);
}

void report(Plant plant, int humidity, bool watered) {
  espSerial.println("measurement " + plant.name + " " + humidity + " " + watered);
  while(Serial.available() == 0){}
  String result = Serial.readStringUntil('\n');
  if(result != "ok"){
    
  } else {
    Serial.println(plant.name+" reported succesfully");
  }
}

