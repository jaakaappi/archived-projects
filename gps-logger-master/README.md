# gps-logger
Arduino GPS logger with microSD support built using PlatformIO.

Reads NMEA-0183 GPS data from Beitian BN-220 via a serial connection.

[BN-220 module spec sheet](https://files.banggood.com/2016/11/BN-220%20GPS+Antenna%20datasheet.pdf)

[NMEA message specification](https://www.gpsinformation.org/dale/nmea.htm)

## Wiring

### Arduino Mega 2560

TODO update GN220 pins

| Arduino pin   | Receiving pin |
| ------------- | ------------- |
|2|OLED CS|
|3|SD module CS|
|9|OLED RES|
|10|OLED DC|
|11|OLED D1|
|12|OLED D0|
|18|GPS RX|
|19|GPS TX|
|50|SD MISO|
|51|SD MOSI|
|52|SD SCK|
|5V|SD and GPS VCC|
|3V|OLED VCC|
|GND|OLED, GPS and SD GNDs|

## v2 plans
- Smaller case, made for Teensy
- Waterproof power switch
- Some kind of attachment point / strap.
- Made of ABS.
