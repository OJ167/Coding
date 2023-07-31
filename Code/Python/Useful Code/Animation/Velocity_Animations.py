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
# Dir  = "F:/Testing/RPM-1.0__Upiston-50__Stroke-50/2023-07-24__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

#### 2 RPM ####
# Dir  = "F:/Testing/RPM-2.0__Upiston-50__Stroke-50/2023-07-25__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

#### 3 RPM ####
# Dir  = "F:/Testing/RPM-3.0__Upiston-50__Stroke-50/2023-05-23__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

#### 6 RPM ####
# Dir  = "F:/Testing/RPM-6.0__Upiston-50__Stroke-50/2023-06-07__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

#### 9 RPM ####
Dir  = "F:/Testing/RPM-9.0__Upiston-50__Stroke-50/2023-05-24__FPS-90/"
umean, vmean = oj.create_Mean(10, Dir) 
umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

#### 12 RPM ####
# Dir = "F:/Testing/RPM-12.0__Upiston-50__Stroke-50/2023-05-19__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(umean.shape[1], umean.shape[2])

time = oj.frames_to_seconds(umean, vmean, 90)

# u,  v = oj.importData73("F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/2/Data/PIV_export.mat")
# u,  v = oj.importData73("/Volumes/T7/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/2/Data/PIV_export.mat")

oj.animate_cube_quiver(umean, vmean, interval=11.11, cmap="seismic", save=1, output="9_50_50_mean.mp4", fps=90, scale = 1, fsize = (19, 12))

f1, ax1 = plt.subplots()
ax1.quiver(z_nd, r_nd, umean[126,:,:], vmean[126,:,:])
plt.title("1RPM Frame 126")


#### 6 RPM ####
# Dir  = "F:/Testing/RPM-2.0__Upiston-50__Stroke-50/2023-07-25__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)

# oj.animate_cube_quiver(umean, vmean, interval=11.11, cmap="seismic", save=1, output="2_50_50_mean.mp4", fps=90, scale = 1, fsize = (19, 12))
