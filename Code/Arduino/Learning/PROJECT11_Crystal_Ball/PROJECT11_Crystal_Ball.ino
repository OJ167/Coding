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

lcd.print("Ask The");//LCD starts to print in the top left
lcd.setCursor(0,1);//setting LCD to move to the bottom left
lcd.print("Crystal Ball");
}

void loop() {
  // put your main code here, to run repeatedly:

switchState = digitalRead(switchPin);

if(switchState != prevSwitchState){ //checking for change in switch state.
  if (switchState == LOW){ //checking that the switch has been triggered to low.
    reply = random(8); //creates a random response number 0-7.
    lcd.clear();
    lcd.print("The Ball Says: ");
    lcd.setCursor(0,1);//setting LCD to move to the bottom left
    switch(reply){
      case 0:
      lcd.print("Yes!");
      break;
      case 1:
      lcd.print("Most Likely");
      break;
      case 2:
      lcd.print("Certainly");
      break;
      case 3:
      lcd.print("Looks Good");
      break;
      case 4:
      lcd.print("Unsure");
      break;
      case 5:
      lcd.print("Ask Again");
      break;
      case 6:
      lcd.print("Doubtful");
      break;
      case 7:
      lcd.print("Nah");
      break;
    }
    
  }
}
prevSwitchState = switchState;
}
