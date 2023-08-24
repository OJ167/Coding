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
Stroke = ['L50', 'L100']
I = 'U100'
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

sumVorticity0  = oj.sum_Vorticity(u0mean [:,:,18:], v0mean [:,:,18:])
sumVorticity1  = oj.sum_Vorticity(u1mean [:,:,18:], v1mean [:,:,18:])
sumVorticity2  = oj.sum_Vorticity(u2mean [:,:,18:], v2mean [:,:,18:])
sumVorticity3  = oj.sum_Vorticity(u3mean [:,:,18:], v3mean [:,:,18:])
sumVorticity6  = oj.sum_Vorticity(u6mean [:,:,18:], v6mean [:,:,18:])
sumVorticity9  = oj.sum_Vorticity(u9mean [:,:,18:], v9mean [:,:,18:])
sumVorticity12 = oj.sum_Vorticity(u12mean[:,:,18:], v12mean[:,:,18:])


sumEnstrophy0  = oj.sum_Enstrophy(u0mean [:,:,18:], v0mean [:,:,18:])
sumEnstrophy1  = oj.sum_Enstrophy(u1mean [:,:,18:], v1mean [:,:,18:])
sumEnstrophy2  = oj.sum_Enstrophy(u2mean [:,:,18:], v2mean [:,:,18:])
sumEnstrophy3  = oj.sum_Enstrophy(u3mean [:,:,18:], v3mean [:,:,18:])
sumEnstrophy6  = oj.sum_Enstrophy(u6mean [:,:,18:], v6mean [:,:,18:])
sumEnstrophy9  = oj.sum_Enstrophy(u9mean [:,:,18:], v9mean [:,:,18:])
sumEnstrophy12 = oj.sum_Enstrophy(u12mean[:,:,18:], v12mean[:,:,18:])

f2, ax2 = plt.subplots(nrows=1, ncols=1)
plt.title("Enstrophy without stopping vortex 100/50, full")
ax2.plot(time, sumEnstrophy0 , label = "0 RPM")
ax2.plot(time, sumEnstrophy1 , label = "1 RPM")
ax2.plot(time, sumEnstrophy2 , label = "2 RPM")
ax2.plot(time, sumEnstrophy3 , label = "3 RPM")
ax2.plot(time, sumEnstrophy6 , label = "6 RPM")
ax2.plot(time, sumEnstrophy9 , label = "9 RPM")
ax2.plot(time, sumEnstrophy12, label = "12 RPM")
ax2.set_xlabel("time [s]")
ax2.set_ylabel("sum of Enstrophy")
plt.legend()
# plt.show()


Vorticity0r, Vorticity0  = oj.calculate_vorticity(u0mean, v0mean)
Vorticity1r, Vorticity1  = oj.calculate_vorticity(u1mean, v1mean)
Vorticity2r, Vorticity2  = oj.calculate_vorticity(u2mean, v2mean)
Vorticity3r, Vorticity3  = oj.calculate_vorticity(u3mean, v3mean)
Vorticity6r, Vorticity6  = oj.calculate_vorticity(u6mean, v6mean)
Vorticity9r, Vorticity9  = oj.calculate_vorticity(u9mean, v9mean)
Vorticity12r, Vorticity12 = oj.calculate_vorticity(u12mean, v12mean)


Enst0  = np.square(Vorticity0)
Enst1  = np.square(Vorticity1)
Enst2  = np.square(Vorticity2)
Enst3  = np.square(Vorticity3)
Enst6  = np.square(Vorticity6)
Enst9  = np.square(Vorticity9)
Enst12 = np.square(Vorticity12)

f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.imshow(Enst0[500,:,:])
# plt.show()


f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.contourf(z_nd, r_nd, Enst0[500,:,:], cmap = "Blues")
plt.title("Velocity Contour and Enstrophy Contour")

print(Enst0[500,10,10])

f3, (ax3, ax4) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
ax3.plot(u0mean [1000, 60, :])
ax4.plot(u12mean[1000, 60, :])
# plt.show()

