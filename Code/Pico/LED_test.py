import machine
import time

led_onboard = machine.Pin(25, machine.Pin.OUT)

while True:
    led_onboard.value(0)
    time.sleep_ms(1000)
    led_onboard.value(1)
    time.sleep_ms(1000)