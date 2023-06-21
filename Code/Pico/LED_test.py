import machine
led_onboard = machine.Pin(25, machine.Pin.OUT)
led_onboard.value(0)