### Finding a baseline where the 0RPM ring can be seen
f3, ax5 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
ax5.plot(Vorticity0 [1000, 68, :], label = "Row 68")
ax5.plot(Vorticity0 [1000, 60, :], label = "Row 60")
ax5.plot(Vorticity0 [1000, 50, :], label = "Row 50")
ax5.plot(Vorticity0 [1000, 40, :], label = "Row 40")
ax5.plot(Vorticity0 [1000, 30, :], label = "Row 30")
plt.legend()


f4, ax6 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
ax6.plot(z_nd, Vorticity0 [500, 0, :] , label = "Row 0")
ax6.plot(z_nd, Vorticity0 [500, 9, :] , label = "Row 10")
ax6.plot(z_nd, Vorticity0 [500, 19, :], label = "Row 20")
ax6.plot(z_nd, Vorticity0 [500, 29, :], label = "Row 30")
ax6.plot(z_nd, Vorticity0 [500, 35, :], label = "Row 35 (mid point)")
plt.title("Axial Vorticity Profile Frame 500 0RPM 100/50")
ax6.set_xlabel("z/D")
ax6.set_ylabel('Azimuthal Vorticity')
plt.legend()
# plt.show()












###### plots of time averaged flow ######

# v0mean  = np.mean(Vorticity0, axis = 0)
# v1mean  = np.mean(Vorticity1, axis = 0)
# v2mean  = np.mean(Vorticity2, axis = 0)
# v3mean  = np.mean(Vorticity3, axis = 0)
# v6mean  = np.mean(Vorticity6, axis = 0)
# v9mean  = np.mean(Vorticity9, axis = 0)
# v12mean = np.mean(Vorticity12, axis = 0)

# vmin = min(np.min(v0mean), np.min(v1mean), np.min(v3mean), np.min(v6mean), np.min(v9mean), np.min(v12mean))
# vmax = max(np.max(v0mean), np.max(v1mean), np.max(v3mean), np.max(v6mean), np.max(v9mean), np.max(v12mean))
# norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

# x = np.linspace(0 , u0mean.shape[2], u0mean.shape[2])
# y = np.linspace(0 , u0mean.shape[1], u0mean.shape[1])
# X, Y = np.meshgrid(x, y)

# fig, axs = plt.subplots(2, 3, sharex= True, sharey=True)
# axs[0, 0].contourf(X, Y, v0mean,  norm=norm, cmap = "seismic")
# # axs[0, 0].set_xlabel("z/D")
# # axs[0, 0].set_ylabel("r/D")
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
# plt.suptitle("Time averaged Vorticity 50/50")
# fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap="seismic"), ax=axs)
# plt.show()

svul0  = oj.sum_Vorticity(u0mean [:,:20,18:], v0mean [:,:20,18:]) +  oj.sum_Vorticity(u0mean [:,53:,18:], v0mean [:, 53:, 18:])
svul1  = oj.sum_Vorticity(u1mean [:,:20,18:], v1mean [:,:20,18:]) +  oj.sum_Vorticity(u1mean [:,53:,18:], v1mean [:, 53:, 18:])
svul2  = oj.sum_Vorticity(u2mean [:,:20,18:], v2mean [:,:20,18:]) +  oj.sum_Vorticity(u2mean [:,53:,18:], v2mean [:, 53:, 18:])
svul3  = oj.sum_Vorticity(u3mean [:,:20,18:], v3mean [:,:20,18:]) +  oj.sum_Vorticity(u3mean [:,53:,18:], v3mean [:, 53:, 18:])
svul6  = oj.sum_Vorticity(u6mean [:,:20,18:], v6mean [:,:20,18:]) +  oj.sum_Vorticity(u6mean [:,53:,18:], v6mean [:, 53:, 18:])
svul9  = oj.sum_Vorticity(u9mean [:,:20,18:], v9mean [:,:20,18:]) +  oj.sum_Vorticity(u9mean [:,53:,18:], v9mean [:, 53:, 18:])
svul12 = oj.sum_Vorticity(u12mean[:,:20,18:], v12mean[:,:20,18:]) +  oj.sum_Vorticity(u12mean[:,53:,18:], v12mean[:, 53:, 18:])

