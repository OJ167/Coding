import numpy as np
import os
import sys
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import pandas as pd
import matplotlib.colors as colors
import matplotlib.cm
import h5py
from matplotlib import animation
from scipy.fft import fft, fftfreq, rfft, rfftfreq
# from colorspacious import cspace_converter

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)


####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

# oj.tic()
# h5file = h5py.File('E:/H5/3D0meandataHLS.h5', 'r')
h5file = h5py.File('E:/H5/3D0HLSFine.h5', 'r')


frame = 750
frametime = frame/150
d = 0.1
vels = h5file['3D0']['U100']['L100']['RPM3']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
# h5file.close()
u_gaussian, v_gaussian = gaussian_filter(u, sigma=6), gaussian_filter(v, sigma=6)
time = oj.frames_to_seconds(u, v, 150)
print(u.shape[0], u.shape[1], u.shape[2])

rpm = np.array([0, 1, 2, 3, 6, 9, 12])


### This is a test section where I figure out the Maths of the normalisation. The maths on the x axis of the third graph is correct
FPS = 150

rot1 = 1 #1 rpm 
rate1 = rot1/60

rot2 = 12 #2 rpm
rate2 = rot2/60

x = np.linspace(0, 3000, 3000)
y1 = np.sin(2*2*np.pi*x*rot1)
y2 = np.sin(2*2*np.pi*x*rot2)

f1, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols = 3)
ax1.set_title('not normalised')
ax1.plot(x/FPS, y1, label = 'y1')
ax1.plot(x/FPS, y2, label = 'y2')
ax2.set_title('normalised by rpm')
ax2.plot(x*rot1/FPS, y1, 'o--', label = 'y1')
ax2.plot(x*rot2/FPS, y2, label = 'y2')
ax3.set_title('normalised by rotation rate')
ax3.plot(x*rate1/FPS, y1, 'o--', label = 'y1')
ax3.plot(x*rate2/FPS, y2, label = 'y2')
ax3.set_xlabel('number of rotations')
plt.legend()
# plt.show()

###################################################################################################
##### Radial against time
###################################################################################################

x = np.linspace(0 , u.shape[2], u.shape[2])
y = np.linspace(0 , u.shape[1], u.shape[1])
X, Y = np.meshgrid(x, y) 


# r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u_gaussian[frame,:,:], v_gaussian[frame,:,:])
# r_arr, theta_arr, U_rBins, U_azBins = oj.binCylindrical(r, theta, U_r, U_az, thetaBins=30, rBins=45)
# inds = (r.flatten()).argsort()
# r2 = (r.flatten())[inds]
# U_r2 = (U_r.flatten())[inds]
# pr = np.poly1d(np.polyfit(r2, U_r2, 11))(r2) #This turns the graph into a polynomial line


radial_Position = np.zeros(u.shape[0])
U_r_Mean = np.zeros(u.shape[0])
U_r_Peak = np.zeros(u.shape[0])

for i in range(u.shape[0]):
# for i in range(10): # for testing
    r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u_gaussian[i,:,:], v_gaussian[i,:,:])
    inds = (r.flatten()).argsort()
    r2 = (r.flatten())[inds]
    U_r2 = (U_r.flatten())[inds]
    p = np.poly1d(np.polyfit(r2, U_r2, 11))(r2) #This turns the graph into a polynomial line
    # max = np.argmax(U_az2)
    max = np.argmax(p)
    U_r_Mean[i] = np.mean(U_r2)
    U_r_Peak[i] = np.max(U_r2)
    radial_Position[i] = max


# rate = rpm[6]/60

# f5, ax = plt.subplots(2, 2)
# plt.suptitle("Radial Velocity Graphs")
# ax[0,0].plot(pr)
# ax[0,0].set_title(r"$U_{r}$ Polynomial" + f" - Time = {frametime}")
# ax[0,0].set_xlabel("$r/d$")
# ax[0,0].set_ylabel(r"$U_{r}$")
# ax[0,1].plot(time*rate, U_r_Mean)
# ax[0,1].set_title(r"$U_{r}$ Mean/time")
# ax[0,1].set_xlabel("$Time [s]$")
# ax[0,1].set_ylabel(r"$\bar{U}_{r}$")
# ax[1,0].plot(time, U_r_Peak)
# ax[1,0].set_title(r"$U_{r}$ Peak/time")
# ax[1,0].set_xlabel("$Time [s]$")
# ax[1,0].set_ylabel(r"$U_{r} Peak$")
# ax[1,1].plot(time, radial_Position)
# ax[1,1].set_title(r"$U_{r}$ Peak location")
# ax[1,1].set_xlabel("not defined")
# ax[1,1].set_ylabel("radial location")
# plt.show()

radial_Positionr = np.zeros([7, u.shape[0]])
U_r_Mean =         np.zeros([7, u.shape[0]])
U_r_Peak =         np.zeros([7, u.shape[0]])

radial_Positionaz = np.zeros([7, u.shape[0]])
U_az_Mean =         np.zeros([7, u.shape[0]])
U_az_Peak =         np.zeros([7, u.shape[0]])

