import matplotlib.pyplot as plt
import numpy as np
import h5py
from scipy.signal import savgol_filter
import os
import sys
from scipy.ndimage import gaussian_filter
import matplotlib


#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
plt.style.use(["science", "vibrant", "no-latex"])
# plt.style.use(["notebook", "vibrant", "no-latex"])
matplotlib.rc('xtick', labelsize=8) 
matplotlib.rc('ytick', labelsize=8) 

h5file = h5py.File('E:/H5/LengthTestNEW.h5', 'r')

Vels = ['U100']
# Len = ['L25', 'L50', 'L75', 'L100', 'L125', 'L150', 'L175', 'L200', 'L225', 'L240']
Len = ['L25', 'L50', 'L75', 'L100', 'L125', 'L150', 'L175', 'L200', 'L225', 'L240']
RPMs = ['RPM0']

vels = h5file['Narrow']['U100'][Len[0]]['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
u, v = oj.scaleVelNozzle(u, v, 90)

VortLocMax, VortLocMin = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
Time = oj.frames_to_seconds(u, v, 90)

start_frame = 71
end_frame = 521 #for 5 seconds

VortLocAvg = np.zeros([10, 2699, 2])
VortLocAvg = np.zeros([len(Len), VortLocMax.shape[0], 2])
Circulation = np.zeros([len(Len), VortLocMax.shape[0]])

for i in range(len(Len)):
    print(Len[i])
    vels = h5file['Narrow']['U100'][Len[i]]['RPM0']
    u = vels[:,:,:,0]
    v = vels[:,:,:,1]
    u, v = oj.scaleVelNozzle(u, v, 90)
    VortLocMax, VortLocMin = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
    VortLocMin[:,0] = abs(np.subtract(VortLocMin[:,0], int(u.shape[1]/2)))
    VortLocMax[:,0] = np.subtract(VortLocMax[:,0], int(u.shape[1]/2))
    # VortLocAvg[i,:,:] = np.zeros([VortLocMax.shape[0], 2])
    VortLocAvg[i,:,:] = np.mean([VortLocMax, VortLocMin], axis = 0)
    # VortLocAvg[i,:,:] = VortLocMax[:,:]
    Circulation[i,:]  = oj.sum_Vorticity(u, v)



f1, ax1 = plt.subplots(nrows=1, ncols=1)
plt.title('Core Radial Position against time')
ax1.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[0,start_frame:end_frame,0], label = f'Len = {Len[0]}', ) # L = 25
ax1.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[1,start_frame:end_frame,0], label = f'Len = {Len[1]}', ) # L = 50
ax1.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[2,start_frame:end_frame,0], label = f'Len = {Len[2]}', ) # L = 75
ax1.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[3,start_frame:end_frame,0], label = f'Len = {Len[3]}', ) # L = 100
ax1.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[4,start_frame:end_frame,0], label = f'Len = {Len[4]}', ) # L = 125
ax1.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[5,start_frame:end_frame,0], label = f'Len = {Len[5]}', ) # L = 150
ax1.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[6,start_frame:end_frame,0], label = f'Len = {Len[6]}', ) # L = 175
ax1.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[7,start_frame:end_frame,0], label = f'Len = {Len[7]}', ) # L = 200
ax1.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[8,start_frame:end_frame,0], label = f'Len = {Len[8]}', ) # L = 225
ax1.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[9,start_frame:end_frame,0], label = f'Len = {Len[9]}', ) # L = 240
ax1.set_ylim([0, 50])
ax1.set_xlabel(r'$t$[s]')
ax1.set_ylabel(r'$r$')
plt.legend()



