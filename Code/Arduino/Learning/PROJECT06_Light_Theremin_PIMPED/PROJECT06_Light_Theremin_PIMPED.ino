int sensorValue;
int duration;
int duration100;
int sensorLow = 1023;
int sensorHigh = 0;

const int ledPin = 13; //this is the onboard LED

void setup() {
  // put your setup code here, to run once:

pinMode(ledPin, OUTPUT);
digitalWrite(ledPin, HIGH); //turn the LED on during callibration

while(millis() < 5000){ //while condition which will last for 5000ms. millis command uses onboard clock to check the time that has passed

//this section is doing the callibration of high and low values
  sensorValue = analogRead(A0);
  if(sensorValue > sensorHigh){
    sensorHigh = sensorValue;
  }
  if(sensorValue < sensorLow){
    sensorLow = sensorValue;
  }
}
digitalWrite(ledPin, LOW); //turn LED off
duration = analogRead(A1);
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  
sensorValue = analogRead(A0);

duration = analogRead(A1);

int duration100 = map(duration, 0, 1023, 0, 100);
Serial.print(duration100);

int Pitch = map(sensorValue, sensorLow, sensorHigh, 50, 4000);
tone(8, Pitch, 50);
delay(20);
}
