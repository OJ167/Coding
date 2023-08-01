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


#### 0 RPM ####
# Dir  = "F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

#### 1 RPM ####
# Dir  = "F:/Testing/RPM-1.0__Upiston-100__Stroke-50/2023-07-24__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

#### 2 RPM ####
# Dir  = "F:/Testing/RPM-2.0__Upiston-100__Stroke-50/2023-07-25__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

#### 3 RPM ####
# Dir  = "F:/Testing/RPM-3.0__Upiston-100__Stroke-50/2023-05-15__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

#### 6 RPM ####
# Dir  = "F:/Testing/RPM-6.0__Upiston-100__Stroke-50/2023-05-11__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

#### 9 RPM ####
# Dir  = "F:/Testing/RPM-9.0__Upiston-100__Stroke-50/2023-05-12__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

#### 12 RPM ####
# Dir = "F:/Testing/RPM-12.0__Upiston-100__Stroke-50/2023-05-19__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)
# r_nd, z_nd = oj.NDUnitsForPlotsNozzle(umean.shape[1], umean.shape[2])



# Rotations = ['RPM0', 'RPM1', 'RPM2', 'RPM3', 'RPM6', 'RPM9', 'RPM12']
# Injection = ['U50', 'U100']

# h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
# vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[0])]
# u0mean = vels[:,:,:,0]
# v0mean = vels[:,:,:,1]

# h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
# vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[1])]
# u1mean = vels[:,:,:,0]
# v1mean = vels[:,:,:,1]

# h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
# vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[2])]
# u2mean = vels[:,:,:,0]
# v2mean = vels[:,:,:,1]

# h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
# vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[3])]
# u3mean = vels[:,:,:,0]
# v3mean = vels[:,:,:,1]

# h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
# vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[4])]
# u6mean = vels[:,:,:,0]
# v6mean = vels[:,:,:,1]

# h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
# vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[5])]
# u9mean = vels[:,:,:,0]
# v9mean = vels[:,:,:,1]

# h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
# vels = h5file['Narrow'][str(Injection[1])]['L50'][str(Rotations[6])]
# u12mean = vels[:,:,:,0]
# v12mean = vels[:,:,:,1]



Dir  = "F:/Testing/RPM-2.0__Upiston-100__Stroke-50/2023-07-25__FPS-90/"
umean, vmean = oj.create_Mean(10, Dir) 
umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)
time = oj.frames_to_seconds(umean, vmean, 90)
oj.animate_cube_quiver(umean, vmean, interval=11.11, cmap="seismic", save=1, output="2_100_50_mean.mp4", fps=90, scale = 1, fsize = (19, 12))
print("0RPM Done")


Dir  = "F:/Testing/RPM-9.0__Upiston-100__Stroke-50/2023-05-12__FPS-90/"
umean, vmean = oj.create_Mean(10, Dir) 
umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)
oj.animate_cube_quiver(umean, vmean, interval=11.11, cmap="seismic", save=1, output="9_100_50_mean.mp4", fps=90, scale = 1, fsize = (19, 12))
print("12RPM Done")


# Dir  = "F:/Testing/RPM-6.0__Upiston-100__Stroke-50/2023-05-11__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# u6mean, v6mean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)
# oj.animate_cube_quiver(u6mean, v6mean, interval=11.11, cmap="seismic", save=1, output="6_100_50_mean.mp4", fps=90, scale = 1, fsize = (19, 12))
# print("6RPM Done")

