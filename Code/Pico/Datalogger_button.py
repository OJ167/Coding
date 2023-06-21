import machine
import utime


button = machine.Pin(13, machine.Pin.IN)
file = open("buttonFFT.csv", "w")

while True:

    file.write(str(button.value()) + ", " + str(utime.ticks_us()) + "\n")
    print(button.value())


print('done')
file.close()

