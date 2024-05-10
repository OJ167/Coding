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

vels = h5file['Narrow'][Vels[0]][Len[0]][RPMs[4]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
u, v = oj.scaleVelNozzle(u, v, 90)

VortLocMax, VortLocMin = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
Time = oj.frames_to_seconds(u, v, 90)


f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.scatter(VortLocMax[91:2000,1], VortLocMax[91:2000,0], label = 'Max')
# plt.show()




##### Changing the 0 index to the centreline of the nozzle

VortLocMin[:,0] = abs(np.subtract(VortLocMin[:,0], int(u.shape[1]/2)))
VortLocMax[:,0] = np.subtract(VortLocMax[:,0], int(u.shape[1]/2))


f4, ax5 = plt.subplots(nrows=1, ncols=1)
ax5.set_title('numpy way')
ax5.scatter(VortLocMax[71:2000, 1], VortLocMax[71:2000, 0], label = 'Max')
ax5.scatter(VortLocMin[71:2000, 1], abs(VortLocMin[71:2000, 0]), label = 'Min')
plt.legend()
# plt.show()

##### Averaging the 2 cores

VortLocAvg = np.zeros([VortLocMax.shape[0], 2])
VortLocAvg = np.mean([VortLocMax, VortLocMin], axis = 0)


f5, ax6 = plt.subplots(nrows=1, ncols=1)
ax6.set_title('Averaged Cores vs Absolute Max and Absolute Min')
ax6.scatter(VortLocMax[71:2000, 1], VortLocMax[71:2000, 0], label = 'Max')
ax6.scatter(VortLocMin[71:2000, 1], VortLocMin[71:2000, 0], label = 'Min')
ax6.scatter(VortLocAvg[71:2000, 1], VortLocAvg[71:2000, 0], label = 'Avg')
ax6.set_ylim([0, 50])
ax6.set_xlim([25, 115])
ax6.set_xlabel(r'$z$')
ax6.set_ylabel(r'$r$')
plt.legend()
plt.show()




####### Comparing different injection conditions #################
index = 6

#5050
vels = h5file['Narrow']['U50']['L50'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax5050, VortLocMin5050 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
VortLocMin5050[:,0] = abs(np.subtract(VortLocMin5050[:,0], int(u.shape[1]/2)))
VortLocMax5050[:,0] = np.subtract(VortLocMax5050[:,0], int(u.shape[1]/2))
VortLocAvg5050 = np.zeros([VortLocMax5050.shape[0], 2])
VortLocAvg5050 = np.mean([VortLocMax5050, VortLocMin5050], axis = 0)
Circ_5050    = oj.sum_Vorticity(u, v)

#10050
vels = h5file['Narrow']['U100']['L50'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax10050, VortLocMin10050 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
VortLocMin10050[:,0] = abs(np.subtract(VortLocMin10050[:,0], int(u.shape[1]/2)))
VortLocMax10050[:,0] = np.subtract(VortLocMax10050[:,0], int(u.shape[1]/2))
VortLocAvg10050 = np.zeros([VortLocMax10050.shape[0], 2])
VortLocAvg10050 = np.mean([VortLocMax10050, VortLocMin10050], axis = 0)
Circ_10050   = oj.sum_Vorticity(u, v)

#50100
vels = h5file['Narrow']['U50']['L100'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax50100, VortLocMin50100 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
VortLocMin50100[:,0] = abs(np.subtract(VortLocMin50100[:,0], int(u.shape[1]/2)))
VortLocMax50100[:,0] = np.subtract(VortLocMax50100[:,0], int(u.shape[1]/2))
VortLocAvg50100 = np.zeros([VortLocMax50100.shape[0], 2])
VortLocAvg50100 = np.mean([VortLocMax50100, VortLocMin50100], axis = 0)
Circ_50100   = oj.sum_Vorticity(u, v)

#100100
vels = h5file['Narrow']['U100']['L100'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax100100, VortLocMin100100 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
VortLocMin100100[:,0] = abs(np.subtract(VortLocMin100100[:,0], int(u.shape[1]/2)))
VortLocMax100100[:,0] = np.subtract(VortLocMax100100[:,0], int(u.shape[1]/2))
VortLocAvg100100 = np.zeros([VortLocMax100100.shape[0], 2])
VortLocAvg100100 = np.mean([VortLocMax100100, VortLocMin100100], axis = 0)
Circ_100100  = oj.sum_Vorticity(u, v)

start_frame = 71
end_frame = 521 #for 5 seconds
# end_frame = 2499



# f4, ax4 = plt.subplots(nrows=1, ncols=1)
# plt.title('12 RPM Absolute Average Position of Vorticity Peaks in first 5 seconds')
# ax4.scatter(VortLocAvg5050  [start_frame:end_frame,1],     VortLocMax5050  [start_frame:end_frame,0], color='c', label = '50 50')
# ax4.scatter(VortLocAvg10050 [start_frame:end_frame,1],     VortLocMax10050 [start_frame:end_frame,0], color='b', label = '100 50')
# ax4.scatter(VortLocAvg50100 [start_frame:end_frame,1],     VortLocMax50100 [start_frame:end_frame,0], color='r', label = '50 100')
# ax4.scatter(VortLocAvg100100[start_frame:end_frame,1],     VortLocMax100100[start_frame:end_frame,0], color='g', label = '100 100')
# # ax4.set_ylim([71, u.shape[1]])
# # ax4.set_xlim([25, u.shape[2]])
# # ax4.tick_params(axis='r_nd')
# ax4.set_ylim([0, 50])
# ax4.set_xlim([25, 115])
# ax4.set_xlabel(r'$z$')
# ax4.set_ylabel(r'$r$')
# plt.legend()



f5, ax5 = plt.subplots(nrows=1, ncols=1)
plt.title('12 RPM Absolute Average Position of Vorticity Peaks in first 5 seconds')
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocMax5050  [start_frame:end_frame,0], color='c', label = '50 50')
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocMax10050 [start_frame:end_frame,0], color='b', label = '100 50')
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocMax50100 [start_frame:end_frame,0], color='r', label = '50 100')
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocMax100100[start_frame:end_frame,0], color='g', label = '100 100')
ax5.set_ylim([0, 50])
ax5.set_xlabel(r'$t$[s]')
ax5.set_ylabel(r'$r$')
plt.legend()
# plt.show()


# f6, ax6 = plt.subplots(nrows=1, ncols=1)
# plt.title('0 RPM Absolute Average Position of Vorticity Peaks in first 5 seconds')
# ax6.scatter(Time[:(end_frame-start_frame)],     VortLocMax5050  [start_frame:end_frame,1], color='c', label = '50 50')
# ax6.scatter(Time[:(end_frame-start_frame)],     VortLocMax10050 [start_frame:end_frame,1], color='b', label = '100 50')
# ax6.scatter(Time[:(end_frame-start_frame)],     VortLocMax50100 [start_frame:end_frame,1], color='r', label = '50 100')
# ax6.scatter(Time[:(end_frame-start_frame)],     VortLocMax100100[start_frame:end_frame,1], color='g', label = '100 100')
# ax6.set_ylim([25, 200])
# ax6.set_xlabel(r'$t$[s]')
# ax6.set_ylabel(r'$z$')
# plt.legend()




f7, ax7 = plt.subplots(nrows=1, ncols=1)
ax7.set_title('measurement of circulation')
ax7.scatter(Time[:(end_frame-start_frame)], Circ_5050[start_frame:end_frame], color='c', label = '50 50')
ax7.scatter(Time[:(end_frame-start_frame)], Circ_10050[start_frame:end_frame], color='b', label = '100 50')
ax7.scatter(Time[:(end_frame-start_frame)], Circ_50100[start_frame:end_frame], color='r', label = '50 100')
ax7.scatter(Time[:(end_frame-start_frame)], Circ_100100[start_frame:end_frame], color='g', label = '100 100')
plt.legend()


f8, ax8 = plt.subplots(nrows=1, ncols=1)
ax8.set_title('Radial Position of Vorticity Peaks Normalised by Circulation against Time')
ax8.scatter(Time[:(end_frame-start_frame)],     (VortLocMax5050  [start_frame:end_frame,0]/Circ_5050[start_frame:end_frame]), color='c', label = '50 50')
ax8.scatter(Time[:(end_frame-start_frame)],     (VortLocMax10050 [start_frame:end_frame,0]/Circ_10050[start_frame:end_frame]), color='b', label = '100 50')
ax8.scatter(Time[:(end_frame-start_frame)],     (VortLocMax50100 [start_frame:end_frame,0]/Circ_50100[start_frame:end_frame]), color='r', label = '50 100')
ax8.scatter(Time[:(end_frame-start_frame)],     (VortLocMax100100[start_frame:end_frame,0]/Circ_100100[start_frame:end_frame]), color='g', label = '100 100')
ax8.set_ylim([0, 0.2])
ax8.set_xlabel(r'$t$[s]')
ax8.set_ylabel(r'$r/ \Gamma$')
plt.legend()
plt.show()