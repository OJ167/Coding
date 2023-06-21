//#include <timeLib.h>


//declaring LCD
#include <LiquidCrystal.h>
const int rs = 12, en = 11, d4 = 3, d5 = 4, d6 = 5, d7 = 6;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
int Contrast = 0;

//declaring sensor pins
int Obstacles_din = 2;
int Obstacles_ain = A0;

//declaring variables
float rev;
float rpm;
float oldtimeo; 
float timeo; 



void setup()
{
  analogWrite(9,Contrast);
  pinMode(Obstacles_din,INPUT);
  pinMode(Obstacles_ain,INPUT);
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(Obstacles_din), beam, CHANGE);

  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  
  // Print a message to the LCD.
  lcd.print("That's a");
  lcd.setCursor(0, 1);
  lcd.print("good trick!");
  delay(2000);
  lcd.clear();
}
void loop()
{
  delay(20000);

  timeo=millis()-oldtimeo;        //finds the timeo  
  rpm=(rev/timeo)*500;            //calculates rpm 

  //Clearing the LCD
  lcd.clear();
  //printing to the LCD
  lcd.setCursor(0, 1);
  lcd.print(rpm);
  lcd.setCursor(0, 0);
  lcd.print("RPM");

  //printing stuff to test
  //Serial.println(rev);
  //Serial.println(digitalRead(Obstacles_din));
  //Serial.println(millis());
  //Serial.println(timeo);
  //Serial.println(oldtimeo);
  Serial.println(rpm);

  oldtimeo=millis();             //saves the current timeo 
  rev = 0;
}


void beam(){         //interrupt service routine
rev++;
Serial.println("ISR active");
}
