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



Dir  = "F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/"
umean, vmean = oj.create_Mean(10, Dir) 
umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)
time = oj.frames_to_seconds(umean, vmean, 90)

# u,  v = oj.importData73("F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/2/Data/PIV_export.mat")
# u,  v = oj.importData73("/Volumes/T7/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/2/Data/PIV_export.mat")

oj.animate_cube_quiver(u, v, interval=11.11, cmap="seismic", save=0, output="0_50_50.mp4", fps=90, scale = 1, fsize = (19, 12))

# r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])

# f1, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
# ax1.quiver(z_nd, r_nd, u[80,:,:], v[80,:,:], pivot="middle")
# ax1.set_xlabel('z/D')
# ax1.set_ylabel('r/D')
# plt.title("0RPM frame 80")
# plt.show()
