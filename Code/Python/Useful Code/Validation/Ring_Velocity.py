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

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])

Rotations = ['RPM0', 'RPM1', 'RPM2', 'RPM3', 'RPM6', 'RPM9', 'RPM12']
Injection = ['U50', 'U100']
Stroke = ['L50', 'L100']
I = 'U100'
S = 'L100'


h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[0])]
u0mean = vels[:,:,:,0]
v0mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[1])]
u1mean = vels[:,:,:,0]
v1mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[2])]
u2mean = vels[:,:,:,0]
v2mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[2])]
u3mean = vels[:,:,:,0]
v3mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[4])]
u6mean = vels[:,:,:,0]
v6mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[5])]
u9mean = vels[:,:,:,0]
v9mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[6])]
u12mean = vels[:,:,:,0]
v12mean = vels[:,:,:,1]

time = oj.frames_to_seconds(u0mean, v0mean, 90)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u0mean.shape[1], u0mean.shape[2])

u0mean, v0mean = oj.scaleVel(u0mean, v0mean, 90)

VortLocMax, VortLocMin = oj.vorticityPeakTracking(u0mean, v0mean)

f1, ax1 = plt.subplots()
ax1.plot(time, VortLocMax[:,1], label = "Max")
ax1.plot(time, VortLocMin[:,1], label = "Min")
# plt.show()

VortLocMean = np.mean(np.array([ VortLocMax, VortLocMin ]), axis=0)

f2, ax2 = plt.subplots()
ax2.plot(time, VortLocMax[:,1], label = "Max")
ax2.plot(time, VortLocMin[:,1], label = "Min")
ax2.plot(time, VortLocMean[:,1], label = "Mean")
plt.legend()
plt.show()


VortSpeed = np.gradient(VortLocMean[:,1])
print(VortSpeed.shape)

f3, ax3 = plt.subplots()
ax3.plot(time, VortSpeed[:], label = "Max")
plt.legend()




f4, ax4 = plt.subplots()
cbar = ax4.contourf(u0mean[600,:,:])
f4.colorbar(cbar, ax=ax4)
plt.show()