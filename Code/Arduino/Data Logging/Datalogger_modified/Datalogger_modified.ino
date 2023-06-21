/*
  SD card datalogger

  The circuit:
   analog sensors on analog ins 0, 1, and 2
   SD card attached to SPI bus as follows:
 ** MOSI - pin 11
 ** MISO - pin 12
 ** CLK - pin 13
 ** CS - pin 10 (for MKRZero SD: SDCARD_SS_PIN)

*/

#include <SPI.h>
#include <SD.h>

const int chipSelect = 10;
int digitalPin = 2;
long timeStamp;

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(2000000);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  //  Serial.print("Initializing SD card..."); //remove this line if data is wanted

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  //  Serial.println("card initialized."); //remove this line if data is wanted
}

void loop() {
  // make a string for assembling the data to log:

  String dataString = "";
  timeStamp = micros();

  int sensor = digitalRead(digitalPin);
  dataString += String(sensor) + "," + timeStamp;

  //  Serial.println(timeStamp);
  //  Serial.println(sensor);
  //  Serial.println(dataString);

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  File dataFile = SD.open("datalog.txt", FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.println(dataString);
    dataFile.close();
    // print to the serial port too:
    Serial.println(dataString);
  }


  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening datalog.txt");
  }
}
