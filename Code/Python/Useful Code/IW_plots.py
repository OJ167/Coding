import numpy as np
import os
import sys
import h5py
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import pandas as pd
import matplotlib.colors as colors
import matplotlib.cm
# from colorspacious import cspace_converter

#####Import Ollie Tools
# dirPath = "C:/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)


####Import Ollie Tools MAC
dirPath = "/Users/olliejackson/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("jet_r")

Rotations = ['RPM0', 'RPM1', 'RPM2', 'RPM3', 'RPM6', 'RPM9', 'RPM12']
Injection = ['U50', 'U100']

h5file = h5py.File('/Volumes/T7/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[0])]
u0mean = vels[:,:,:,0]
v0mean = vels[:,:,:,1]

h5file = h5py.File('/Volumes/T7/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[1])]
u1mean = vels[:,:,:,0]
v1mean = vels[:,:,:,1]

h5file = h5py.File('/Volumes/T7/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[2])]
u2mean = vels[:,:,:,0]
v2mean = vels[:,:,:,1]

h5file = h5py.File('/Volumes/T7/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[3])]
u3mean = vels[:,:,:,0]
v3mean = vels[:,:,:,1]

h5file = h5py.File('/Volumes/T7/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[4])]
u6mean = vels[:,:,:,0]
v6mean = vels[:,:,:,1]

h5file = h5py.File('/Volumes/T7/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[5])]
u9mean = vels[:,:,:,0]
v9mean = vels[:,:,:,1]

h5file = h5py.File('/Volumes/T7/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[6])]
u12mean = vels[:,:,:,0]
v12mean = vels[:,:,:,1]

time = oj.frames_to_seconds(u0mean, v0mean, 90)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u0mean.shape[1], u0mean.shape[2])

# /Volumes/T7/H5/meandataVLS.h5
# F:/H5/meandataVLS.h5

iw20 = oj.IWFilter(u12mean, 20, 90, 12)
iw40 = oj.IWFilter(u12mean, 40, 90, 12)
iw60 = oj.IWFilter(u12mean, 60, 90, 12)
iw80 = oj.IWFilter(u12mean, 80, 90, 12)

iw = oj.IWFilter(u12mean, 60, 90, 12)
f1, ax1 = plt.subplots()
plt.title("reconstructed velocity plot filtered for inertial wave frequency")
ax1.contourf(z_nd, r_nd, iw[600,:,:], cmap = 'bwr')
ax1.set_xlabel("z/D")
ax1.set_ylabel("r/D")
# plt.show()


f2, ax = plt.subplots(nrows=2, ncols=2)
ax[0,0].contourf(z_nd, r_nd, iw20[600,:,:], cmap = 'bwr')
ax[0,1].contourf(z_nd, r_nd, iw40[600,:,:], cmap = 'bwr')
ax[1,0].contourf(z_nd, r_nd, iw60[600,:,:], cmap = 'bwr')
ax[1,1].contourf(z_nd, r_nd, iw80[600,:,:], cmap = 'bwr')
plt.show()