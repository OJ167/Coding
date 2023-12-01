import numpy as np
import os
import sys
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
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




h5file = h5py.File('E:/H5/3D0meandataHLS.h5', 'r')

vels = h5file['3D0']['U100']['L100']['RPM3']
u = vels[:,:,:,0]
v = vels[:,:,:,1]

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)

x = 55
y = 35
x = np.linspace(0 , umean.shape[1], umean.shape[1])
y = np.linspace(0 , umean.shape[0], umean.shape[0])
X, Y = np.meshgrid(x, y) 

r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[1400,:,:], v[1400,:,:])
r_arr, theta_arr, U_rBins, U_azBins = oj.binCylindrical(r, theta, U_r, U_az, thetaBins=5, rBins=5)

f1, (ax1, ax2) = plt.subplots(ncols=2)
ax1.plot(U_az[ :, 55])
# ax2.plot(U_r[ 35, :])
ax2.plot(u[800, :, 55])
plt.show()