f2, ax2 = plt.subplots(nrows=1, ncols=1)
plt.title('Averaged Core Location in the first 5 seconds')
ax2.scatter(VortLocAvg[0,start_frame:end_frame,1],     VortLocAvg[0,start_frame:end_frame,0], label = f'Len = {Len[0]}') # L = 25
ax2.scatter(VortLocAvg[1,start_frame:end_frame,1],     VortLocAvg[1,start_frame:end_frame,0], label = f'Len = {Len[1]}') # L = 50
ax2.scatter(VortLocAvg[2,start_frame:end_frame,1],     VortLocAvg[2,start_frame:end_frame,0], label = f'Len = {Len[2]}') # L = 75
ax2.scatter(VortLocAvg[3,start_frame:end_frame,1],     VortLocAvg[3,start_frame:end_frame,0], label = f'Len = {Len[3]}') # L = 100
ax2.scatter(VortLocAvg[4,start_frame:end_frame,1],     VortLocAvg[4,start_frame:end_frame,0], label = f'Len = {Len[4]}') # L = 125
ax2.scatter(VortLocAvg[5,start_frame:end_frame,1],     VortLocAvg[5,start_frame:end_frame,0], label = f'Len = {Len[5]}') # L = 150
ax2.scatter(VortLocAvg[6,start_frame:end_frame,1],     VortLocAvg[6,start_frame:end_frame,0], label = f'Len = {Len[6]}') # L = 175
ax2.scatter(VortLocAvg[7,start_frame:end_frame,1],     VortLocAvg[7,start_frame:end_frame,0], label = f'Len = {Len[7]}') # L = 200
ax2.scatter(VortLocAvg[8,start_frame:end_frame,1],     VortLocAvg[8,start_frame:end_frame,0], label = f'Len = {Len[8]}') # L = 225
ax2.scatter(VortLocAvg[9,start_frame:end_frame,1],     VortLocAvg[9,start_frame:end_frame,0], label = f'Len = {Len[9]}') # L = 240
ax2.set_ylim([0, 50])
ax2.set_xlabel(r'$z$')
ax2.set_ylabel(r'$r$')
plt.legend()







f3, ax3 = plt.subplots(nrows=1, ncols=1, figsize=(5.5, 4))
plt.title('Circulation against time')
ax3.scatter(Time[:(end_frame-start_frame)],     Circulation[0,start_frame:end_frame], label = f'Len = {Len[0]}', ) # L = 25
ax3.scatter(Time[:(end_frame-start_frame)],     Circulation[1,start_frame:end_frame], label = f'Len = {Len[1]}', ) # L = 50
ax3.scatter(Time[:(end_frame-start_frame)],     Circulation[2,start_frame:end_frame], label = f'Len = {Len[2]}', ) # L = 75
ax3.scatter(Time[:(end_frame-start_frame)],     Circulation[3,start_frame:end_frame], label = f'Len = {Len[3]}', ) # L = 100
ax3.scatter(Time[:(end_frame-start_frame)],     Circulation[4,start_frame:end_frame], label = f'Len = {Len[4]}', ) # L = 125
ax3.scatter(Time[:(end_frame-start_frame)],     Circulation[5,start_frame:end_frame], label = f'Len = {Len[5]}', ) # L = 150
ax3.scatter(Time[:(end_frame-start_frame)],     Circulation[6,start_frame:end_frame], label = f'Len = {Len[6]}', ) # L = 175
ax3.scatter(Time[:(end_frame-start_frame)],     Circulation[7,start_frame:end_frame], label = f'Len = {Len[7]}', ) # L = 200
ax3.scatter(Time[:(end_frame-start_frame)],     Circulation[8,start_frame:end_frame], label = f'Len = {Len[8]}', ) # L = 225
ax3.scatter(Time[:(end_frame-start_frame)],     Circulation[9,start_frame:end_frame], label = f'Len = {Len[9]}', ) # L = 240
ax3.set_xlabel(r'$t$[s]')
ax3.set_ylabel(r'$\Gamma$ [cm$^2$s$^-1$]')
# f3.savefig('//cantus.ads.warwick.ac.uk/User44/u/u2088308/Documents/My Pictures/Thesis Images/Circulation_plot_new_data.png', dpi = 400)
plt.legend()

f4, ax4 = plt.subplots(nrows=1, ncols=1)
plt.title('Core Axial Position against time')
ax4.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[0,start_frame:end_frame,1], label = f'Len = {Len[0]}', ) # L = 25
ax4.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[1,start_frame:end_frame,1], label = f'Len = {Len[1]}', ) # L = 50
ax4.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[2,start_frame:end_frame,1], label = f'Len = {Len[2]}', ) # L = 75
ax4.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[3,start_frame:end_frame,1], label = f'Len = {Len[3]}', ) # L = 100
ax4.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[4,start_frame:end_frame,1], label = f'Len = {Len[4]}', ) # L = 125
ax4.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[5,start_frame:end_frame,1], label = f'Len = {Len[5]}', ) # L = 150
ax4.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[6,start_frame:end_frame,1], label = f'Len = {Len[6]}', ) # L = 175
ax4.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[7,start_frame:end_frame,1], label = f'Len = {Len[7]}', ) # L = 200
ax4.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[8,start_frame:end_frame,1], label = f'Len = {Len[8]}', ) # L = 225
ax4.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[9,start_frame:end_frame,1], label = f'Len = {Len[9]}', ) # L = 240
ax4.set_xlabel(r'$t$[s]')
ax4.set_ylabel(r'$z$')
plt.legend()
# plt.show()

