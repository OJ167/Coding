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

Vels = ['U50', 'U100']
Len = ['L50', 'L100']
RPMs = ['RPM0' , 'RPM1', 'RPM2', 'RPM3' ,'RPM6', 'RPM9', 'RPM12']

vels = h5file['Narrow'][Vels[0]][Len[0]][RPMs[0]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]

VortLocMax, VortLocMin = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
Time = oj.frames_to_seconds(u, v, 90)



f1, ax1 = plt.subplots(nrows=1, ncols=1)
# ax1.scatter(z_nd, r_nd)#, VortLocMax[250,1], VortLocMax[250,0], label = 'Max')
ax1.scatter(VortLocMax[91:2000,1], VortLocMax[91:2000,0], label = 'Max')
ax1.scatter(VortLocMin[91:2000,1], VortLocMin[91:2000,0], label = 'Min')
plt.legend()




f3, ax3 = plt.subplots(nrows=1, ncols=1)
ax3.scatter(VortLocMax[71:2000,1], VortLocMax[71:2000,0], label = 'Max')
ax3.scatter(VortLocMin[71:2000,1], abs(VortLocMin[71:2000,0]-74)+74, label = 'Min')
ax3.set_ylim([71, u.shape[2]])
ax3.set_xlim([25, u.shape[1]])
plt.legend()
# plt.show()



#5050
vels = h5file['Narrow']['U50']['L50'][RPMs[1]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax5050, VortLocMin5050 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial

#10050
vels = h5file['Narrow']['U100']['L50'][RPMs[1]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax10050, VortLocMin10050 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial

#50100
vels = h5file['Narrow']['U50']['L100'][RPMs[1]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax50100, VortLocMin50100 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial


#100100
vels = h5file['Narrow']['U100']['L100'][RPMs[1]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax100100, VortLocMin100100 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial


start_frame = 71
end_frame = 450

f4,ax4 = plt.subplots(nrows=1, ncols=1)
plt.title('1RPM Absolute Position of Vorticity Peaks in first 5 seconds')
ax4.scatter(VortLocMax5050  [start_frame:end_frame,1],     VortLocMax5050  [start_frame:end_frame,0], color='c', label = '50 50')
ax4.scatter(VortLocMin5050  [start_frame:end_frame,1], abs(VortLocMin5050  [start_frame:end_frame,0]-74)+74, color='c')
ax4.scatter(VortLocMax10050 [start_frame:end_frame,1],     VortLocMax10050 [start_frame:end_frame,0], color='b', label = '100 50')
ax4.scatter(VortLocMin10050 [start_frame:end_frame,1], abs(VortLocMin10050 [start_frame:end_frame,0]-74)+74, color='b')
ax4.scatter(VortLocMax50100 [start_frame:end_frame,1],     VortLocMax50100 [start_frame:end_frame,0], color='r', label = '50 100')
ax4.scatter(VortLocMin50100 [start_frame:end_frame,1], abs(VortLocMin50100 [start_frame:end_frame,0]-74)+74, color = 'r')
ax4.scatter(VortLocMax100100[start_frame:end_frame,1],     VortLocMax100100[start_frame:end_frame,0], color='g', label = '100 100')
ax4.scatter(VortLocMin100100[start_frame:end_frame,1], abs(VortLocMin100100[start_frame:end_frame,0]-74)+74, color='g')
ax4.set_ylim([71, u.shape[1]])
ax4.set_xlim([25, u.shape[2]])
ax4.set_xlabel(r'$z$')
ax4.set_ylabel(r'$r$')
plt.legend()
plt.show()