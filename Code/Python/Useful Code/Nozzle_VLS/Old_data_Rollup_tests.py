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

print(u.shape)

VortLocMax0, VortLocMin0 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
Time = oj.frames_to_seconds(u, v, 90)


f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.plot(Time[71:500], VortLocMin0[71:500,0], label = 'Min axis 0')
ax1.plot(Time[71:500], VortLocMax0[71:500,0], label = 'Max axis 0')
plt.legend()


f2, ax2 = plt.subplots(nrows=1, ncols=1)
ax2.scatter(VortLocMin0[:,1], VortLocMin0[:,0], label = 'Min')
ax2.scatter(VortLocMax0[:,1], VortLocMax0[:,0], label = 'Max')
plt.legend()


f3, ax3 = plt.subplots(nrows=1, ncols=1)
plt.title('0RPM  position of vorticity peaks frame 250')
ax3.quiver(z_nd, r_nd, u[250,:,:], v[250,:,:])#, VortLocMin0[250,1], VortLocMin0[250,0], label = 'Min')
ax3.quiver(z_nd, r_nd, u[250,:,:], v[250,:,:])#, VortLocMax0[250,1], VortLocMax0[250,0], label = 'Max')
ax3.scatter(VortLocMin0[250,1], VortLocMin0[250,0], label = 'Min')
plt.legend()
# plt.show()


vels = h5file['Narrow'][Vels[0]][Len[0]][RPMs[6]]
u = vels[:,:,:,0]
v = vels[:,:,:,1]

VortLocMax12, VortLocMin12 = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:])

f3, ax3 = plt.subplots(nrows=1, ncols=1)
plt.title('12RPM radial position of vorticity peaks')
ax3.plot(Time[71:500], VortLocMin12[71:500,0], label = 'Min axis 0')
ax3.plot(Time[71:500], VortLocMax12[71:500,0], label = 'Max axis 0')
plt.legend()


f4, ax4 = plt.subplots(nrows=1, ncols=1)
plt.title('0RPM vs 12RPM radial position of vorticity peaks')
ax4.plot(Time[71:500], VortLocMin0[71:500,0], label = '0RPM Min')
ax4.plot(Time[71:500], VortLocMin12[71:500,0], label = '12RPM Min')
ax4.plot(Time[71:500], VortLocMax0[71:500,0], label = '0RPM Max')
ax4.plot(Time[71:500], VortLocMax12[71:500,0], label = '12RPM Max')
plt.legend()
# plt.show()

VortLocMax_i = np.zeros([len(RPMs[:]), 2699, 2])
VortLocMin_i = np.zeros([len(RPMs[:]), 2699, 2])

for i in range(len(RPMs[:])):
    vels = h5file['Narrow'][Vels[0]][Len[1]][RPMs[i]]
    print('RPM: ', RPMs[i])
    u = vels[:,:,:,0]
    v = vels[:,:,:,1]

    VortLocMax_i[i,:,:], VortLocMin_i[i,:,:] = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:])


print(VortLocMin_i.shape)

f5, ax5 = plt.subplots(nrows=1, ncols=1)
plt.title('radial position of vorticity minimum against time')
ax5.plot(Time[71:500], VortLocMin_i[0,71:500,0], label = '0RPM Min')
ax5.plot(Time[71:500], VortLocMin_i[1,71:500,0], label = '1RPM Min')
ax5.plot(Time[71:500], VortLocMin_i[2,71:500,0], label = '2RPM Min')
ax5.plot(Time[71:500], VortLocMin_i[3,71:500,0], label = '3RPM Min')
ax5.plot(Time[71:500], VortLocMin_i[4,71:500,0], label = '6RPM Min')
ax5.plot(Time[71:500], VortLocMin_i[5,71:500,0], label = '9RPM Min')
ax5.plot(Time[71:500], VortLocMin_i[6,71:500,0], label = '12RPM Min')
ax5.set_xlabel('Time (s)')
ax5.set_ylabel('r')
plt.legend()