f5, ax7 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
ax7.plot(time, svul0[:] , label = "0 RPM")
ax7.plot(time, svul1[:] , label = "1 RPM")
ax7.plot(time, svul2[:] , label = "2 RPM")
ax7.plot(time, svul3[:] , label = "3 RPM")
ax7.plot(time, svul6[:] , label = "6 RPM")
ax7.plot(time, svul9[:] , label = "9 RPM")
ax7.plot(time, svul12[:], label = "12 RPM")
ax7.set_xlabel("T [s]")
ax7.set_ylabel('$\Gamma$')
plt.title("Circulation at large r 50/50")
plt.legend()


seul0  = oj.sum_Enstrophy(u0mean [:,:18,18:], v0mean [:,:18,18:]) +  oj.sum_Enstrophy(u0mean [:,51:,18:], v0mean [:, 51:, 18:])
seul1  = oj.sum_Enstrophy(u1mean [:,:18,18:], v1mean [:,:18,18:]) +  oj.sum_Enstrophy(u1mean [:,51:,18:], v1mean [:, 51:, 18:])
seul2  = oj.sum_Enstrophy(u2mean [:,:18,18:], v2mean [:,:18,18:]) +  oj.sum_Enstrophy(u2mean [:,51:,18:], v2mean [:, 51:, 18:])
seul3  = oj.sum_Enstrophy(u3mean [:,:18,18:], v3mean [:,:18,18:]) +  oj.sum_Enstrophy(u3mean [:,51:,18:], v3mean [:, 51:, 18:])
seul6  = oj.sum_Enstrophy(u6mean [:,:18,18:], v6mean [:,:18,18:]) +  oj.sum_Enstrophy(u6mean [:,51:,18:], v6mean [:, 51:, 18:])
seul9  = oj.sum_Enstrophy(u9mean [:,:18,18:], v9mean [:,:18,18:]) +  oj.sum_Enstrophy(u9mean [:,51:,18:], v9mean [:, 51:, 18:])
seul12 = oj.sum_Enstrophy(u12mean[:,:18,18:], v12mean[:,:18,18:]) +  oj.sum_Enstrophy(u12mean[:,51:,18:], v12mean[:, 51:, 18:])

f5, ax7 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
ax7.plot(time, seul0[:] , label = "0 RPM")
ax7.plot(time, seul1[:] , label = "1 RPM")
ax7.plot(time, seul2[:] , label = "2 RPM")
ax7.plot(time, seul3[:] , label = "3 RPM")
ax7.plot(time, seul6[:] , label = "6 RPM")
ax7.plot(time, seul9[:] , label = "9 RPM")
ax7.plot(time, seul12[:], label = "12 RPM")
ax7.set_xlabel("T [s]")
ax7.set_ylabel('Sum of Enstrophy')
plt.title("Enstrophy at large r 100/50")
plt.legend()


f6, ax8 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
plt.title("Axial velocity profile at the nozzle 0RPM 100/50")
ax8.plot(r_nd, u0mean[90,  :, 13], label = "0.0 Seconds")
ax8.plot(r_nd, u0mean[99,  :, 13], label = "0.1 Second")
ax8.plot(r_nd, u0mean[108, :, 13], label = "0.2 Seconds")
ax8.plot(r_nd, u0mean[117, :, 13], label = "0.3 Seconds")
ax8.plot(r_nd, u0mean[126, :, 13], label = "0.4 Seconds")
ax8.plot(r_nd, u0mean[135, :, 13], label = "0.5 Seconds")
plt.legend()

Vmag = np.sqrt(np.square(abs(v0mean)) + np.square(abs(u0mean)))
f6, ax8 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
plt.title("Velocity Magnitude profile at the nozzle 0RPM 100/50")
ax8.plot(r_nd, u0mean[82,  :, 14], label = "0 Seconds")
ax8.plot(r_nd, u0mean[170, :, 14], label = "1 Second")
ax8.plot(r_nd, u0mean[260, :, 14], label = "2 Seconds")
ax8.plot(r_nd, u0mean[350, :, 14], label = "3 Seconds")
ax8.plot(r_nd, u0mean[440, :, 14], label = "4 Seconds")
ax8.plot(r_nd, u0mean[530, :, 14], label = "5 Seconds")
plt.legend()
plt.show()

