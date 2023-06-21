#include <Servo.h>

//creating a servo object - this contains all the options and capabilities of the servo library
Servo myServo;

//creating constants
const int potPin = A0;
int potValue;
int angle;

void setup() {
  // put your setup code here, to run once:

//telling the program where the servo is
myServo.attach(9);

//creating a serial connection to check values from potentiometer
Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly: 

//assigning potentiometer value and printing it to monitor.
potValue = analogRead(potPin);
Serial.print("potentiometer input: ");
Serial.print(potValue);

//mapping the angle from raw input to angle.
angle = map(potValue, 0, 1023, 0, 179);
Serial.print("\t Angle: ");
Serial.println(angle);

//commands to move the servo
myServo.write(angle);
delay(150);
}
