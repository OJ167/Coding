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

h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')
# h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')

Vels = ['U50', 'U100']
Len = ['L50', 'L100']
RPMs = ['RPM0' , 'RPM1', 'RPM2', 'RPM3' ,'RPM6', 'RPM9', 'RPM12']

vels = h5file['Narrow'][Vels[0]][Len[0]][RPMs[0]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
u, v = oj.scaleVelNozzle(u, v, 90)

VortLocMax, VortLocMin = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
Time = oj.frames_to_seconds(u, v, 90)


f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.scatter(VortLocMax[91:2000,1], VortLocMax[91:2000,0], label = 'Max')
# plt.show()


# arr = [[0,1,2,3,4,5,6,7,8,9,10], [11,12,13,14,15,16,17,18,19,20]]

arf = np.flip(u[200,:,:], axis = 0)
# print(arf)

f2, (ax2, ax3) = plt.subplots(nrows=1, ncols=2)
ax2.contourf(arf)
ax3.contourf(u[200,:,:])

minflipa = np.flip(VortLocMin[:,0], axis = 0)
minflipr = np.flip(VortLocMin[:,1], axis = 0)

f3, ax4 = plt.subplots(nrows=1, ncols=1)
ax4.scatter(VortLocMax[71:2000,1], VortLocMax[71:2000,0], label = 'Max')
ax4.scatter(VortLocMin[71:2000,1], VortLocMin[71:2000,0], label = 'Min')
ax4.scatter(minflipa[71:2000], VortLocMin[71:2000,0], label = 'flip')
plt.legend()
plt.show()

print(minflipa[71:2000])