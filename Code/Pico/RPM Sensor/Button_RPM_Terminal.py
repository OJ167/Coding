#Importing required libraries
import machine
import utime

#Global Variables
signalPin = machine.Pin(13, machine.Pin.IN)
flag_value = 0
flag_limit = 10 #This value sets the number of ticks before display is updated
pulses_per_revolution = 100 #Number of pulses per revolution NOT THE NUMBER OF TEETH!!!
normalisedFlagLimit = flag_limit/pulses_per_revolution #Normalise the flag limit against number of pulses for one revolution

#Time Variables
startTime = utime.ticks_us()
endTime = 0
timeNormaliser = 60000000 #Change this number based on what time increment is used
                          #(60*10^x where x is the inverse power of the time incriment)
                          #currently using microseconds therefore x = 6

RPM = 0

#ISR: add one to the count
def sensorISR(Pin):
    global flag_value
    flag_value += 1
    print('ISR Active')

#attach pin to interrupt
signalPin.irq(trigger = machine.Pin.IRQ_FALLING|machine.Pin.IRQ_RISING, handler = sensorISR)

#|machine.Pin.IRQ_FALLING
#|machine.Pin.IRQ_RISING

#Run loop - waiting for enough interrupt triggers
while True:
    if flag_value < flag_limit: #This sets the limit for how many ticks before new value is 
        pass
    
    else:
        
        endTime = utime.ticks_us() #find the time that the loop ended
        flag_value = 0 #Reset flag value to 0
        deltaTime = endTime - startTime #Amount of time taken for that many interrupts
        normalisedDeltaTime = deltaTime/timeNormaliser #Normalising time based on time incriment
        RPM = (normalisedFlagLimit / normalisedDeltaTime) #Calculating RPM
        
        
        print('RPM = ' + str(RPM))

    
        #update the display using I2C, and reset flag and time values
        
    
        startTime = utime.ticks_us() #Keep this at the end to improve accuracy