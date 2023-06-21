//Pin Deffinitions
int switchUpper = 2;
int LED_Pin = 13 ;

// Global Variables

volatile int switch_Upper_Flag;
int flashCounter = 0;


void setup() {
  // put your setup code here, to run once:
  pinMode(LED_Pin, OUTPUT);
  digitalWrite(LED_Pin, LOW);   // turn the LED on (HIGH is the voltage level)
  pinMode(switchUpper, INPUT_PULLUP);
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(2), ISR_switchUpper, RISING);
  digitalWrite(LED_Pin, HIGH);
}


void loop() {  //this is the part that causes the flashing
  // put your main code here, to run repeatedly:



  if (switch_Upper_Flag == LOW) {
    digitalWrite(LED_Pin, LOW);
    //Serial.print("low");
  }
  else {


    digitalWrite(LED_Pin, LOW);
    delay(500);
    digitalWrite(LED_Pin, HIGH);
    delay(500);
    digitalWrite(LED_Pin, LOW);
    delay(500);
    digitalWrite(LED_Pin, HIGH);
    delay(5000);
    digitalWrite(LED_Pin, LOW);
    delay(100);
    digitalWrite(LED_Pin, HIGH);
    delay(100);
    digitalWrite(LED_Pin, LOW);
    delay(100);
    digitalWrite(LED_Pin, HIGH);
    delay(100);
    Serial.print("high");

    Serial.println(digitalRead(switch_Upper_Flag));
    switch_Upper_Flag = LOW;
  }
  Serial.println(switch_Upper_Flag);
}

void ISR_switchUpper() {
  switch_Upper_Flag = HIGH;
  Serial.println(switch_Upper_Flag);
}
