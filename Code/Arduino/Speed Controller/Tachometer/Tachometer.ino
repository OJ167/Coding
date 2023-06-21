
float value=0;
float rev=0;
int rpm;
int oldtime=0;        
int time;

void isr()          //interrupt service routine
{
rev++;
}

void setup()
{
attachInterrupt(2,isr,RISING);  //attaching the interrupt
Serial.begin(9600);
}

void loop()
{
delay(2000);// 2 second delay
detachInterrupt(0);           //detaches the interrupt while calculating
time=millis()-oldtime;        //finds the time 
rpm=(rev/time)*60000;         //calculates rpm
oldtime=millis();             //saves the current time
rev=0;
attachInterrupt(2,isr,RISING);

Serial.println(rpm);
}
