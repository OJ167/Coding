# sender.py
import time
import serial
ser = serial.Serial(
  port='COM11', # Change this according to connection methods, e.g. /dev/ttyUSB0
  baudrate = 9600, #Change according to port settings
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)
msg = ""
i = 0
while True:
    i+=1
    print("Counter {} - Hello from PC".format(i))
    ser.write('hello'.encode('utf-8'))
    time.sleep(2)