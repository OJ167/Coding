//Pin Deffinitions
//int switchUpper = 2;
//int LED_Pin = 13 ;


// Global Variables

volatile boolean switch_Flag = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(4, OUTPUT);
  pinMode(2, INPUT);
  attachInterrupt(2, ISR_switch, RISING);
  digitalWrite(LED_BUILTIN, HIGH);

}

void loop() {
  // put your main code here, to run repeatedly:
}

void ISR_switch() {

  if (switch_Flag) {
    switch_Flag = false;
    digitalWrite(4, LOW);
  }
  else {
    switch_Flag = true;
    digitalWrite(4, HIGH);
  }
}
