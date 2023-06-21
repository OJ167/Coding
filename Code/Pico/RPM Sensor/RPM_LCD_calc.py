#Importing required libraries
import machine
import utime
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


#Global Variables
RPM = 0
signalPin = machine.Pin(13, machine.Pin.IN)
flag_value = 0
flag_limit = 120 #This value sets the number of ticks before display is updated
pulses_per_revolution = 120 #Number of pulses per revolution NOT THE NUMBER OF TEETH!!!
normalisedFlagLimit = flag_limit/pulses_per_revolution #Normalise the flag limit against number of pulses for one revolution

#Time Variables
startTime = utime.ticks_us()
endTime = 0
timeNormaliser = 60000000 #Change this number based on what time increment is used
                          #(60*10^x where x is the inverse power of the time incriment)
                          #currently using microseconds therefore x = 6
calcTime = 1

#LCD Variables

SDA_PIN = 0
SCL_PIN = 1
I2C_ADD = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN), freq=200000)
lcd = I2cLcd(i2c, I2C_ADD, I2C_NUM_ROWS, I2C_NUM_COLS)

# Print the meme string
lcd.putstr("That's a good trick!")
utime.sleep(2)
#lcd.clear() #this line might not be needed

#ISR: add one to the count
def sensorISR(Pin):
    global flag_value
    flag_value += 1
    #print('ISR Active, ' + str(flag_value))
    
#Printing to the screen
def screen_update():
    #update the display using I2C, and reset flag and time values
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr('RPM:')
    lcd.move_to(0,1)
    lcd.putstr(str(RPM))

#attach pin to interrupt
signalPin.irq(trigger = machine.Pin.IRQ_FALLING|machine.Pin.IRQ_RISING, handler = sensorISR)



###############
###Run loop - waiting for enough interrupt triggers
###############

while True:
    if flag_value == flag_limit: #This sets the limit for how many ticks before new value is displayed
        
        endTime = utime.ticks_us() #find the time that the loop ended
        flag_value = 0 #Reset flag value to 0
        deltaTime = endTime - startTime #Amount of time taken for that many interrupts
        normalisedDeltaTime = deltaTime/timeNormaliser #Normalising time based on time incriment
        RPM = (normalisedFlagLimit / normalisedDeltaTime) * (1- (calcTime/deltaTime)) #Calculating RPM and removing calculation time
        screen_update()
        calcTime = utime.ticks_us() - endTime #Finds time taken to run the loop
        startTime = utime.ticks_us() #Keep this at the end to improve accuracy

    else:
        pass