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

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])



# u, v = oj.importData73("G:/Testing/Condition_tests/L250_U500/Data/PIV_export.mat")
# u, v = oj.importData73("G:/Testing/Condition_tests/L250_U1000/Data/PIV_export.mat")
# u, v = oj.importData73("G:/Testing/Condition_tests/L500_U500/Data/PIV_export.mat")
# u, v = oj.importData73("G:/Testing/Condition_tests/L500_U2000/Data/PIV_export.mat")
# u, v = oj.importData73("G:/Testing/Condition_tests/L1000_U500/Data/PIV_export.mat")
# u, v = oj.importData73("G:/Testing/Condition_tests/L1000_U1000/Data/PIV_export.mat")

# u, v = oj.importData73("F:/Testing/RPM-9.0__Upiston-50__Stroke-100/2023-08-19__FPS-90/2/Data/PIV_export.mat")
u, v = oj.importData73("F:/Testing/RPM-9.0__Upiston-100__Stroke-100/2023-08-19__FPS-90/6/Data/PIV_export.mat")
u, v = gaussian_filter(u, sigma=0.7), gaussian_filter(v, sigma=0.7)

time = oj.frames_to_seconds(u, v, 90)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])

 

oj.animate_cube_quiver(u, v)

f1, ax1 = plt.subplots()
ax1.contourf(z_nd, r_nd, u[300,:,:], cmap = "seismic")
plt.show()

