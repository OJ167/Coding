void setup() {
  pinMode(2, INPUT);
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);
  Serial.begin(9600);
}

void loop() {
  int stateButton = digitalRead(2);
  Serial.println(stateButton);
  delay(500);

  if (digitalRead(2 == HIGH)) {
    digitalWrite(4, HIGH);
  }
  else {
    digitalWrite(4, LOW);
  }
}