f6, ax6 = plt.subplots(nrows=1, ncols=1)
plt.title('radial position of vorticity maximum against time')
ax6.plot(Time[71:500], VortLocMax_i[0,71:500,0], label = '0RPM Max')
ax6.plot(Time[71:500], VortLocMax_i[1,71:500,0], label = '1RPM Max')
ax6.plot(Time[71:500], VortLocMax_i[2,71:500,0], label = '2RPM Max')
ax6.plot(Time[71:500], VortLocMax_i[3,71:500,0], label = '3RPM Max')
ax6.plot(Time[71:500], VortLocMax_i[4,71:500,0], label = '6RPM Max')
ax6.plot(Time[71:500], VortLocMax_i[5,71:500,0], label = '9RPM Max')
ax6.plot(Time[71:500], VortLocMax_i[6,71:500,0], label = '12RPM Max')
ax6.set_xlabel('Time (s)')
ax6.set_ylabel('r')
plt.legend()






f7, ax7 = plt.subplots(nrows=1, ncols=1)
plt.title('Radial Position of Vorticity Peaks against Time')
ax7.plot(Time[71:315], VortLocMin_i[0,71:315,0], color = 'c', label = '0RPM')
ax7.plot(Time[71:315], VortLocMin_i[1,71:315,0], color = 'y', label = '1RPM')
ax7.plot(Time[71:315], VortLocMin_i[2,71:315,0], color = 'g', label = '2RPM')
ax7.plot(Time[71:315], VortLocMin_i[3,71:315,0], color = 'r', label = '3RPM')
ax7.plot(Time[71:315], VortLocMin_i[4,71:315,0], color = 'm', label = '6RPM')
ax7.plot(Time[71:315], VortLocMin_i[5,71:315,0], color = 'b', label = '9RPM')
ax7.plot(Time[71:315], VortLocMin_i[6,71:315,0], color = 'k', label = '12RPM')
ax7.plot(Time[71:315], VortLocMax_i[0,71:315,0], color = 'c')
ax7.plot(Time[71:315], VortLocMax_i[1,71:315,0], color = 'y')
ax7.plot(Time[71:315], VortLocMax_i[2,71:315,0], color = 'g')
ax7.plot(Time[71:315], VortLocMax_i[3,71:315,0], color = 'r')
ax7.plot(Time[71:315], VortLocMax_i[4,71:315,0], color = 'm')
ax7.plot(Time[71:315], VortLocMax_i[5,71:315,0], color = 'b')
ax7.plot(Time[71:315], VortLocMax_i[6,71:315,0], color = 'k')
ax7.set_xlabel('Time (s)')
ax7.set_ylabel('r')
ax7.set_ylim([0, 149])
plt.legend()
plt.show()


# VortLocMax_j = np.zeros([len(Len[:]), 2699, 2])
# VortLocMin_j = np.zeros([len(Len[:]), 2699, 2])

# for i in range(len(Len[:])):
#     vels = h5file['Narrow'][Vels[0]][Len[i]][RPMs[0]]
#     print('Len: ', Len[i])
#     u = vels[:,:,:,0]
#     v = vels[:,:,:,1]

#     VortLocMax_i[i,:,:], VortLocMin_i[i,:,:] = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:])

# f8, ax8 = plt.subplots(nrows=1, ncols=1)
# plt.title('Radial Position of Vorticity Peaks against Time')
# ax8.plot(Time[71:315], VortLocMin_i[0,71:315,0], color = 'c', label = 'L50 Min')
# ax8.plot(Time[71:315], VortLocMin_i[1,71:315,0], color = 'y', label = 'L100 Min')
# ax8.plot(Time[71:315], VortLocMax_i[0,71:315,0], color = 'c', label = 'L50 Max')
# ax8.plot(Time[71:315], VortLocMax_i[1,71:315,0], color = 'y', label = 'L100 Max')
# ax8.set_xlabel('Time (s)')
# ax8.set_ylabel('r')
# ax8.set_ylim([0, 149])
# plt.legend()
# plt.show()  
