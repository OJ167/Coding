void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  String msg = "";
  if (Serial.available() > 0)
  {
    while (Serial.available() > 0)
    {
      msg += char(Serial.read());
      delay(250);
    }
  }
  Serial.print(msg + "!");
  // Serial.print("!");
}
