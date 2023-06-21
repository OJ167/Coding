
//  Stepper Motor Test
//  stepper-test01.ino
//  Uses MA860H or similar Stepper Driver Unit

// Pin Definitions

int reverseSwitch = 2;  // Push button for reverse
int driverSTEP = 7;    // STEP- pin
int driverDIR = 6;    // DIR- pin

// Global Variables

int pd = 50000;       // Step Delay period
boolean driverVAL = LOW;

void setup() {

  pinMode (driverSTEP, OUTPUT);
  pinMode (driverDIR, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  delay(1000);

  for (int x = 0; x <= 1000; x++) {


    if ( x < 1000) {
      digitalWrite(driverSTEP, HIGH);
      delayMicroseconds(pd);
      digitalWrite(driverSTEP, LOW);
      delayMicroseconds(pd);
      Serial.println(driverVAL);
      Serial.println(driverSTEP);
    }
  }
  driverVAL = !driverVAL;
  digitalWrite(driverDIR, driverVAL);
}