# repeat the test with old data

h5file = h5py.File('E:/H5/LengthTest.h5', 'r')
for i in range(len(Len)):
    print(Len[i])
    vels = h5file['Narrow']['U100'][Len[i]]['RPM0']
    u = vels[:,:,:,0]
    v = vels[:,:,:,1]
    u, v = oj.scaleVelNozzle(u, v, 90)
    VortLocMax, VortLocMin = oj.vorticityPeakTracking_inter(u[:,:,:], v[:,:,:]) # Axis 0 is radial, axis 1 is axial
    VortLocMin[:,0] = abs(np.subtract(VortLocMin[:,0], int(u.shape[1]/2)))
    VortLocMax[:,0] = np.subtract(VortLocMax[:,0], int(u.shape[1]/2))
    # VortLocAvg[i,:,:] = np.zeros([VortLocMax.shape[0], 2])
    VortLocAvg[i,:,:] = np.mean([VortLocMax, VortLocMin], axis = 0)
    # VortLocAvg[i,:,:] = VortLocMax[:,:]
    Circulation[i,:]  = oj.sum_Vorticity(u, v)

f5, ax5 = plt.subplots(nrows=1, ncols=1)
plt.title('Core Radial Position against time')
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[0,start_frame:end_frame,0], label = f'Len = {Len[0]}', ) # L = 25
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[1,start_frame:end_frame,0], label = f'Len = {Len[1]}', ) # L = 50
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[2,start_frame:end_frame,0], label = f'Len = {Len[2]}', ) # L = 75
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[3,start_frame:end_frame,0], label = f'Len = {Len[3]}', ) # L = 100
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[4,start_frame:end_frame,0], label = f'Len = {Len[4]}', ) # L = 125
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[5,start_frame:end_frame,0], label = f'Len = {Len[5]}', ) # L = 150
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[6,start_frame:end_frame,0], label = f'Len = {Len[6]}', ) # L = 175
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[7,start_frame:end_frame,0], label = f'Len = {Len[7]}', ) # L = 200
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[8,start_frame:end_frame,0], label = f'Len = {Len[8]}', ) # L = 225
ax5.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[9,start_frame:end_frame,0], label = f'Len = {Len[9]}', ) # L = 240
ax5.set_ylim([0, 50])
ax5.set_xlabel(r'$t$[s]')
ax5.set_ylabel(r'$r$')
plt.legend()



f6, ax6 = plt.subplots(nrows=1, ncols=1)
plt.title('Averaged Core Location in the first 5 seconds')
ax6.scatter(VortLocAvg[0,start_frame:end_frame,1],     VortLocAvg[0,start_frame:end_frame,0], label = f'Len = {Len[0]}') # L = 25
ax6.scatter(VortLocAvg[1,start_frame:end_frame,1],     VortLocAvg[1,start_frame:end_frame,0], label = f'Len = {Len[1]}') # L = 50
ax6.scatter(VortLocAvg[2,start_frame:end_frame,1],     VortLocAvg[2,start_frame:end_frame,0], label = f'Len = {Len[2]}') # L = 75
ax6.scatter(VortLocAvg[3,start_frame:end_frame,1],     VortLocAvg[3,start_frame:end_frame,0], label = f'Len = {Len[3]}') # L = 100
ax6.scatter(VortLocAvg[4,start_frame:end_frame,1],     VortLocAvg[4,start_frame:end_frame,0], label = f'Len = {Len[4]}') # L = 125
ax6.scatter(VortLocAvg[5,start_frame:end_frame,1],     VortLocAvg[5,start_frame:end_frame,0], label = f'Len = {Len[5]}') # L = 150
ax6.scatter(VortLocAvg[6,start_frame:end_frame,1],     VortLocAvg[6,start_frame:end_frame,0], label = f'Len = {Len[6]}') # L = 175
ax6.scatter(VortLocAvg[7,start_frame:end_frame,1],     VortLocAvg[7,start_frame:end_frame,0], label = f'Len = {Len[7]}') # L = 200
ax6.scatter(VortLocAvg[8,start_frame:end_frame,1],     VortLocAvg[8,start_frame:end_frame,0], label = f'Len = {Len[8]}') # L = 225
ax6.scatter(VortLocAvg[9,start_frame:end_frame,1],     VortLocAvg[9,start_frame:end_frame,0], label = f'Len = {Len[9]}') # L = 240
ax6.set_ylim([0, 50])
ax6.set_xlabel(r'$z$')
ax6.set_ylabel(r'$r$')
plt.legend()







