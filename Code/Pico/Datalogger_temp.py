import machine
import utime

sensor_temp = machine.ADC(machine.ADC.CORE_TEMP)
time_start = utime.time()
newtime = utime.time() - time_start

conversion_factor = 3.3/65535
file = open("adding.csv", "w")
while newtime < 5:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    #tup = temperature, utime.ticks_us()
    #list.append(tup)
    file.write(str(temperature) + ", " + str(utime.ticks_us()) + "\n")
    #file.flush()
    #file.write(str(tup) + "\n")
    newtime = utime.time() - time_start

print('done')
file.close()