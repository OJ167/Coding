import machine
import utime


signal = machine.Pin(13, machine.Pin.IN)
file = open("signalFFT.csv", "w")

while True:

    file.write(str(signal.value()) + ", " + str(utime.ticks_us()) + "\n")

print('done')
file.close()