f7, ax7 = plt.subplots(nrows=1, ncols=1, figsize=(5.5, 4))
plt.title('Vortex Ring Circulation Against Time')
ax7.scatter(Time[:(end_frame-start_frame)],     Circulation[0,start_frame:end_frame], label = f'Len = {Len[0]}', ) # L = 25
ax7.scatter(Time[:(end_frame-start_frame)],     Circulation[1,start_frame:end_frame], label = f'Len = {Len[1]}', ) # L = 50
ax7.scatter(Time[:(end_frame-start_frame)],     Circulation[2,start_frame:end_frame], label = f'Len = {Len[2]}', ) # L = 75
ax7.scatter(Time[:(end_frame-start_frame)],     Circulation[3,start_frame:end_frame], label = f'Len = {Len[3]}', ) # L = 100
ax7.scatter(Time[:(end_frame-start_frame)],     Circulation[4,start_frame:end_frame], label = f'Len = {Len[4]}', ) # L = 125
ax7.scatter(Time[:(end_frame-start_frame)],     Circulation[5,start_frame:end_frame], label = f'Len = {Len[5]}', ) # L = 150
ax7.scatter(Time[:(end_frame-start_frame)],     Circulation[6,start_frame:end_frame], label = f'Len = {Len[6]}', ) # L = 175
ax7.scatter(Time[:(end_frame-start_frame)],     Circulation[7,start_frame:end_frame], label = f'Len = {Len[7]}', ) # L = 200
ax7.scatter(Time[:(end_frame-start_frame)],     Circulation[8,start_frame:end_frame], label = f'Len = {Len[8]}', ) # L = 225
ax7.scatter(Time[:(end_frame-start_frame)],     Circulation[9,start_frame:end_frame], label = f'Len = {Len[9]}', ) # L = 240
ax7.set_xlabel(r'$t$[s]')
ax7.set_ylabel(r'$\Gamma$ [cm$^2$s$^-1$]')
f7.savefig('//cantus.ads.warwick.ac.uk/User44/u/u2088308/Documents/My Pictures/Thesis Images/Circulation_plot_old_data.png', dpi = 400)
plt.legend()

f8, ax8 = plt.subplots(nrows=1, ncols=1)
plt.title('Core Axial Position against time')
ax8.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[0,start_frame:end_frame,1], label = f'Len = {Len[0]}', ) # L = 25
ax8.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[1,start_frame:end_frame,1], label = f'Len = {Len[1]}', ) # L = 50
ax8.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[2,start_frame:end_frame,1], label = f'Len = {Len[2]}', ) # L = 75
ax8.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[3,start_frame:end_frame,1], label = f'Len = {Len[3]}', ) # L = 100
ax8.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[4,start_frame:end_frame,1], label = f'Len = {Len[4]}', ) # L = 125
ax8.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[5,start_frame:end_frame,1], label = f'Len = {Len[5]}', ) # L = 150
ax8.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[6,start_frame:end_frame,1], label = f'Len = {Len[6]}', ) # L = 175
ax8.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[7,start_frame:end_frame,1], label = f'Len = {Len[7]}', ) # L = 200
ax8.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[8,start_frame:end_frame,1], label = f'Len = {Len[8]}', ) # L = 225
ax8.scatter(Time[:(end_frame-start_frame)],     VortLocAvg[9,start_frame:end_frame,1], label = f'Len = {Len[9]}', ) # L = 240
ax8.set_xlabel(r'$t$[s]')
ax8.set_ylabel(r'$z$')
plt.legend()
plt.show()