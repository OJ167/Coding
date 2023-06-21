int switchPin = 8;
unsigned long previousTime = 0;
int switchState = 0;
int prevSwitchState = 0;
int led = 2;
long interval = 60000;

void setup() {
  // put your setup code here, to run once:

  for(int pinNumber = 2; pinNumber<8; pinNumber++){
    pinMode(pinNumber, OUTPUT);
  }
pinMode(switchPin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

unsigned long currentTime = millis();
  
  if(currentTime - previousTime >= interval){
  previousTime = currentTime;
  digitalWrite(led, HIGH);
  led++;
  if(led == 7){
  }
  }
  switchState = digitalRead(switchPin);
  
  if(switchState != prevSwitchState){
    for(int pinNumber = 2; pinNumber<8; pinNumber++){
      digitalWrite(pinNumber, LOW);
    }
    led = 2;
    previousTime = currentTime;
    }
  prevSwitchState = switchState;
   
}
