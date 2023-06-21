
#include <LiquidCrystal.h>
const int rs = 12, en = 11, d4 = 3, d5 = 4, d6 = 5, d7 = 6;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
int Contrast = 0;

int Obstacles_din=6;
int Obstacles_ain=A0;
int ad_value;
int din_value;



void setup()
{
  analogWrite(9,Contrast);
  pinMode(Obstacles_din,INPUT);
  pinMode(Obstacles_ain,INPUT);
  Serial.begin(9600);

  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("That's a");
  lcd.setCursor(0, 1);
  lcd.print("good trick!");
  
}
void loop()
{
  ad_value = analogRead(Obstacles_ain);
  din_value = digitalRead(Obstacles_din);
  if(digitalRead(Obstacles_din)==LOW)
  {
    Serial.println("Near the Obstacles");
    Serial.println(ad_value);
    Serial.println(din_value);
  }
  else
  {
    Serial.println("Far the Obstacles");
    Serial.println(din_value);
  }
  delay(500);
}
