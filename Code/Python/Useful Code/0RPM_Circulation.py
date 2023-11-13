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



h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][Injection[0]][Stroke[0]][str(Rotations[0])]
u5050 = vels[:,:,:,0]
v5050 = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][Injection[1]][Stroke[0]][str(Rotations[0])]
u10050 = vels[:,:,:,0]
v10050 = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][Injection[0]][Stroke[1]][str(Rotations[0])]
u50100 = vels[:,:,:,0]
v50100 = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][Injection[1]][Stroke[1]][str(Rotations[0])]
u100100 = vels[:,:,:,0]
v100100 = vels[:,:,:,1]


time = oj.frames_to_seconds(u5050, u5050, 90)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u5050.shape[1], u5050.shape[2])

sumVorticity5050    = oj.sum_Vorticity(u5050   [:,:,18:], v5050 [:,:,18:])
sumVorticity10050   = oj.sum_Vorticity(u10050  [:,:,18:], v10050 [:,:,18:])
sumVorticity50100   = oj.sum_Vorticity(u50100  [:,:,18:], v50100 [:,:,18:])
sumVorticity100100  = oj.sum_Vorticity(u100100 [:,:,18:], v100100 [:,:,18:])


f2, ax2 = plt.subplots(nrows=1, ncols=1)
plt.title("Vortex Ring Circulation 0 RPM")
ax2.plot(time, sumVorticity5050,    label = "Speed 50,  stroke: 50" )
ax2.plot(time, sumVorticity10050,   label = "Speed 100, stroke: 50" )
ax2.plot(time, sumVorticity50100,   label = "Speed 50,  stroke: 100" )
ax2.plot(time, sumVorticity100100,  label = "Speed 100, stroke: 100" )
ax2.set_xlabel("time [s]")
ax2.set_ylabel("$\Gamma \: [cm^{2}s^{-1}]$")
plt.legend()
plt.show()