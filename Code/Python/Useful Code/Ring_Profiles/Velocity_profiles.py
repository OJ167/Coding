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
from matplotlib import animation
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
Stroke = ['L50', 'L100']
I = 'U50'
S = 'L100'


h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[0])]
u0mean = vels[:,:,:,0]
v0mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[1])]
u1mean = vels[:,:,:,0]
v1mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[2])]
u2mean = vels[:,:,:,0]
v2mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[2])]
u3mean = vels[:,:,:,0]
v3mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[4])]
u6mean = vels[:,:,:,0]
v6mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[5])]
u9mean = vels[:,:,:,0]
v9mean = vels[:,:,:,1]

h5file = h5py.File('G:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[6])]
u12mean = vels[:,:,:,0]
v12mean = vels[:,:,:,1]

time = oj.frames_to_seconds(u0mean, v0mean, 90)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u0mean.shape[1], u0mean.shape[2])

#### Animation of Profiles ####





oj.animate_Line(u0mean)


vort0, gauss0 = oj.calculate_vorticity(u0mean, v0mean)
vort1, gauss1 = oj.calculate_vorticity(u1mean, v1mean)
vort2, gauss2 = oj.calculate_vorticity(u2mean, v2mean)
vort3, gauss3 = oj.calculate_vorticity(u3mean, v3mean)
vort6, gauss6 = oj.calculate_vorticity(u6mean, v6mean)
vort9, gauss9 = oj.calculate_vorticity(u9mean, v9mean)
vort12, gauss12 = oj.calculate_vorticity(u12mean, v12mean)

oj.animate_Line(gauss0)



#### Profiles in radial direction ####
###Row 13 is nozzle exit plane
row = 42
frame = 500

ylimitMAX = np.max((np.max(u0mean[100,:,13]),np.max(u1mean[100,:,13]),np.max(u2mean[100,:,13]),np.max(u3mean[100,:,13]),np.max(u6mean[100,:,13]),np.max(u9mean[100,:,13]),np.max(u12mean[100,:,13])))
ylimitMIN = np.min((np.min(u0mean[100,:,13]),np.min(u1mean[100,:,13]),np.min(u2mean[100,:,13]),np.min(u3mean[100,:,13]),np.min(u6mean[100,:,13]),np.min(u9mean[100,:,13]),np.min(u12mean[100,:,13])))

fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
axs[0, 0].plot(u0mean[frame,:,row])
axs[0, 0].set_xlabel("r/D")
axs[0, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[0, 1].plot(u1mean[frame,:,row])
axs[0, 1].set_xlabel("r/D")
axs[0, 1].set_ylim(ylimitMIN, ylimitMAX)
# axs[0, 1].plot(u2mean[100,:,row])

axs[0, 2].plot(u3mean[frame,:,row])
axs[0, 2].set_xlabel("r/D")
axs[0, 2].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 0].plot(u6mean[frame,:,row])
axs[1, 0].set_xlabel("r/D")
axs[1, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 1].plot(u9mean[frame,:,row])
axs[1, 1].set_xlabel("r/D")
axs[1, 1].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 2].plot(u12mean[frame,:,row])
axs[1, 2].set_xlabel("r/D")
axs[1, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[0, 0].set_title('0 RPM')
axs[0, 1].set_title('1 RPM')
# ax4.set_title('2 RPM')
axs[0, 2].set_title('3 RPM')
axs[1, 0].set_title('6 RPM')
axs[1, 1].set_title('9 RPM')
axs[1, 2].set_title('12 RPM')
plt.suptitle("Nozzle Exit Axial Velocity")
# plt.show()


#### Moving with 0RPM Ring Peak Vorticity

VortMax0, VortMin0 = oj.vorticityPeakTracking(u0mean, v0mean)


f1, ax1 = plt.subplots()
ax1.plot(VortMax0[:,1], label = "max")
ax1.plot(VortMin0[:,1], label = "min")
plt.show()

frame = 500
row = int(VortMax0[frame,1])

ylimitMAX = np.max((np.max(u0mean[frame,:,row]),np.max(u1mean[frame,:,row]),np.max(u2mean[frame,:,row]),np.max(u3mean[frame,:,row]),np.max(u6mean[frame,:,row]),np.max(u9mean[frame,:,row]),np.max(u12mean[frame,:,row])))
ylimitMIN = np.min((np.min(u0mean[frame,:,row]),np.min(u1mean[frame,:,row]),np.min(u2mean[frame,:,row]),np.min(u3mean[frame,:,row]),np.min(u6mean[frame,:,row]),np.min(u9mean[frame,:,row]),np.min(u12mean[frame,:,row])))


fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
axs[0, 0].plot(u0mean[frame,:,int(VortMax0[frame,1])])
axs[0, 0].set_xlabel("r/D")
axs[0, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[0, 1].plot(u1mean[frame,:,int(VortMax0[frame,1])])
axs[0, 1].set_xlabel("r/D")
axs[0, 1].set_ylim(ylimitMIN, ylimitMAX)
# axs[0, 1].plot(u2mean[100,:,int(VortMax0[frame,1])])

axs[0, 2].plot(u3mean[frame,:,int(VortMax0[frame,1])])
axs[0, 2].set_xlabel("r/D")
axs[0, 2].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 0].plot(u6mean[frame,:,int(VortMax0[frame,1])])
axs[1, 0].set_xlabel("r/D")
axs[1, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 1].plot(u9mean[frame,:,int(VortMax0[frame,1])])
axs[1, 1].set_xlabel("r/D")
axs[1, 1].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 2].plot(u12mean[frame,:,int(VortMax0[frame,1])])
axs[1, 2].set_xlabel("r/D")
axs[1, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[0, 0].set_title('0 RPM')
axs[0, 1].set_title('1 RPM')
# ax4.set_title('2 RPM')
axs[0, 2].set_title('3 RPM')
axs[1, 0].set_title('6 RPM')
axs[1, 1].set_title('9 RPM')
axs[1, 2].set_title('12 RPM')
plt.suptitle("Axial Velocity, Frame " + str(frame) + " row " + str(row))
# plt.show()

ylimitMAX = np.max((np.max(u0mean[frame,:,row]),np.max(u1mean[frame,:,row]),np.max(u2mean[frame,:,row]),np.max(u3mean[frame,:,row]),np.max(u6mean[frame,:,row]),np.max(u9mean[frame,:,row]),np.max(u12mean[frame,:,row])))
ylimitMIN = np.min((np.min(u0mean[frame,:,row]),np.min(u1mean[frame,:,row]),np.min(u2mean[frame,:,row]),np.min(u3mean[frame,:,row]),np.min(u6mean[frame,:,row]),np.min(u9mean[frame,:,row]),np.min(u12mean[frame,:,row])))


fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
axs[0, 0].plot(gauss0[frame,:,int(VortMax0[frame,1])])
axs[0, 0].set_xlabel("r/D")
axs[0, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[0, 1].plot(gauss1[frame,:,int(VortMax0[frame,1])])
axs[0, 1].set_xlabel("r/D")
axs[0, 1].set_ylim(ylimitMIN, ylimitMAX)
# axs[0, 1].plot(u2mean[100,:,int(VortMax0[frame,1])])

axs[0, 2].plot(gauss3[frame,:,int(VortMax0[frame,1])])
axs[0, 2].set_xlabel("r/D")
axs[0, 2].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 0].plot(gauss6[frame,:,int(VortMax0[frame,1])])
axs[1, 0].set_xlabel("r/D")
axs[1, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 1].plot(gauss9[frame,:,int(VortMax0[frame,1])])
axs[1, 1].set_xlabel("r/D")
axs[1, 1].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 2].plot(gauss12[frame,:,int(VortMax0[frame,1])])
axs[1, 2].set_xlabel("r/D")
axs[1, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[0, 0].set_title('0 RPM row '+ str(row))
axs[0, 1].set_title('1 RPM row '+ str(row))
# ax4.set_title('2 RPM row ', str(row2))
axs[0, 2].set_title('3 RPM row '+ str(row))
axs[1, 0].set_title('6 RPM row '+ str(row))
axs[1, 1].set_title('9 RPM row '+ str(row))
axs[1, 2].set_title('12 RPM row '+ str(row))
plt.suptitle("Azimuthal Vorticity, Frame "+ str(frame) + " row " + str(row))
plt.show()

#### Moving with Their Own Peak Vorticity

VortMax0 , VortMin0  = oj.vorticityPeakTracking(u0mean , v0mean )
VortMax1 , VortMin1  = oj.vorticityPeakTracking(u1mean , v1mean )
VortMax2 , VortMin2  = oj.vorticityPeakTracking(u2mean , v2mean )
VortMax3 , VortMin3  = oj.vorticityPeakTracking(u3mean , v3mean )
VortMax6 , VortMin6  = oj.vorticityPeakTracking(u6mean , v6mean )
VortMax9 , VortMin9  = oj.vorticityPeakTracking(u9mean , v9mean )
VortMax12, VortMin12 = oj.vorticityPeakTracking(u12mean, v12mean)


frame = 500
row0 = int(VortMax0[frame,1])
row1 = int(VortMax1[frame,1])
row2 = int(VortMax2[frame,1])
row3 = int(VortMax3[frame,1])
row6 = int(VortMax6[frame,1])
row9 = int(VortMax9[frame,1])
row12 = int(VortMax12[frame,1])

ylimitMAX = np.max((np.max(u0mean[frame,:,row0]),np.max(u1mean[frame,:,row1]),np.max(u2mean[frame,:,row2]),np.max(u3mean[frame,:,row3]),np.max(u6mean[frame,:,row6]),np.max(u9mean[frame,:,row9]),np.max(u12mean[frame,:,row12])))
ylimitMIN = np.min((np.min(u0mean[frame,:,row0]),np.min(u1mean[frame,:,row1]),np.min(u2mean[frame,:,row2]),np.min(u3mean[frame,:,row3]),np.min(u6mean[frame,:,row6]),np.min(u9mean[frame,:,row9]),np.min(u12mean[frame,:,row12])))


fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
axs[0, 0].plot(u0mean[frame,:,int(VortMax0[frame,1])])
axs[0, 0].set_xlabel("r/D")
axs[0, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[0, 1].plot(u1mean[frame,:,int(VortMax1[frame,1])])
axs[0, 1].set_xlabel("r/D")
axs[0, 1].set_ylim(ylimitMIN, ylimitMAX)
# axs[0, 1].plot(u2mean[100,:,int(VortMax2[frame,1])])

axs[0, 2].plot(u3mean[frame,:,int(VortMax3[frame,1])])
axs[0, 2].set_xlabel("r/D")
axs[0, 2].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 0].plot(u6mean[frame,:,int(VortMax6[frame,1])])
axs[1, 0].set_xlabel("r/D")
axs[1, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 1].plot(u9mean[frame,:,int(VortMax9[frame,1])])
axs[1, 1].set_xlabel("r/D")
axs[1, 1].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 2].plot(u12mean[frame,:,int(VortMax12[frame,1])])
axs[1, 2].set_xlabel("r/D")
axs[1, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[0, 0].set_title('0 RPM row '+ str(row0))
axs[0, 1].set_title('1 RPM row '+ str(row1))
# ax4.set_title('2 RPM row ', str(row2))
axs[0, 2].set_title('3 RPM row '+ str(row3))
axs[1, 0].set_title('6 RPM row '+ str(row6))
axs[1, 1].set_title('9 RPM row '+ str(row9))
axs[1, 2].set_title('12 RPM row '+ str(row12))
plt.suptitle("Axial Velocity, Frame "+ str(frame))
# plt.show()

f3, ax3 = plt.subplots()
ax3.plot(VortMax0[:,1], label = "0RPM")
ax3.plot(VortMax1[:,1], label = "1RPM")
ax3.plot(VortMax2[:,1], label = "2RPM")
ax3.plot(VortMax3[:,1], label = "3RPM")
ax3.plot(VortMax6[:,1], label = "6RPM")
ax3.plot(VortMax9[:,1], label = "9RPM")
ax3.plot(VortMax12[:,1], label = "12RPM")
plt.legend()
















ylimitMAX = np.max((np.max(u0mean[frame,:,row0]),np.max(u1mean[frame,:,row1]),np.max(u2mean[frame,:,row2]),np.max(u3mean[frame,:,row3]),np.max(u6mean[frame,:,row6]),np.max(u9mean[frame,:,row9]),np.max(u12mean[frame,:,row12])))
ylimitMIN = np.min((np.min(u0mean[frame,:,row0]),np.min(u1mean[frame,:,row1]),np.min(u2mean[frame,:,row2]),np.min(u3mean[frame,:,row3]),np.min(u6mean[frame,:,row6]),np.min(u9mean[frame,:,row9]),np.min(u12mean[frame,:,row12])))


fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
axs[0, 0].plot(gauss0[frame,:,int(VortMax0[frame,1])])
axs[0, 0].set_xlabel("r/D")
axs[0, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[0, 1].plot(gauss1[frame,:,int(VortMax1[frame,1])])
axs[0, 1].set_xlabel("r/D")
axs[0, 1].set_ylim(ylimitMIN, ylimitMAX)
# axs[0, 1].plot(u2mean[100,:,int(VortMax2[frame,1])])

axs[0, 2].plot(gauss3[frame,:,int(VortMax3[frame,1])])
axs[0, 2].set_xlabel("r/D")
axs[0, 2].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 0].plot(gauss6[frame,:,int(VortMax6[frame,1])])
axs[1, 0].set_xlabel("r/D")
axs[1, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 1].plot(gauss9[frame,:,int(VortMax9[frame,1])])
axs[1, 1].set_xlabel("r/D")
axs[1, 1].set_ylim(ylimitMIN, ylimitMAX)

axs[1, 2].plot(gauss12[frame,:,int(VortMax12[frame,1])])
axs[1, 2].set_xlabel("r/D")
axs[1, 0].set_ylim(ylimitMIN, ylimitMAX)

axs[0, 0].set_title('0 RPM row '+ str(row0))
axs[0, 1].set_title('1 RPM row '+ str(row1))
# ax4.set_title('2 RPM row ', str(row2))
axs[0, 2].set_title('3 RPM row '+ str(row3))
axs[1, 0].set_title('6 RPM row '+ str(row6))
axs[1, 1].set_title('9 RPM row '+ str(row9))
axs[1, 2].set_title('12 RPM row '+ str(row12))
plt.suptitle("Azimuthal Vorticity, Frame "+ str(frame))
plt.show()

# f3, ax3 = plt.subplots()
# ax3.plot(VortMax0[:,1], label = "0RPM")
# ax3.plot(VortMax1[:,1], label = "1RPM")
# ax3.plot(VortMax2[:,1], label = "2RPM")
# ax3.plot(VortMax3[:,1], label = "3RPM")
# ax3.plot(VortMax6[:,1], label = "6RPM")
# ax3.plot(VortMax9[:,1], label = "9RPM")
# ax3.plot(VortMax12[:,1], label = "12RPM")
# plt.legend()
# plt.show()





fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
axs[0, 0].contourf(u0mean[frame,:,:], cmap = "seismic")
axs[0, 0].set_xlabel("z/D")
axs[0, 0].set_ylabel("r/D")

axs[0, 1].contourf(u1mean[frame,:,:], cmap = "seismic")
axs[0, 1].set_xlabel("z/D")
axs[0, 1].set_ylabel("r/D")

axs[0, 2].contourf(u2mean[frame,:,:], cmap = "seismic")
# axs[0, 2].plot(u3mean[frame,:,int(VortMax0[frame,1])])
axs[0, 2].set_xlabel("z/D")
axs[0, 2].set_ylabel("r/D")

axs[1, 0].contourf(u6mean[frame,:,:], cmap = "seismic")
axs[1, 0].set_xlabel("z/D")
axs[1, 0].set_ylabel("r/D")

axs[1, 1].contourf(u9mean[frame,:,:], cmap = "seismic")
axs[1, 1].set_xlabel("z/D")
axs[1, 1].set_ylabel("r/D")

axs[1, 2].contourf(u12mean[frame,:,:], cmap = "seismic")
axs[1, 2].set_xlabel("z/D")
axs[1, 2].set_ylabel("r/D")

axs[0, 0].set_title('0 RPM')
axs[0, 1].set_title('1 RPM')
axs[0, 2].set_title('2 RPM')
# axs[0, 2].set_title('3 RPM')
axs[1, 0].set_title('6 RPM')
axs[1, 1].set_title('9 RPM')
axs[1, 2].set_title('12 RPM')
plt.suptitle("Axial Velocity, Frame " + str(frame))
plt.show()