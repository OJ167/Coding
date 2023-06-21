void setup() {
  // put your setup code here, to run once:
  pinMode(7, OUTPUT);
  digitalWrite(7, HIGH);

  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  handleSerial(); //function to handle serial monitor
}


void handleSerial() { //Serial monitor function
  while (Serial.available() > 0) {

    char    msg = Serial.read();
    Serial.println(msg);
    switch (msg) {
      case'H':
      case'h':
        digitalWrite(7, HIGH);
        Serial.println("LED ON");
        break;

      case'W':
      case'w':
        digitalWrite(7, LOW);
        Serial.println("LED OFF");
    }
  }
}
