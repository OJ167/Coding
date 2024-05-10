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



########## Finding radial Velocities at the core location

# vort_max_loc_x = np.zeros([u.shape[0]])
# vort_max_loc_y = np.zeros([u.shape[0]])

# for i in range(u.shape[0]):
#     vort_max_loc_x[i] = VortLocMax[i,1]
#     vort_max_loc_y[i] = VortLocMax[i,0]

# print(vort_max_loc_x, vort_max_loc_y)
# print(vort_max_loc_x.shape, vort_max_loc_y.shape)

# f3, ax3 = plt.subplots(nrows=1, ncols=1)
# ax3.plot(v[:, int(vort_max_loc_y[i]), int(vort_max_loc_x[i])])
# # plt.show()



########### Find Ring Expansion Rate ###########

VortLocMax[:,0] = savgol_filter(VortLocMax[:,0], 21, 3)
VortLocMax[:,1] = savgol_filter(VortLocMax[:,1], 21, 3)
drdt = np.gradient(VortLocMax[:,0])

f4, ax4 = plt.subplots(nrows=1, ncols=1)
plt.title('Ring Expansion Rate')
ax4.plot(drdt[71:500])
# ax4.plot(VortLocMax[71:500,0])
# ax4.set_ylim([71, u.shape[2]])
# ax4.set_xlim([25, u.shape[1]])
plt.legend()
# plt.show()






#### convolved smoothing for the ring expansion rate ####

filt = np.ones(15)/15
y_smooth = np.convolve(VortLocMax[:,0], filt, mode='valid')
dysdx = np.gradient(y_smooth)

f5, ax5 = plt.subplots(nrows=1, ncols=1)
plt.title('Ring Expansion Rate')
ax5.plot(drdt[71:500] , label='$r\'(t)$' )
ax5.plot(dysdx[71:500], label='$r_{smooth}\'(t)$')
plt.legend()
plt.show()

























####### Comparing different injection conditions #################
index = 0

#5050
vels = h5file['Narrow']['U50']['L50'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax5050, VortLocMin5050 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial

#10050
vels = h5file['Narrow']['U100']['L50'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax10050, VortLocMin10050 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial

#50100
vels = h5file['Narrow']['U50']['L100'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax50100, VortLocMin50100 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial


#100100
vels = h5file['Narrow']['U100']['L100'][RPMs[index]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
VortLocMax100100, VortLocMin100100 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial



start_frame = 71
end_frame = 450

f4,ax4 = plt.subplots(nrows=1, ncols=1)
plt.title('12 RPM Absolute Position of Vorticity Peaks in first 5 seconds')
ax4.scatter(VortLocMax5050  [start_frame:end_frame,1],     VortLocMax5050  [start_frame:end_frame,0], color='c', label = '50 50')
ax4.scatter(VortLocMin5050  [start_frame:end_frame,1], abs(VortLocMin5050  [start_frame:end_frame,0]-74)+74, color='c')
ax4.scatter(VortLocMax10050 [start_frame:end_frame,1],     VortLocMax10050 [start_frame:end_frame,0], color='b', label = '100 50')
ax4.scatter(VortLocMin10050 [start_frame:end_frame,1], abs(VortLocMin10050 [start_frame:end_frame,0]-74)+74, color='b')
ax4.scatter(VortLocMax50100 [start_frame:end_frame,1],     VortLocMax50100 [start_frame:end_frame,0], color='r', label = '50 100')
ax4.scatter(VortLocMin50100 [start_frame:end_frame,1], abs(VortLocMin50100 [start_frame:end_frame,0]-74)+74, color = 'r')
ax4.scatter(VortLocMax100100[start_frame:end_frame,1],     VortLocMax100100[start_frame:end_frame,0], color='g', label = '100 100')
ax4.scatter(VortLocMin100100[start_frame:end_frame,1], abs(VortLocMin100100[start_frame:end_frame,0]-74)+74, color='g')
# ax4.set_ylim([71, u.shape[1]])
# ax4.set_xlim([25, u.shape[2]])
# ax4.tick_params(axis='r_nd')
ax4.set_ylim([95, 115])
ax4.set_xlim([25, 115])
ax4.set_xlabel(r'$z$')
ax4.set_ylabel(r'$r$')
plt.legend()


frame = 500
V = np.sqrt(u[frame,:,:]**2 + v[frame,:,:]**2)

us, vs = oj.scaleVelNozzle(u, v, 90)
Vs = np.sqrt(us[frame,:,:]**2 + vs[frame,:,:]**2)

f5, ax = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
plt.title('scaled velocity field')
ax[0,0].imshow(u [frame,:,:], cmap = 'bwr')
ax[0,1].imshow(v [frame,:,:], cmap = 'bwr')
ax[1,0].imshow(us[frame,:,:], cmap = 'bwr')
ax[1,1].imshow(vs[frame,:,:], cmap = 'bwr')
plt.show()