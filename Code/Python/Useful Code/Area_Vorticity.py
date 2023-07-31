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

Rotations = ['RPM0', 'RPM1', 'RPM2', 'RPM3', 'RPM6', 'RPM9', 'RPM12']
Injection = ['U50', 'U100']

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[0])]['L50'][str(Rotations[0])]
u0mean = vels[:,:,:,0]
v0mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[0])]['L50'][str(Rotations[1])]
u1mean = vels[:,:,:,0]
v1mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[0])]['L50'][str(Rotations[2])]
u2mean = vels[:,:,:,0]
v2mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[0])]['L50'][str(Rotations[3])]
u3mean = vels[:,:,:,0]
v3mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[0])]['L50'][str(Rotations[4])]
u6mean = vels[:,:,:,0]
v6mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[0])]['L50'][str(Rotations[5])]
u9mean = vels[:,:,:,0]
v9mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(Injection[0])]['L50'][str(Rotations[6])]
u12mean = vels[:,:,:,0]
v12mean = vels[:,:,:,1]

time = oj.frames_to_seconds(u0mean, v0mean, 90)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u0mean.shape[1], u0mean.shape[2])

sumVorticity0  = oj.sum_Vorticity(u0mean [:,:,18:], v0mean [:,:,18:])
sumVorticity1  = oj.sum_Vorticity(u1mean [:,:,18:], v1mean [:,:,18:])
sumVorticity2  = oj.sum_Vorticity(u2mean [:,:,18:], v2mean [:,:,18:])
sumVorticity3  = oj.sum_Vorticity(u3mean [:,:,18:], v3mean [:,:,18:])
sumVorticity6  = oj.sum_Vorticity(u6mean [:,:,18:], v6mean [:,:,18:])
sumVorticity9  = oj.sum_Vorticity(u9mean [:,:,18:], v9mean [:,:,18:])
sumVorticity12 = oj.sum_Vorticity(u12mean[:,:,18:], v12mean[:,:,18:])

f1, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.contourf(u0mean[1000,:,:], cmap = "seismic")
plt.title("Velocity Contour")



f2, ax2 = plt.subplots(nrows=1, ncols=1)
plt.title("Circulation without stopping vortex 100/50, full")
ax2.plot(time, sumVorticity0 , label = "0 RPM")
ax2.plot(time, sumVorticity1 , label = "1 RPM")
ax2.plot(time, sumVorticity2 , label = "2 RPM")
ax2.plot(time, sumVorticity3 , label = "3 RPM")
ax2.plot(time, sumVorticity6 , label = "6 RPM")
ax2.plot(time, sumVorticity9 , label = "9 RPM")
ax2.plot(time, sumVorticity12, label = "12 RPM")
ax2.set_xlabel("time [s]")
ax2.set_ylabel("sum of vorticity")
plt.legend()
# plt.show()


Vorticity0r, Vorticity0  = oj.calculate_vorticity(u0mean, v0mean)
Vorticity1r, Vorticity1  = oj.calculate_vorticity(u1mean, v1mean)
Vorticity2r, Vorticity2  = oj.calculate_vorticity(u2mean, v2mean)
Vorticity3r, Vorticity3  = oj.calculate_vorticity(u3mean, v3mean)
Vorticity6r, Vorticity6  = oj.calculate_vorticity(u6mean, v6mean)
Vorticity9r, Vorticity9  = oj.calculate_vorticity(u9mean, v9mean)
Vorticity12r, Vorticity12 = oj.calculate_vorticity(u12mean, v12mean)

f3, (ax3, ax4) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
ax3.plot(Vorticity0 [1000, 60, :])
ax4.plot(Vorticity12[1000, 60, :])
# plt.show()

### FInding a baseline where the 0RPM ring can be seen
f3, ax5 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
ax5.plot(Vorticity0 [1000, 68, :], label = "Row 68")
ax5.plot(Vorticity0 [1000, 60, :], label = "Row 60")
ax5.plot(Vorticity0 [1000, 50, :], label = "Row 50")
ax5.plot(Vorticity0 [1000, 40, :], label = "Row 40")
ax5.plot(Vorticity0 [1000, 30, :], label = "Row 30")
plt.legend()
plt.show()


# v0mean  = np.mean(v0mean, axis = 0)
# v1mean  = np.mean(v1mean, axis = 0)
# v2mean  = np.mean(v2mean, axis = 0)
# v3mean  = np.mean(v3mean, axis = 0)
# v6mean  = np.mean(v6mean, axis = 0)
# v9mean  = np.mean(v9mean, axis = 0)
# v12mean = np.mean(v12mean, axis = 0)

# vmin = min(np.min(v0mean), np.min(v1mean), np.min(v3mean), np.min(v6mean), np.min(v9mean), np.min(v12mean))
# vmax = max(np.min(v0mean), np.max(v1mean), np.max(v3mean), np.max(v6mean), np.max(v9mean), np.max(v12mean))
# norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)


# fig, axs = plt.subplots(2, 3, sharex= True, sharey=True)
# axs[0, 0].contourf(z_nd, r_nd, v0mean,  norm=norm, cmap = "seismic")
# axs[0, 0].set_xlabel("z/D")
# axs[0, 0].set_ylabel("r/D")
# axs[0, 1].contourf(z_nd, r_nd, v1mean,  norm=norm, cmap = "seismic")
# axs[0, 1].set_xlabel("z/D")
# axs[0, 1].set_ylabel("r/D")
# # axs[0, 1].contourf(z_nd, r_nd, u2mean,  norm=norm, cmap = "seismic")
# axs[0, 2].contourf(z_nd, r_nd, v3mean,  norm=norm, cmap = "seismic")
# axs[0, 2].set_xlabel("z/D")
# axs[0, 2].set_ylabel("r/D")
# axs[1, 0].contourf(z_nd, r_nd, v6mean,  norm=norm, cmap = "seismic")
# axs[1, 0].set_xlabel("z/D")
# axs[1, 0].set_ylabel("r/D")
# axs[1, 1].contourf(z_nd, r_nd, v9mean,  norm=norm, cmap = "seismic")
# axs[1, 1].set_xlabel("z/D")
# axs[1, 1].set_ylabel("r/D")
# axs[1, 2].contourf(z_nd, r_nd, v12mean, norm=norm, cmap = "seismic")
# axs[1, 2].set_xlabel("z/D")
# axs[1, 2].set_ylabel("r/D")
# axs[0, 0].set_title('0 RPM')
# axs[0, 1].set_title('1 RPM')
# # ax4.set_title('2 RPM')
# axs[0, 2].set_title('3 RPM')
# axs[1, 0].set_title('6 RPM')
# axs[1, 1].set_title('9 RPM')
# axs[1, 2].set_title('12 RPM')
# plt.suptitle("Time averaged radial Velocity 50/50")
# plt.show()








