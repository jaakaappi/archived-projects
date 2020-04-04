#include <Adafruit_NeoPixel.h>
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(1, 5, NEO_GRB + NEO_KHZ800);

int sensor1signal = A0;
int sensor2signal = A1;

int sensor1power = 6;
int sensor2power = 7;

int pump1signal = A2;
int pump2signal = A3;

int sensor1threshold = 800;
int sensor2threshold = 800;

int ledpin = 5;

int measuredelay = 10000;
int waterduration = 20000;

void setup() {
  pixels.begin();

  pinMode(sensor1signal, INPUT);
  pinMode(sensor2signal, INPUT);

  pinMode(sensor1power, OUTPUT);
  pinMode(sensor2power, OUTPUT);

  pinMode(pump1signal, OUTPUT);
  pinMode(pump2signal, OUTPUT);
  digitalWrite(pump1signal, HIGH);
  digitalWrite(pump2signal, HIGH);

  digitalWrite(sensor1power, LOW);
  digitalWrite(sensor2power, LOW);

  Serial.begin(115200);
}

void loop() {
  if (digitalRead(13) == HIGH) {
    Serial.println("checking");
    int sensor1value = readSensor(sensor1power, sensor1signal);
    if (sensor1value >= sensor1threshold) {
      irrigate(pump1signal, waterduration);
    }
    int sensor2value = readSensor(sensor2power, sensor2signal);
    if (sensor2value >= sensor2threshold) {
      irrigate(pump2signal, waterduration);
    }

    delay(measuredelay);
  }
  else {
    pixels.setPixelColor(0, pixels.Color(255, 105, 180));
    pixels.show();
    delay(1000);
    pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    pixels.show();
    delay(1000);
  }
}

int readSensor(int sensorpower, int sensorsignal) {
  digitalWrite(sensorpower, HIGH);
  delay(100);
  int value = analogRead(sensorsignal);
  Serial.println(value);
  digitalWrite(sensorpower, LOW);
  return value;
}

void irrigate(int relaypin, int duration) {
  Serial.println("started irrigating relay in pin" + String(relaypin) + " for " + String(duration) + " milliseconds");
  digitalWrite(relaypin, LOW);
  delay(duration);
  digitalWrite(relaypin, HIGH);
}

