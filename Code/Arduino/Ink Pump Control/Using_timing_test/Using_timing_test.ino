//Pump pin 8 is on/off
//pump pin 4, & 5 are the direction controll and must be grounded

int pumpPin = 4;
int LED = 13;

void setup() {
  // put your setup code here, to run once:

pinMode(pumpPin, OUTPUT);
pinMode(LED, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

digitalWrite(pumpPin, HIGH);
digitalWrite(LED, HIGH);
delay(1000);
digitalWrite(pumpPin, LOW);
digitalWrite(LED, LOW);
delay(5000);

}
