const byte ledPin = 13;
const byte interruptPin = 2;
volatile byte state = LOW;
int rev = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), blink, FALLING);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(ledPin, state);
  Serial.println(rev);
}

void blink() {
  state = !state;
  rev++;
}
