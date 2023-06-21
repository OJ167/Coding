import numpy as np
import os
import sys
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import matplotlib.colors as colors


#####Import Ollie Tools
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)


######## Importing multiple rings #####
n = 10
u, v = oj.importData73("")
u, v = oj.importData73("")
u = np.zeros([n, u.shape[0], u.shape[1], u.shape[2]])
v = np.zeros([n, v.shape[0], v.shape[1], v.shape[2]])

for i in range(1, n+1):
    u[(i-1),:,:,:], v[(i-1),:,:,:] = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/{i}/Data/PIV_export.mat")
    oj.progressBar(i)

