void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);

  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0);
  {
    char Letter = Serial.read();

    if (Letter == '1')
    {
      digitalWrite(13, HIGH);
      Serial.println("LED ON");
    }
    else if (Letter == '0')
    {
      digitalWrite(13, LOW);
      Serial.println("LED OFF");
    }
  }
}
