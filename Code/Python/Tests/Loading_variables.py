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


dir = "F:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90"
# uMean, vMean = np.load(str(dir + '/Var/DataMatrix.npz'))
data = np.load('F:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90/Var/DataMatrix.npz')

uMean = data['uMean']
vMean = data['vMean']


f1, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
ax1.contourf(uMean[200,:,:], cmap = "bwr")
ax2.contourf(vMean[200,:,:], cmap = "bwr")
plt.show()