oj.tic()
for i in range(len(rpm)):
# for i in range(2):
    print('RPM{0}'.format(rpm[i]))
    vels = h5file['3D0']['U100']['L100']['RPM{0}'.format(rpm[i])]
    u = vels[:,:,:,0]
    v = vels[:,:,:,1]
    u_gaussian, v_gaussian = gaussian_filter(u, sigma=6), gaussian_filter(v, sigma=6)

    for j in range(u.shape[0]):
        r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u_gaussian[j,:,:], v_gaussian[j,:,:])
        inds = (r.flatten()).argsort()
        r2 = (r.flatten())[inds]
        U_r2 = (U_r.flatten())[inds]
        pr = np.poly1d(np.polyfit(r2, U_r2, 11))(r2) #This turns the graph into a polynomial line
        U_r_Mean[i, j] = np.mean(U_r2)
        U_r_Peak[i, j] = np.max(U_r2)
        radial_Positionr[i, j] = np.argmax(pr)

        U_az2 = (U_az.flatten())[inds]
        paz = np.poly1d(np.polyfit(r2, U_az2, 11))(r2) #This turns the graph into a polynomial line
        U_az_Mean[i, j] = np.mean(U_az2)
        U_az_Peak[i, j] = np.max(U_az2)
        radial_Positionaz[i, j] = np.argmax(paz)

oj.toc()    

rate = np.zeros(7)
for i in range(len(rpm)):
    rate[i] = rpm[i]/60


f5, ax = plt.subplots(2, 2)
plt.suptitle("Radial Velocity Graphs")
ax[0,0].plot(time, U_r_Mean[1,:])
ax[0,0].set_title(r"$U_{r}$ Polynomial" + f" - Time = {frametime}")
ax[0,0].set_xlabel("$r/d$")
ax[0,0].set_ylabel(r"$U_{r}$")
ax[0,1].plot(time*rate[1], U_r_Mean[1,:], label = '1RPM')
ax[0,1].plot(time*rate[2], U_r_Mean[2,:], label = '2RPM')
ax[0,1].plot(time*rate[3], U_r_Mean[3,:], label = '3RPM')
ax[0,1].plot(time*rate[4], U_r_Mean[4,:], label = '6RPM')
ax[0,1].plot(time*rate[5], U_r_Mean[5,:], label = '9RPM')
ax[0,1].plot(time*rate[6], U_r_Mean[6,:], label = '12RPM')
ax[0,1].legend()
ax[0,1].set_title(r"$U_{r}$ Mean/time")
ax[0,1].set_xlabel("$Number of Rotations$")
ax[0,1].set_ylabel(r"$\bar{U}_{r}$")
ax[1,0].plot(time, U_r_Peak[1,:])
ax[1,0].set_title(r"$U_{r}$ Peak/time")
ax[1,0].set_xlabel("$Time [s]$")
ax[1,0].set_ylabel(r"$U_{r} Peak$")
ax[1,1].plot(time, radial_Positionr[1,:])
ax[1,1].set_title(r"$U_{r}$ Peak location")
ax[1,1].set_xlabel("not defined")
ax[1,1].set_ylabel("radial location")

f6, ax7 = plt.subplots()
plt.suptitle("Radial Velocity Graphs")
ax7.plot(time*rate[1], U_r_Mean[1,:], label = '1RPM')
ax7.plot(time*rate[2], U_r_Mean[2,:], label = '2RPM')
ax7.plot(time*rate[3], U_r_Mean[3,:], label = '3RPM')
ax7.plot(time*rate[4], U_r_Mean[4,:], label = '6RPM')
ax7.plot(time*rate[5], U_r_Mean[5,:], label = '9RPM')
ax7.plot(time*rate[6], U_r_Mean[6,:], label = '12RPM')
ax7.legend()
ax7.set_title(r"$U_{r}$ Mean/time")
ax7.set_xlabel("$Number of rotations$")
ax7.set_ylabel(r"$\bar{U}_{r}$")


f7, ax8 = plt.subplots()
plt.suptitle("Azimuthal Velocity Graphs")
ax8.plot(time*rate[1], U_az_Mean[1,:], label = '1RPM')
ax8.plot(time*rate[2], U_az_Mean[2,:], label = '2RPM')
ax8.plot(time*rate[3], U_az_Mean[3,:], label = '3RPM')
ax8.plot(time*rate[4], U_az_Mean[4,:], label = '6RPM')
ax8.plot(time*rate[5], U_az_Mean[5,:], label = '9RPM')
ax8.plot(time*rate[6], U_az_Mean[6,:], label = '12RPM')
ax8.legend()
ax8.set_title(r"$U_{az}$ Mean/time")
ax8.set_xlabel("$Number of rotations$")
ax8.set_ylabel(r"$\bar{U}_{az}$")



f9, ax10 = plt.subplots()
plt.suptitle("Radial Velocity Graphs")
ax10.plot(time*rate[1], U_r_Peak[1,:], label = '1RPM')
ax10.plot(time*rate[2], U_r_Peak[2,:], label = '2RPM')
ax10.plot(time*rate[3], U_r_Peak[3,:], label = '3RPM')
ax10.plot(time*rate[4], U_r_Peak[4,:], label = '6RPM')
ax10.plot(time*rate[5], U_r_Peak[5,:], label = '9RPM')
ax10.plot(time*rate[6], U_r_Peak[6,:], label = '12RPM')
ax10.legend()
ax10.set_title(r"$U_{r}$ Peak/time")
ax10.set_xlabel("$Number of rotations$")
ax10.set_ylabel(r"$U_{r}$")


f10, ax11 = plt.subplots()
plt.suptitle("Azimuthal Velocity Graphs")
ax11.plot(time*rate[1], U_az_Peak[1,:], label = '1RPM')
ax11.plot(time*rate[2], U_az_Peak[2,:], label = '2RPM')
ax11.plot(time*rate[3], U_az_Peak[3,:], label = '3RPM')
ax11.plot(time*rate[4], U_az_Peak[4,:], label = '6RPM')
ax11.plot(time*rate[5], U_az_Peak[5,:], label = '9RPM')
ax11.plot(time*rate[6], U_az_Peak[6,:], label = '12RPM')
ax11.legend()
ax11.set_title(r"$U_{az}$ Peak/time")
ax11.set_xlabel("$Number of rotations$")
ax11.set_ylabel(r"$U_{az}$")
plt.show()
