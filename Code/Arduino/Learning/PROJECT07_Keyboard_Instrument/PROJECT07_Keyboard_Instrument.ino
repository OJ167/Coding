//creating an array of note frequencies (CEGB)
int notes[] = {261, 329, 392, 523};

void setup() {
  // put your setup code here, to run once:

//start communication with the computer
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

int inputValue = analogRead(A0);
Serial.println(inputValue);

if(inputValue>= 1015){
  tone(8, notes[3]);
}
else if(inputValue >= 990 && inputValue<= 1010){
  tone(8, notes[2]);
}
else if(inputValue >= 500 && inputValue <= 520){
  tone(8, notes[1]);
}
else if(inputValue >= 2 && inputValue <= 30){
  tone(8, notes[0]);
}
else{
  noTone(8);
}
}
