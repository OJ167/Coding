  int IR_Sensor = 2;
  
void setup() {
  // put your setup code here, to run once:
  //attachInterrupt(digitalPinToInterrupt (2), beam, FALLING);
  pinMode(IR_Sensor, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

if(digitalRead(IR_Sensor) == 1){ 
digitalWrite(LED_BUILTIN, HIGH);
}

else if(digitalRead(IR_Sensor) == 0){
  digitalWrite(LED_BUILTIN, LOW);
}
Serial.println(digitalRead(IR_Sensor));
}
