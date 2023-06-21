int LEDPin = 13;
int Button = 2;
volatile byte state = LOW;

void setup() {
  // put your setup code here, to run once:
  pinMode(2, INPUT_PULLUP);
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(2), isr_button, FALLING);

}

void loop() {
  // put your main code here, to run repeatedly:

  digitalWrite(LEDPin, state);
  Serial.println(digitalRead(Button));

}


void isr_button() {

  state = !state;

}
