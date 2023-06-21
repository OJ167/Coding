//assigning pin values
const int greenLEDPin = 9;
const int blueLEDPin = 10;
const int redLEDPin = 11;
const int redSensorPin = A0;
const int greenSensorPin = A1;
const int blueSensorPin = A2;

//assigning initial values for each parameter
int redLEDValue = 0;
int greenLEDValue = 0;
int blueLEDValue = 0;

int redSensorValue = 0;
int greenSensorValue = 0;
int blueSensorValue = 0;

void setup() {
  // put your setup code here, to run once:

//open serial input
Serial.begin(9600);

//selecting the pin modes of the outputs
pinMode(greenLEDPin, OUTPUT);
pinMode(blueLEDPin, OUTPUT);
pinMode(redLEDPin, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

//reading the input from each analogue input pin and addigning the value to a variable
redSensorValue = analogRead(redSensorPin);
delay(5);
greenSensorValue = analogRead(greenSensorPin);
delay(5);
blueSensorValue = analogRead(blueSensorPin);
delay(2);

//printing the outputs to the monitor

Serial.print("Raw Sensor values \t Red: ");
Serial.print(redSensorValue);
Serial.print("\t Green: ");
Serial.print(greenSensorValue);
Serial.print("\t Blue: ");
Serial.println(blueSensorValue);

//calculating the PWM values for each colour. PWM values are from 0-255 but sesnor values are 0-1023.

redLEDValue = redSensorValue/4;
greenLEDValue = greenSensorValue/4;
blueLEDValue = blueSensorValue/4;

//sending output to pins
analogWrite(redLEDPin, redLEDValue);
analogWrite(redLEDPin, redLEDValue);
analogWrite(greenLEDPin, greenLEDValue);
analogWrite(blueLEDPin, blueLEDValue);

//sending signals to monitor
Serial.print("PWM LED values \t Red: ");
Serial.print(redLEDValue);
Serial.print("\t Green: ");
Serial.print(greenLEDValue);
Serial.print("\t Blue: ");
Serial.println(blueLEDValue);
}
