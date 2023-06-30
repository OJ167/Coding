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
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

######## Importing multiple rings #####
n = 10
u, v = oj.importData73("F:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90/1/Data/PIV_export.mat")
# u, v = oj.importData73("")
u = np.zeros([n, u.shape[0], u.shape[1], u.shape[2]])
v = np.zeros([n, v.shape[0], v.shape[1], v.shape[2]])

for i in range(1, n+1):
    u[(i-1),:,:,:], v[(i-1),:,:,:] = oj.importData73(f"F:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90/{i}/Data/PIV_export.mat")
    oj.progressBar(i, 10)
    print("\n")

uMean = np.mean(u, 0)
vMean = np.mean(v, 0)


dir = "F:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90"
np.savez(str(dir + '/Var/DataMatrix.npz'), uMean=uMean, vMean=vMean)