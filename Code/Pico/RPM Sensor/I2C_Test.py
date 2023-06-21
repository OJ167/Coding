import utime
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


I2C_ADDR     = 0x27 
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

def greeting():
    
    lcd.backlight_on()
    lcd.move_to(5,0)
    lcd.putstr("Welcome")
    lcd.move_to(3,1)
    lcd.putstr("To NerdCave")
    utime.sleep(2)

    
greeting()
print(I2C_ADDR)
