#include <avr/sleep.h>
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"
#include <RtcDS3231.h>
#include <Wire.h>

RtcDS3231<TwoWire> Rtc(Wire);

bool USE_DFPLAYER = true;

SoftwareSerial mySoftwareSerial(11, 10); // RX, TX
DFRobotDFPlayerMini myDFPlayer;

volatile bool interrupted = false;

RtcDateTime compiled = RtcDateTime(__DATE__, __TIME__);

int song = 1;
int lastSong = 30;

void setup() {
  delay(1000);

  pinMode(2, INPUT);
  pinMode(13, OUTPUT);

  Rtc.Begin();
  Rtc.Enable32kHzPin(false);
  Rtc.SetSquareWavePin(DS3231SquareWavePin_ModeAlarmOne);
  Rtc.SetDateTime(compiled);
  setup_alarm();

  delay(100);
  sleep();
}

void setup_alarm() {
  DS3231AlarmOne alarm1(0, random(1,5), 0, 0, DS3231AlarmOneControl_SecondsMatch);
  Rtc.SetAlarmOne(alarm1);
  Rtc.LatchAlarmsTriggeredFlags();
  attachInterrupt(digitalPinToInterrupt(2), interrupt, CHANGE);
}

void sleep() {
  sleep_enable();
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_mode();
  sleep_disable();
}

void interrupt() {
  interrupted = true;
}

void loop() {
  if (interrupted) {
    wakePlayerPlayNext();
    delay(100);
    interrupted = false;
    setup_alarm();
    sleep();
    detachInterrupt(digitalPinToInterrupt(2));
  }
}

void wakePlayerPlayNext() {
  mySoftwareSerial.begin(9600);
  if (!myDFPlayer.begin(mySoftwareSerial)) {
    while (true);
  }
  myDFPlayer.volume(30);
  myDFPlayer.play(song);
  song++;
  if(song > lastSong){
    song = 1;
  }
  delay(60000);
  myDFPlayer.sleep();
}

