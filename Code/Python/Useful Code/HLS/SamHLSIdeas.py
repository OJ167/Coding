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


# h5file = h5py.File('E:/H5/3D0meandataHLS.h5', 'r')
h5file = h5py.File('E:/H5/3D0HLSFine.h5', 'r')

frame = 1000
d = 0.1
vels = h5file['3D0']['U100']['L100']['RPM9']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
h5file.close()
u_gaussian, v_gaussian = gaussian_filter(u, sigma=6), gaussian_filter(v, sigma=6)
time = oj.frames_to_seconds(u, v, 150)
print(u.shape[0], u.shape[1], u.shape[2])

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)


x = 55
y = 35
x = np.linspace(0 , umean.shape[1], umean.shape[1])
y = np.linspace(0 , umean.shape[0], umean.shape[0])
X, Y = np.meshgrid(x, y) 




r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u_gaussian[frame,:,:], v_gaussian[frame,:,:])
r_arr, theta_arr, U_rBins, U_azBins = oj.binCylindrical(r, theta, U_r, U_az, thetaBins=30, rBins=45)
inds = (r.flatten()).argsort()
r2 = (r.flatten())[inds]
U_az2 = (U_az.flatten())[inds]
pf = np.poly1d(np.polyfit(r2, U_az2, 11))(r2) #This turns the graph into a polynomial line
# max = np.argmax(p)
max = np.max(pf)
print(max)

f3, ax3 =plt.subplots()
# ax3.scatter(r2*d, U_az2)
ax3.plot(r2*d, pf)
ax3.set_xlabel("$r/d$")
ax3.set_ylabel("$U_{az}$")

f1, ax = plt.subplots(2, 2,)
ax[0,0].scatter(r2*d, U_az)
ax[0,0].set_title("U_az")
ax[0,1].scatter(r2*d, U_az2)
ax[0,1].set_title("U_az2")
ax[1,0].scatter(r2*d, pf)
ax[1,0].set_title("Pf")
ax[1,1].plot(r_arr, np.mean(U_azBins, axis = 1))
ax[1,1].set_title("Uaz_bins")

f2, ax2 = plt.subplots()
ax2.imshow(U_azBins, cmap = "seismic")
# plt.show()



#### Averaging the value frame by frame and seeing what happens

radial_Position = np.zeros(u.shape[0])
U_az_Mean = np.zeros(u.shape[0])
U_az_Peak = np.zeros(u.shape[0])

for i in range(u.shape[0]):
# for i in range(10): # for testing
    r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u_gaussian[i,:,:], v_gaussian[i,:,:])
    inds = (r.flatten()).argsort()
    r2 = (r.flatten())[inds]
    U_az2 = (U_az.flatten())[inds]
    p = np.poly1d(np.polyfit(r2, U_az2, 11))(r2) #This turns the graph into a polynomial line
    max = np.argmax(p)
    U_az_Mean[i] = np.mean(p)
    U_az_Peak[i] = np.max(p)

print(U_az_Mean)
print(U_az_Peak)

f3, ax3 = plt.subplots()
ax3.plot(U_az_Mean, label = "Uaz Mean")
# ax3.set_label("Uaz Mean")
ax3.plot(U_az_Peak, label = "Uaz Peak")
# ax3.set_label()
ax3.plot(r2*d, pf, label = "p")
plt.legend()




f4, ax = plt.subplots(2, 2,)
ax[0,0].plot(r2*d, pf)
ax[0,0].set_title("U_az Polynomial - single frame")
ax[0,1].plot(time, U_az_Mean)
ax[0,1].set_title("Uaz Mean/time")
ax[1,0].plot(time, U_az_Peak)
ax[1,0].set_title("Uaz Peak/time")
ax[1,1].plot()
ax[1,1].set_title("U_az_Peak location")
plt.show()
