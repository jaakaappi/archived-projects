#include <Arduino.h>
#include <SPI.h>
#include <SD.h>

enum STATUS {
   INIT,
   READY,
   ERROR
};

STATUS sd_status = INIT;
STATUS gps_status = INIT;

File gpx_file;
const int sd_chip_select = 3;

bool sd_write_nmea(String nmea)
{
   gpx_file = SD.open("log.txt", FILE_WRITE);
   if (!gpx_file)
   {
      return false;
   }
   byte written = gpx_file.print(nmea);
   if (nmea.length() != 0 && written == 0)
   {
      return false;
   }
   gpx_file.close();
   return true;
}

String read_nmea_data()
{
   String buffer = "";
   while (Serial1.available())
   {
      char c = Serial1.read();
      buffer += c;
   }
   Serial.print(buffer);
   return buffer;
}

void setup()
{

   // setup serial
   Serial.begin(9600);
   if (Serial)
   {
      Serial.println("GPXLogger is coming up");
      Serial.println("- Serial connection init successful");
   }

   // setup sd card
   pinMode(53, OUTPUT);

   if (!SD.begin(sd_chip_select))
   {
      Serial.println("- SD card init failed");
   }
   else
   {
      Serial.println("- SD card init successful");
   }

   //setup gps
   Serial1.begin(9600);
   if (Serial1)
   {
      Serial.println("- GPS init successful");
   }
   else
   {
      Serial.println("- GPS init failed");
   }
}

void loop()
{
   if (gps_status == READY && sd_status == READY)
   {
      String nmea_buffer_contents = read_nmea_data();
      boolean sd_write_success = sd_write_nmea(nmea_buffer_contents);
      if (!sd_write_success)
      {
      }
      if (Serial)
      {
         Serial.println(nmea_buffer_contents);
      }
   }
   else if (gps_status == INIT)
   {
      if (Serial1.available())
      {
      }
   }
   else
   {
   }
}