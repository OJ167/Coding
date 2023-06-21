#Code to automate tank function

from cgitb import reset
import numpy as np

import os
from datetime import date
from tkinter import filedialog
import sys
import math as maths

import glob

import time
import serial

from simple_pyspin import Camera
from PIL import Image
import os

#### Declaring Global Variables ####
# port  = "COM14" # port that the Arduino is connected to - CHANGE THIS IF ARDUINO IS DISCONNECTED


#### Tank Properties ####
t = "Vortex Ring"  # Type of experiment
d = 0.05  # Diameter of Nozzle in m
vk = 0.000001  # Kinematic viscosity
l = 0.05  # Characteristic length (equal to nozzle diameter)

############# these change vortex generation ########################
Stroke =  50 # piston stroke in mm
Upiston = 100 # piston velocity in mm/s
Ring_Count = 5 # Number of rings to be generated
#####################################################################

#### Secondary tank principles ####
Delay = 10 # Delay between ring generations
RPM = 9 # Rotation rate used for saving data correctly
CameraFPS = 45 #camera framerate
frames = 100 #number of frames to capture
########

IndNotes = ""
notes = (
    "..."
)

#### Arduino Settings ####

arduino = serial.Serial(port = 'COM14', baudrate=9600, timeout=.1)

def write_read(driver_command): # writes commands to the Arduino from the PC
    arduino.write(bytes(driver_command, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


# Calculations
CSA = maths.pi * d**2 / 4 #Nozzle cross sectional area
Volume = Stroke/1000 * CSA #Fluid Volume per Injection in m
Q = Upiston/1000 * CSA #Flow Velocity at Nozzle in m/s(based on piston speed) 
Re = (Upiston/1000) * d / vk #Re0 = (U0*D0/nu)

if RPM == 0:
    Omega = 0
    Ek = 0
    Ro = 0
else:
    Omega = 2 * maths.pi * float(RPM) / 60
    Ek = vk / (2 * Omega * l**2)
    Ro = Upiston / (2 * Omega * l)


def command_converter(): # funcion to convert from physical units to vortex ring generator units
    arduino_Speed = Upiston * 10 # convert from speed to steps/s
    print("Speed " + str(Upiston) + "mm/s = " + str(arduino_Speed) + "steps")
    arduino_Steps =  Stroke * 10 # convert from displacement to steps
    print("Stroke " + str(Stroke) + "mm = " + str(arduino_Steps) + "steps")
    return arduino_Speed, arduino_Steps # return values for speed and steps in arduino format

def ring_control(Upiston, Stroke): # Function to control the arduino via serial communication, and also control the number of rings and generation parameters
    Command = "o" + " " + str(arduino_Steps) + " " + str(arduino_Speed)
    print("Command is: " + Command)
    write_read(Command)
    return Command

def piston_return(Upiston, Stroke): # moves piston back to the top of the cylinder ready to reset
    Command = "c" + " " + str(arduino_Steps) + " " + str(arduino_Speed)
    print("Command is: " + Command)
    write_read(Command)
    return Command

def file_conrtol(directoryNew): # function to automatically create the file structure for the remaining runs
    global number
    # Get todays date and convert to string
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    date_and_fps = str(d1 + f"__FPS-{CameraFPS}")   

    parameterDir = str("RPM-" + str(RPM) + "__Upiston-" + str(Upiston) + "__Stroke-" + str(Stroke))
    print(parameterDir)
    # Set root directory


    # Create directory within root with control parameters
    path1 = os.path.join(directoryNew, parameterDir)
    if os.path.exists(path1) == True:
        pass
    else:
        os.mkdir(path1) 

    # Create containing folder with date and fps
    folder = os.path.join(path1, date_and_fps)
    if os.path.exists(folder) == True:
        pass
    else:
        os.mkdir(folder)

    # Create final numbered containers - by counting up by one from currently existing folder
    number = str(1) 

    def count():
        global number
        if os.path.exists(os.path.join(folder, number)) == True:
            number = str(int(number) + 1)
            count()
        else:
            os.mkdir(os.path.join(folder, number))  

    count()
    print(number)
    finalDir = os.path.join(folder, number)
    os.mkdir(os.path.join(finalDir, "B"))
    os.mkdir(os.path.join(finalDir, "T"))
    os.mkdir(os.path.join(finalDir, "M"))
    os.mkdir(os.path.join(finalDir, "Var"))
    os.mkdir(os.path.join(finalDir, "Short"))
    os.mkdir(os.path.join(finalDir, "Data"))    

    # Create Text file with required variables
    file1 = open(os.path.join(finalDir, "Details.txt"), "w+")
    file1.write("Basic variables." + "\n" + "\n")
    file1.write("   - Table RPM  =  " + str(RPM) + "\n")
    file1.write("   - Piston Speed  =  " + str(Upiston) + "\n")
    file1.write("   - Piston Stroke  =  " + str(Stroke) + "\n")
    file1.write(
        "   - FPS Camera  =  "
        + str(CameraFPS)
        + "\n"
        + "\n"
        + "Calculated variables."
        + "\n"
        + "\n"
    )
    file1.write("   - Omega = " + str(round(Omega, 3)) + " rad/s" + "\n")
    file1.write(
        "   - Q = "
        + str(round(Q, 9))
        + " m^3/s = "
        + str(round(Q * 1000, 6))
        + " l/s "
        + str(round(Q * 1000000, 9))
        + " cm^3/s"
        + "\n"
    )
    file1.write("   - U = " + str(round(Upiston/1000, 5)) + " m/s" + "\n")
    file1.write("   - Re = " + str(round(Re, 5)) + "\n")
    file1.write("   - Ro = " + str(round(Ro, 5)) + "\n")
    file1.write("   - Ek = " + str(round(Ek, 9)) + "\n" + "\n" + "Notes." + "\n")
    file1.write(notes + "\n")
    file1.write(str(IndNotes))
    file1.close()
    print("final dir " + str(finalDir))
    return finalDir
    print("file 1 " + str(file1))
    print("file dir " + str(finalDir))

def camera_control(finalDir): # function to trigger the camera recording and save to the right location
    with Camera() as cam: # Initialize Camera
        cam.start() # Start recording
        imgs = [cam.get_array() for n in range(frames)]
        cam.stop() # Stop recording

    # Make a directory to save some images
    output_dir = finalDir + "\B"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Saving images to: %s" % output_dir)

    # Save them
    # NOTE: images may be very dark or bright, depending on the camera lens and
    #   room conditions!
    for n, img in enumerate(imgs):
        Image.fromarray(img).save(os.path.join(output_dir, '%08d.png' % n))

def Ring_Generator(): # function to run the tank including the delay.
    global arduino_Speed, arduino_Steps
    arduino_Speed, arduino_Steps = command_converter()
    directoryNew = filedialog.askdirectory()

    for i in range(Ring_Count):
        finalDir = file_conrtol(directoryNew)
        ring_control(arduino_Speed, arduino_Steps)
        camera_control(finalDir)
        time.sleep(Delay)
        piston_return(arduino_Speed, arduino_Steps)

Ring_Generator()
# directoryNew = filedialog.askdirectory()
# file_conrtol(directoryNew)
# print(file_conrtol(directoryNew))

######################### Testing Area #########################

# def my_function(person):
#     print(str(person) + " hello")

# my_function("sean")

# x = input("how many rings? ")

# def get_even(numbers):
#      even_nums = [num for num in numbers if not num % 2]
#      return even_nums

# v = [1, 2, 3, 4, 5, 6]

# even_v = get_even(v)
# print(even_v)



# def add_one(x):
#     result = x + 1
#     return result

# print(add_one(3))

######################### Testing Area #########################