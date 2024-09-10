import numpy as np
import os
import sys
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import pandas as pd
import matplotlib.colors as colors
import matplotlib.cm
import h5py
from matplotlib import animation
from scipy.fft import fft, fftfreq, rfft, rfftfreq
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


h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')
# h5file = h5py.File('E:/H5/3D0HLSFine.h5', 'r')

vels = h5file['Narrow']['U100']['L100']['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]

frame = 350
u, v = gaussian_filter(u, sigma=0.7), gaussian_filter(v, sigma=0.7)

oj.descend_obj(h5file)
h5file.close()

vort, vort_gauss = oj.calculate_vorticity(u, v)
enst = np.square(vort_gauss)

vert_sum = np.sum(enst, 1)

f1, (ax1, ax2) = plt.subplots(ncols=2, nrows=1)
ax1.contourf(enst[frame, :,:], cmap = 'seismic')
ax2.plot(vert_sum[frame,:], linestyle='dotted')

# plt.show()

# Generate Figure 2
f2, ax3 = plt.subplots()
ax3.plot(np.mean(vert_sum, axis=0), linestyle='dashed')
ax3.set_title('Mean Vorticity Sum')
ax3.set_xlabel('Index')
ax3.set_ylabel('Vorticity Sum')

plt.show()