# f7, ax9 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
# plt.title("Axial velocity profile at the nozzle 1RPM 100/50")
# ax9.plot(r_nd, u1mean[170, :, 18], label = "1 Second")
# ax9.plot(r_nd, u1mean[260, :, 18], label = "2 Seconds")
# ax9.plot(r_nd, u1mean[350, :, 18], label = "3 Seconds")
# ax9.plot(r_nd, u1mean[440, :, 18], label = "4 Seconds")
# ax9.plot(r_nd, u1mean[530, :, 18], label = "5 Seconds")
# plt.legend()

# f8, ax10 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
# plt.title("Axial velocity profile at the nozzle 2RPM 100/50")
# ax10.plot(r_nd, u2mean[170, :, 18], label = "1 Second")
# ax10.plot(r_nd, u2mean[260, :, 18], label = "2 Seconds")
# ax10.plot(r_nd, u2mean[350, :, 18], label = "3 Seconds")
# ax10.plot(r_nd, u2mean[440, :, 18], label = "4 Seconds")
# ax10.plot(r_nd, u2mean[530, :, 18], label = "5 Seconds")
# plt.legend()

# f9, ax11 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
# plt.title("Axial velocity profile at the nozzle 3RPM 100/50")
# ax11.plot(r_nd, u3mean[170, :, 18], label = "1 Second")
# ax11.plot(r_nd, u3mean[260, :, 18], label = "2 Seconds")
# ax11.plot(r_nd, u3mean[350, :, 18], label = "3 Seconds")
# ax11.plot(r_nd, u3mean[440, :, 18], label = "4 Seconds")
# ax11.plot(r_nd, u3mean[530, :, 18], label = "5 Seconds")
# plt.legend()
# plt.show()



f6, ax8 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
plt.title("Radial velocity profile at the nozzle 0RPM 100/50")
ax8.plot(r_nd, v0mean[170, :, 18], label = "1 Second")
ax8.plot(r_nd, v0mean[260, :, 18], label = "2 Seconds")
ax8.plot(r_nd, v0mean[350, :, 18], label = "3 Seconds")
ax8.plot(r_nd, v0mean[440, :, 18], label = "4 Seconds")
ax8.plot(r_nd, v0mean[530, :, 18], label = "5 Seconds")
plt.legend()

f7, ax9 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
plt.title("Radial velocity profile at the nozzle 1RPM 100/50")
ax9.plot(r_nd, v1mean[170, :, 18], label = "1 Second")
ax9.plot(r_nd, v1mean[260, :, 18], label = "2 Seconds")
ax9.plot(r_nd, v1mean[350, :, 18], label = "3 Seconds")
ax9.plot(r_nd, v1mean[440, :, 18], label = "4 Seconds")
ax9.plot(r_nd, v1mean[530, :, 18], label = "5 Seconds")
plt.legend()

f8, ax10 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
plt.title("Radial velocity profile at the nozzle 2RPM 100/50")
ax10.plot(r_nd, v2mean[170, :, 18], label = "1 Second")
ax10.plot(r_nd, v2mean[260, :, 18], label = "2 Seconds")
ax10.plot(r_nd, v2mean[350, :, 18], label = "3 Seconds")
ax10.plot(r_nd, v2mean[440, :, 18], label = "4 Seconds")
ax10.plot(r_nd, v2mean[530, :, 18], label = "5 Seconds")
plt.legend()

f9, ax11 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
plt.title("Radial velocity profile at the nozzle 12RPM 100/50")
ax11.plot(r_nd, v12mean[170, :, 18], label = "1 Second")
ax11.plot(r_nd, v12mean[260, :, 18], label = "2 Seconds")
ax11.plot(r_nd, v12mean[350, :, 18], label = "3 Seconds")
ax11.plot(r_nd, v12mean[440, :, 18], label = "4 Seconds")
ax11.plot(r_nd, v12mean[530, :, 18], label = "5 Seconds")
plt.legend()
plt.show()

