//attempt 1 to drive vortex generator properly


// User Variables

int injectionVAR = 1; // User input for "P" value (Pmax = 1.375)
int onerevSTEPS = 12800; // Number of steps based on stepper driver setting
int velocity = 1000; // Piston velocity [mm/s]

//Pin Definitions

int driverSTEP = 7;    // STEP- pin
int driverDIR = 6;    // DIR- pin (LOW = down, HIGH = up)

// Global Variables

boolean driverVAL = LOW; // Boolean logic command to change the direction.
int diameterNOZZLE = 50; // Nozzle Diameter [mm]
int stepDIST = 100 / onerevSTEPS; //Distance traveled by a single step [mm]

//Derived variables

int injectionLENGTH = pow(injectionVAR, 3) * diameterNOZZLE; //Distance of piston travel [mm]
int numberSTEPS = injectionLENGTH / stepDIST; //calculated number of steps required
int pulseTIME = injectionLENGTH / 2 * velocity * numberSTEPS; //time for each pin pulse (needs to be used in MICROSECONDS)

void setup() {
  // put your setup code here, to run once:

  pinMode (driverSTEP, OUTPUT); //Set step pin as output
  pinMode (driverDIR, OUTPUT); //Set direction pin as output
  Serial.begin(9600); //begin serial monitor

  Serial.println(injectionLENGTH);
  Serial.println(pulseTIME);
}

void loop() {
  // put your main code here, to run repeatedly:

  digitalWrite(driverSTEP, HIGH);
  delayMicroseconds(pulseTIME);
  Serial.println(driverSTEP);
  digitalWrite(driverSTEP, LOW);
  delayMicroseconds(pulseTIME);
  Serial.println("driverSTEP");
}
