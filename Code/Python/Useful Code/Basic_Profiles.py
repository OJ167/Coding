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
# u, v = oj.importData73("G:/Testing/RPM-9.0__Upiston-100__Stroke-100/2023-08-19__FPS-90/6/Data/PIV_export.mat")

u5050, v5050 = oj.importData73("F:/Testing/3Do/RPM-0.0__Upiston-50__Stroke-50/2023-09-15__FPS-150/1/Data/PIV_export.mat")
u50100, v50100 = oj.importData73("F:/Testing/3Do/RPM-0.0__Upiston-50__Stroke-100/2023-09-15__FPS-150/1/Data/PIV_export.mat")
u10050, v10050 = oj.importData73("F:/Testing/3Do/RPM-0.0__Upiston-100__Stroke-50/2023-09-15__FPS-150/1/Data/PIV_export.mat")
u100100, v100100 = oj.importData73("F:/Testing/3Do/RPM-0.0__Upiston-100__Stroke-100/2023-09-14__FPS-150/1/Data/PIV_export.mat")

# u, v = gaussian_filter(u, sigma=1.7), gaussian_filter(v, sigma=1.7)

# time = oj.frames_to_seconds(u, v, 150)
# r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])

 

oj.animate_cube_quiver(u5050[1200:,:,:], v5050[1200:,:,:])
oj.animate_cube_quiver(u50100[1200:,:,:], v50100[1200:,:,:])
oj.animate_cube_quiver(u10050 [1200:,:,:], v10050 [1200:,:,:])
oj.animate_cube_quiver(u100100[1200:,:,:], v100100[1200:,:,:])

f1, axs = plt.subplots(2, 2, sharex= True, sharey=True)
axs[0, 0].quiver(u5050  [1900,:,:], v5050  [1900,:,:])
axs[0, 1].quiver(u50100 [900,:,:], v50100 [900,:,:])
axs[1, 0].quiver(u10050 [900,:,:], v10050 [900,:,:])
axs[1, 1].quiver(u100100[900,:,:], v100100[900,:,:])
plt.show()

