int x;

void setup() {
 Serial.begin(9600);
 Serial.setTimeout(1);
 pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 //Serial.print(x + 1);

 digitalWrite(LED_BUILTIN, HIGH);
 delay(1000*x);
 digitalWrite(LED_BUILTIN, LOW);
 delay(1000*x);
}
