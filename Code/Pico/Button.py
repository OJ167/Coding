#gp13

import machine
import utime
Button = machine.Pin(13, machine.Pin.IN)
LED_Onboard = machine.Pin(25, machine.Pin.OUT)
LED_Onboard.value(0)
        
while True:
    if Button.value() == 1:
        print("You're a Cunt!")
        LED_Onboard.value(1)
        utime.sleep(0.01)
        LED_Onboard.value(0)