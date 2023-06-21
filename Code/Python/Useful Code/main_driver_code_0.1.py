

####
# main code to run the vortex ring generator.
# this code is intended to take inputs from user, calculate ring properties, generate a folder structure, and then command the vortex ring generator. 
# the vortex ring generator will be controlled by the arduino, this code will simply pass the message to the arduino by serial communication.
# function - make file structure
# function - calculate ring properties from user input
# function - serial communication (might not be able to make this a function)

#   Arduino Requires:
#      Direction
#      Speed
#   Acceleration
####


number_of_rings = input("How many rings?: ")
injection_volume = input("Volume of rings?: ")
piston_speed = input("Piston speed: ")

print(number_of_rings)
print(injection_volume)
print(piston_speed)


step_distance = xxxxxxxx #Distance piston moves with a single step.
piston_area = xxxxxxxxxx #Cross sectional area of piston.
step_volume = xxxxxxxxxxx #Volume of a single step (step distance * piston area).
step_number = injection_volume / step_volume #Number of steps required

step_time = xxxxxxxxxx #Time for a single step - 1/step time = steps/second.
step_rate = 1 / step_time #Number of steps per second.
injection_speed = step_rate * step_number


current_ring = #How many rings have been shot.
