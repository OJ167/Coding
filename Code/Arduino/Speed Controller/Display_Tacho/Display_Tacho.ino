//declaring LCD
#include <LiquidCrystal.h>
const int rs = 12, en = 11, d4 = 3, d5 = 4, d6 = 5, d7 = 6;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
int Contrast = 0;

//declaring sensor pins
int Obstacles_din=2;
int Obstacles_ain=A0;
int ad_value;
int din_value;

//declaring variables
float value=0;
float rev=0;
int rpm;
int oldtime=0;        
int time;


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
delay(2000);// 2 second delay
detachInterrupt(2);           //detaches the interrupt while calculating
time=millis()-oldtime;        //finds the time 
rpm=(rev/time);               //calculates rpm
oldtime=millis();             //saves the current time
rev=0;
attachInterrupt(2,beam,FALLING);

Serial.println(rev);
}


void beam()         //interrupt service routine
{
rev++;
}
