import matplotlib.pyplot as plt
import numpy as np
import h5py
from scipy.signal import savgol_filter
import os
import sys
from scipy.ndimage import gaussian_filter


#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
plt.style.use(["science", "vibrant", "no-latex"])

from tkinter.filedialog import askdirectory


################ To load in. move this to another file 

h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')
# h5file = h5py.File('E:/H5/3D0HLSFine.h5', 'r')

vels = h5file['Narrow']['U100']['L50']['RPM0']
# vels = h5file['3D0']['U100']['L100']['RPM12']
u = vels[:,:,:,0]
v = vels[:,:,:,1]

oj.descend_obj(h5file)
h5file.close()

frame = 150

#background image is a reference from 0RPM 100, 100 background image
# 'G:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/1/B/bgImage/image1_bg.tiff'
# copied to local drive
# 'C:/Users/u2088308/Pictures/image1_bg.tiff'

r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])

im = plt.imread('C:/Users/u2088308/Pictures/image1_bg.tiff')
f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.imshow(im,extent=[ z_nd[0], z_nd[-1], r_nd[0], r_nd[-1]], cmap = 'Greys_r')
ax1.streamplot(z_nd, r_nd, u[frame,:,:], v[frame,:,:], color = 'g', broken_streamlines = False)



f2, ax2 = plt.subplots(nrows=1, ncols=1)
ax2.imshow(im,extent=[ z_nd[0], z_nd[-1], r_nd[0], r_nd[-1]], cmap = 'Greys_r')
ax2.quiver(z_nd, r_nd, u[frame,:,:], v[frame,:,:], color = 'w')


f3, (ax3, ax4) = plt.subplots(nrows=2,ncols=1)
# ax3.imshow(im,extent=[ z_nd[0], z_nd[-1], r_nd[0], r_nd[-1]], cmap = 'Greys_r')
ax3.quiver(u[frame,:,:], v[frame,:,:], color = 'k')
# ax3.axvline(x=43, color = 'r')
ax3.set_xlim([0, u.shape[2]])
ax3.set_ylim([0, u.shape[1]])

ax3.axvline(x = 31, color = 'b', label = 'line 31')
ax3.axvline(x = 37, color = 'r', label = 'line 37')
ax3.axvline(x = 43, color = 'g', label = 'line 43')
ax3.axvline(x = 49, color = 'c', label = 'line 49')
ax3.axvline(x = 51, color = 'm', label = 'line 51')
plt.legend()
ax4.imshow(im,extent=[ z_nd[0], z_nd[-1], r_nd[0], r_nd[-1]], cmap = 'Greys_r',aspect='auto')

f4, ax5 = plt.subplots(nrows=1, ncols=1)
ax5.plot(u[frame,:,31], color = 'b', label = 'line 31')
ax5.plot(u[frame,:,37], color = 'r', label = 'line 37')
ax5.plot(u[frame,:,43], color = 'g', label = 'line 43')
ax5.plot(u[frame,:,49], color = 'c', label = 'line 49')
ax5.plot(u[frame,:,51], color = 'm', label = 'line 51')
plt.legend()
plt.show()