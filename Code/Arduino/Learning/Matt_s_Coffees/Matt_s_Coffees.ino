#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

int switchPin = 6;
int switchState = 0;
int prevSwitchState = 0;
int reply;

void setup() {
  // put your setup code here, to run once:
pinMode(switchPin, INPUT); //making the pin an input.
lcd.begin(16, 2); //initialising the LCD library and giving it dimensions.

lcd.print("How many coffees");//LCD starts to print in the top left
lcd.setCursor(0,1);//setting LCD to move to the bottom left
lcd.print("will Matt have?");
delay(5000);
}

void loop() {
  // put your main code here, to run repeatedly:

switchState = digitalRead(switchPin);

if(switchState != prevSwitchState){ //checking for change in switch state.
  if (switchState == LOW){ //checking that the switch has been triggered to low.
    reply = random(5); //creates a random response number 0-7.
    lcd.clear();
    lcd.print("The Ball Says: ");
    lcd.setCursor(0,1);//setting LCD to move to the bottom left
    switch(reply){
      case 0:
      lcd.print("None");
      break;
      case 1:
      lcd.print("One");
      break;
      case 2:
      lcd.print("Two");
      break;
      case 3:
      lcd.print("Three");
      break;
      case 4:
      lcd.print("Many");
      break;
    }
    
  }
}
prevSwitchState = switchState;
}
