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
    String msg = "";
    if (Serial.available() > 0)
    {

      msg = Serial.readString();

      Serial.println(msg);
    }

    if (msg == "hello")
    {
      digitalWrite(13, HIGH);
      Serial.println("LED ON");
    }
    else if (msg == "world")
    {
      digitalWrite(13, LOW);
      Serial.println("LED OFF");
    }
  }
}
