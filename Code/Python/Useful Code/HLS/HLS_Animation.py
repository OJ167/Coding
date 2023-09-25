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
cmap = plt.get_cmap("jet_r")




h5file = h5py.File('F:/H5/3D0meandataHLS.h5', 'r')

vels = h5file['3D0']['U100']['L100']['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)


time = oj.frames_to_seconds(u, v, 150)
oj.animate_cube_quiver(u, v, interval=6.67, cmap="seismic", save=1, output="0_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "0_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
print("0RPM Done")

# vels = h5file['3D0']['U100']['L100']['RPM2']
# u = vels[:,:,:,0]
# v = vels[:,:,:,1]

# time = oj.frames_to_seconds(u, v, 150)
# oj.animate_cube_quiver(u, v, interval=6.67, cmap="seismic", save=1, output="2_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "2_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
# print("2RPM Done")
