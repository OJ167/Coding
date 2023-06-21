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

# from colorspacious import cspace_converter

#####Import Ollie Tools
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

u, v = oj.importData(f"G:/Testing/BackgroundMovement_3.0RPM/PIVlab.mat")

f1, ax1 = plt.subplots(nrows=1, ncols=1)
plt.title("velocity plot")
ax1.contourf(u[1000, :, :])
# plt.show()

fft_mid = np.fft.rfft(u[:,37,60])
fft_edge = np.fft.rfft(u[:,37,100])
f2, ax2 = plt.subplots(nrows=1, ncols=1)
plt.title("fft")
ax2.plot(fft_mid)
ax2.plot(fft_edge)
# plt.show()

vfft_u = oj.IWFilter(u, 40, 60, 3)
vfft_v = oj.IWFilter(v, 40, 60, 3)
f1, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1)
ax1.contourf(vfft_u[450,:,:], cmap="seismic")
ax2.contourf(vfft_v[450,:,:], cmap="seismic")
plt.show()

oj.animate_cube_contourf(u, 16.7)