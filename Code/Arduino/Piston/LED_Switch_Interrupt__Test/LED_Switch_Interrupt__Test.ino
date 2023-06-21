//Pin Deffinitions
int switchUpper = 2;
int LED_Pin = 13 ;
long ISR_Delay = 1000000000;

// Global Variables

volatile int switch_Upper_Flag;
int flashCounter = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_Pin, OUTPUT);
  pinMode(switchUpper, INPUT);
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(2), ISR_switchUpper, RISING);

}

void loop() {  //this is the part tha causes the flashing
  // put your main code here, to run repeatedly:
  digitalWrite(LED_Pin, HIGH);   // turn the LED on (HIGH is the voltage level)
  Serial.print(digitalRead(switchUpper));
}

void ISR_switchUpper() {

  digitalWrite(LED_Pin, LOW);    // turn the LED off by making the voltage LOW
  delayMicroseconds(ISR_Delay);
}
