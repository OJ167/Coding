import numpy as np
import os
import sys
import mat73
import math as maths
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm
from scipy.ndimage.filters import gaussian_filter


#####Import Ollie Tools
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

#####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding/Code"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

#####Import Rings
# u,  v = oj.importData73("G:/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/Data/PIV_export.mat")
# u3,  v3 = oj.importData73("G:/Testing/RPM-3.0__Upiston-200__Stroke-100/2023-03-14__FPS-60/1/Data/PIV_export.mat")
# u6,  v6 = oj.importData73("G:/Testing/RPM-6.0__Upiston-200__Stroke-100/2023-03-15__FPS-60/10/Data/PIV_export.mat")
# u9,  v9 = oj.importData73("G:/Testing/RPM-9.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/5/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-12.0__Upiston-200__Stroke-100/2023-03-17__FPS-60/1/Data/PIV_export.mat")

# u0,  v0 = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/PIV_export.mat")
# u3,  v3 = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-3.0__Upiston-200__Stroke-100/2023-02-14__FPS-60/8/PIV_export.mat")
# u6,  v6 = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-6.0__Upiston-200__Stroke-100/2023-03-15__FPS-60/8/PIV_export.mat")
# u9,  v9 = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-9.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/8/PIV_export.mat")
# u12, v12 = oj.importData73("/Volumes/Crucial X6/useful_data_copy_from_samsung/RPM-12.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/1/PIV_export.mat")

# u,  v = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/PIV_export.mat")
# u,  v = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-3.0__Upiston-200__Stroke-100/2023-02-14__FPS-60/8/PIV_export.mat")
# u,  v = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-6.0__Upiston-200__Stroke-100/2023-03-15__FPS-60/8/PIV_export.mat")
# u,  v = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-9.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/8/PIV_export.mat")
# ur,  vr = oj.importData73("/Volumes/Crucial X6/useful_data_copy_from_samsung/RPM-12.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/1/PIV_export.mat")

u,  v = oj.importData73("G:/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-3.0__Upiston-200__Stroke-100/2023-03-14__FPS-60/1/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-6.0__Upiston-200__Stroke-100/2023-03-15__FPS-60/1/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-9.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/5/Data/PIV_export.mat")
ur,  vr = oj.importData73("G:/Testing/RPM-12.0__Upiston-200__Stroke-100/2023-03-17__FPS-60/1/Data/PIV_export.mat")


#####Import GUI Rings Close to Nozzle

u,  v = oj.importData("F:/NozzleFOV/RPM-0__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab.mat")
u0,  v0 = oj.importData("F:/NozzleFOV/RPM-0__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab.mat")
u3,  v3 = oj.importData("F:/NozzleFOV/RPM-3.0__Upiston-100__Stroke-100/2022-11-28__FPS-30/1/Data/PIVlab.mat")
u6,  v6 = oj.importData("F:/NozzleFOV/RPM-6.34__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab.mat")
u9,  v9 = oj.importData("F:/NozzleFOV/RPM-9.0__Upiston-100__Stroke-100/2022-11-28__FPS-30/1/Data/PIVlab.mat")

u_gaussian, v_gaussian = gaussian_filter(u, sigma=0.7), gaussian_filter(v, sigma=0.7)
vorticity, vorticity_gaussian = oj.calculate_vorticity(u_gaussian, v_gaussian)
VortLocMax, VortLocMin = oj.vorticityPeakTracking(u_gaussian, v_gaussian)

ur_gaussian, vr_gaussian = gaussian_filter(ur, sigma=0.7), gaussian_filter(vr, sigma=0.7)
vorticityr, vorticityr_gaussian = oj.calculate_vorticity(ur_gaussian, vr_gaussian)
VortLocMaxr, VortLocMinr = oj.vorticityPeakTracking(ur_gaussian, vr_gaussian)

VortLocMax_sav = np.zeros([VortLocMax.shape[0], VortLocMax.shape[1]])
VortLocMax_sav[:,1] = oj.FilterSpikes(VortLocMax[:,1], 50)
VortLocMax_sav[:,1] = savgol_filter(VortLocMax_sav[:,1], 21, 3)
VortLocMax_sav[:,0] = oj.FilterSpikes(VortLocMax[:,0], 50)
VortLocMax_sav[:,0] = savgol_filter(VortLocMax_sav[:,0], 21, 3)

VortLocMin_sav = np.zeros([VortLocMin.shape[0], VortLocMin.shape[1]])
VortLocMin_sav[:,1] = oj.FilterSpikes(VortLocMin[:,1], 5)
VortLocMin_sav[:,1] = savgol_filter(VortLocMin_sav[:,1], 21, 3)
VortLocMin_sav[:,0] = oj.FilterSpikes(VortLocMin[:,0], 5)
VortLocMin_sav[:,0] = savgol_filter(VortLocMin_sav[:,0], 21, 3)

Vorticity_average_position = np.mean([VortLocMax_sav, VortLocMin_sav], axis=0)


time = oj.frames_to_seconds(u, v, 30)
frame = 90 ####Frame to be viewed
frameTime = frame/30


f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.plot(u_gaussian[frame, :, int(Vorticity_average_position[frame,1])], label = f"Ring Velocity Profile at {frameTime} seconds")
plt.legend()



#### all frames ####

f2, ax2 = plt.subplots(nrows=1, ncols=1)
for i in range(0, int(u.shape[0]), 30):
    itime = int(i/30)
    ax2.plot(u_gaussian[i, :, int(Vorticity_average_position[i,1])], label = f"Ring Velocity Profile at {itime} seconds")
plt.legend()




f3, ax3 = plt.subplots(nrows=1, ncols=1)
ax3.plot(time, Vorticity_average_position[:,1], label = "Vortex z Position")
plt.legend()


f4, ax4 = plt.subplots(nrows=1, ncols=1)
ax4.set_title("u at 2 seconds")
ax4.contourf(u_gaussian[60,:,:], cmap= "bwr")


f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.plot(u_gaussian[60, :, 20], label = f"Ring Velocity Profile at 1 second")
plt.legend()

f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.plot(u_gaussian[240, :, 20], label = f"Ring Velocity Profile at 8 seconds")
plt.legend()
# plt.show()

#### subtracting mean flow

u_mean = np.mean(u_gaussian, (0, 1, 2))

# f4, ax4 = plt.subplots(nrows=1, ncols=1)
# ax4.set_title("u mean")
# ax4.plot(u_mean)
# plt.show()

# u_relative = u_gaussian - u_mean

# f6, (ax6, ax7) = plt.subplots(nrows=2, ncols=1)
# ax6.set_title("u at 2 seconds")
# ax6.contourf(u_gaussian[60,:,:], cmap= "bwr")
# ax7.set_title("u_relative at 2 seconds")
# ax7.contourf(u_relative[60,:,:], cmap= "bwr")


# print("u mean: " + str(u_mean))
# print("u_gaussian:" + str(u_gaussian[60, 18, 25]))
# print("u_gaussian:" + str(u_relative[60, 18, 25]))


### subtracting time average

u_mean = np.mean(u_gaussian, 0)
print("u_mean shape " + str(u_mean.shape))

f4, ax4 = plt.subplots(nrows=1, ncols=1)
ax4.set_title("u mean")
ax4.contourf(u_mean)


u_relative = u_gaussian - u_mean

f6, (ax6, ax7) = plt.subplots(nrows=2, ncols=1)
ax6.set_title("u at 2 seconds")
ax6.contourf(u_gaussian[60,:,:], cmap= "bwr")
ax7.set_title("u_relative at 2 seconds")
ax7.contourf(u_relative[60,:,:], cmap= "bwr")


f7, (ax8, ax9) = plt.subplots(nrows=2, ncols=1)
ax8.plot(u_gaussian[60, :, 20], label = f"U gaussian Ring Velocity Profile at 1 second")
ax9.plot(u_relative[60, :, 20], label = f"U relative Ring Velocity Profile at 1 second")



f8, (ax10, ax11) = plt.subplots(nrows=2, ncols=1, sharex= True, sharey=True)
plt.title("Velocity profile vs Relative profile")
ax10.plot(u_gaussian[frame, :, int(Vorticity_average_position[frame,1])], label = f"Ring Velocity Profile at {frameTime} seconds")
ax10.legend()
ax11.plot(u_relative[frame, :, int(Vorticity_average_position[frame,1])], label = f"Ring Relative Velocity Profile at {frameTime} seconds")
ax11.legend()
# plt.show()

f9, ax12 = plt.subplots(nrows=1, ncols=1, sharex= True, sharey=True)
plt.title("Velocity profile vs Relative profile")
ax12.plot(u_gaussian[frame, :, int(Vorticity_average_position[frame,1])], label = f"Ring Velocity Profile at {frameTime} seconds")
ax12.plot(u_relative[frame, :, int(Vorticity_average_position[frame,1])], label = f"Ring Relative Velocity Profile at {frameTime} seconds")
ax12.legend()
# plt.show()




##### Plotting time series as contour

f10, (ax13, ax14,) = plt.subplots(nrows=2, ncols=1, sharex= True, sharey=True)
plt.title("Velocity profile vs time contour")
x = ax13.contourf(u_gaussian[:, 19, :])#, cmap = "bwr")
y = ax14.contourf(ur_gaussian[:, 19, :])#, cmap = "bwr")
f10.colorbar(x)
f10.colorbar(y)


f11, (ax15, ax16) = plt.subplots(nrows=2, ncols=1, sharex= True, sharey=True)
plt.suptitle("Velocity profile vs time contour")
levels = np.linspace(-0.02, 0.08, 11)
x = ax15.contourf(u_gaussian[:, 19, 12:], levels=levels, cmap='bwr')
y = ax16.contourf(ur_gaussian[:, 19, 12:], levels=levels, cmap='bwr')
ax15.set_title("0RPM")
ax15.set_xlabel("Axial Distance")
ax15.set_ylabel("Time [Frames (30FPS)]")
ax16.set_title("9RPM")
ax16.set_xlabel("Axial Distance")
ax16.set_ylabel("Time [Frames (30FPS)]")
f11.colorbar(x)
f11.colorbar(y)
# plt.show()




f12, ax17 = plt.subplots(nrows=1, ncols=1, sharex= True, sharey=True) 
x = np.linspace(0 , u_gaussian.shape[2], (u_gaussian.shape[2] + 1))
y = np.linspace(0 , u_gaussian.shape[0], (u_gaussian.shape[0] + 1))
X, Y = np.meshgrid(x, y)
Z = u_gaussian[:, 19, :]
vmin = np.amin(u_gaussian[:, 19, :])
vmax = np.amax(u_gaussian[:, 19, :])
norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
plt.pcolor(X, Y, Z,  norm=norm, cmap='bwr')
plt.colorbar()   
plt.show()

f13, ax18  = plt.subplots(nrows=1, ncols=1, sharex= True, sharey=True)
plt.suptitle("Velocity profile Against Time")
x = ax18.contourf(u_gaussian[:, 19, :], cmap='bwr')
ax18.set_title("12RPM")
ax18.set_xlabel("Axial Distance")
ax18.set_ylabel("Time [Frames (30FPS)]")
f13.colorbar(x)


#### plotting 4 at once
u0_gaussian, v0_gaussian = gaussian_filter(u0, sigma=0.7), gaussian_filter(v0, sigma=0.7)
u3_gaussian, v3_gaussian = gaussian_filter(u3, sigma=0.7), gaussian_filter(v3, sigma=0.7)
u6_gaussian, v6_gaussian = gaussian_filter(u6, sigma=0.7), gaussian_filter(v6, sigma=0.7)
u9_gaussian, v9_gaussian = gaussian_filter(u9, sigma=0.7), gaussian_filter(v9, sigma=0.7)

# Create some sample data
x = np.linspace(0 , u0_gaussian.shape[2], u0_gaussian.shape[2])
y = np.linspace(0 , u0_gaussian.shape[0], u0_gaussian.shape[0])
X, Y = np.meshgrid(x, y)
Z1 = u0_gaussian[:, 18, :]
Z2 = u3_gaussian[:, 18, :]
Z3 = u6_gaussian[:, 18, :]
Z4 = u9_gaussian[:, 18, :]
vmin = min(np.min(Z1), np.min(Z2), np.min(Z3), np.min(Z4))
vmax = max(np.max(Z1), np.max(Z2), np.max(Z3), np.max(Z4))
norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

fig, axs = plt.subplots(2, 2, sharex= True, sharey=True)
axs[0, 0].contourf(X, Y, Z1, norm=norm, cmap='bwr')
axs[0, 0].set_title('0RPM')
axs[0, 0].set_xlabel("Axial Distance")
axs[0, 0].set_ylabel("Time [Frames (60FPS)]")
axs[0, 1].contourf(X, Y, Z2, norm=norm, cmap='bwr')
axs[0, 1].set_title('3RPM')
axs[0, 1].set_xlabel("Axial Distance")
axs[0, 1].set_ylabel("Time [Frames (60FPS)]")
axs[1, 0].contourf(X, Y, Z3, norm=norm, cmap='bwr')
axs[1, 0].set_title('6RPM')
axs[1, 0].set_xlabel("Axial Distance")
axs[1, 0].set_ylabel("Time [Frames (60FPS)]")
axs[1, 1].contourf(X, Y, Z4, norm=norm, cmap='bwr')
axs[1, 1].set_title('9RPM')
axs[1, 1].set_xlabel("Axial Distance")
axs[1, 1].set_ylabel("Time [Frames (60FPS)]")
fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap="bwr"), ax=axs)
fig.suptitle('Velocity profile vs time contour')
plt.show()


vorticity0, vorticity_gaussian0 = oj.calculate_vorticity(u0_gaussian, v0_gaussian)
VortLocMax0, VortLocMin0 = oj.vorticityPeakTracking(u0_gaussian, v0_gaussian)
VortLocMax0_sav = np.zeros([VortLocMax0.shape[0], VortLocMax0.shape[1]])
VortLocMax0_sav[:,1] = oj.FilterSpikes(VortLocMax0[:,1], 50)
VortLocMax0_sav[:,1] = savgol_filter(VortLocMax0_sav[:,1], 21, 3)
VortLocMax0_sav[:,0] = oj.FilterSpikes(VortLocMax0[:,0], 50)
VortLocMax0_sav[:,0] = savgol_filter(VortLocMax0_sav[:,0], 21, 3)

VortLocMin0_sav = np.zeros([VortLocMin0.shape[0], VortLocMin0.shape[1]])
VortLocMin0_sav[:,1] = oj.FilterSpikes(VortLocMin0[:,1], 5)
VortLocMin0_sav[:,1] = savgol_filter(VortLocMin0_sav[:,1], 21, 3)
VortLocMin0_sav[:,0] = oj.FilterSpikes(VortLocMin0[:,0], 5)
VortLocMin0_sav[:,0] = savgol_filter(VortLocMin0_sav[:,0], 21, 3)
Vorticity_average_position0 = np.mean([VortLocMax0_sav, VortLocMin0_sav], axis=0)



vorticity3, vorticity_gaussian3 = oj.calculate_vorticity(u3_gaussian, v3_gaussian)
VortLocMax3, VortLocMin3 = oj.vorticityPeakTracking(u3_gaussian, v3_gaussian)
VortLocMax3_sav = np.zeros([VortLocMax3.shape[0], VortLocMax3.shape[1]])
VortLocMax3_sav[:,1] = oj.FilterSpikes(VortLocMax3[:,1], 50)
VortLocMax3_sav[:,1] = savgol_filter(VortLocMax3_sav[:,1], 21, 3)
VortLocMax3_sav[:,0] = oj.FilterSpikes(VortLocMax3[:,0], 50)
VortLocMax3_sav[:,0] = savgol_filter(VortLocMax3_sav[:,0], 21, 3)

VortLocMin3_sav = np.zeros([VortLocMin3.shape[0], VortLocMin3.shape[1]])
VortLocMin3_sav[:,1] = oj.FilterSpikes(VortLocMin3[:,1], 5)
VortLocMin3_sav[:,1] = savgol_filter(VortLocMin3_sav[:,1], 21, 3)
VortLocMin3_sav[:,0] = oj.FilterSpikes(VortLocMin3[:,0], 5)
VortLocMin3_sav[:,0] = savgol_filter(VortLocMin3_sav[:,0], 21, 3)
Vorticity_average_position3 = np.mean([VortLocMax3_sav, VortLocMin_sav], axis=0)




vorticity6, vorticity_gaussian6 = oj.calculate_vorticity(u6_gaussian, v6_gaussian)
VortLocMax6, VortLocMin6 = oj.vorticityPeakTracking(u6_gaussian, v6_gaussian)
VortLocMax6_sav = np.zeros([VortLocMax6.shape[0], VortLocMax6.shape[1]])
VortLocMax6_sav[:,1] = oj.FilterSpikes(VortLocMax6[:,1], 50)
VortLocMax6_sav[:,1] = savgol_filter(VortLocMax6_sav[:,1], 21, 3)
VortLocMax6_sav[:,0] = oj.FilterSpikes(VortLocMax6[:,0], 50)
VortLocMax6_sav[:,0] = savgol_filter(VortLocMax6_sav[:,0], 21, 3)

VortLocMin6_sav = np.zeros([VortLocMin6.shape[0], VortLocMin6.shape[1]])
VortLocMin6_sav[:,1] = oj.FilterSpikes(VortLocMin6[:,1], 5)
VortLocMin6_sav[:,1] = savgol_filter(VortLocMin6_sav[:,1], 21, 3)
VortLocMin6_sav[:,0] = oj.FilterSpikes(VortLocMin6[:,0], 5)
VortLocMin6_sav[:,0] = savgol_filter(VortLocMin6_sav[:,0], 21, 3)
Vorticity_average_position6 = np.mean([VortLocMax6_sav, VortLocMin6_sav], axis=0)



vorticity9, vorticity9_gaussian = oj.calculate_vorticity(u9_gaussian, v9_gaussian)
VortLocMax9, VortLocMin9 = oj.vorticityPeakTracking(u9_gaussian, v9_gaussian)
VortLocMax9_sav = np.zeros([VortLocMax9.shape[0], VortLocMax9.shape[1]])
VortLocMax9_sav[:,1] = oj.FilterSpikes(VortLocMax9[:,1], 50)
VortLocMax9_sav[:,1] = savgol_filter(VortLocMax9_sav[:,1], 21, 3)
VortLocMax9_sav[:,0] = oj.FilterSpikes(VortLocMax9[:,0], 50)
VortLocMax9_sav[:,0] = savgol_filter(VortLocMax9_sav[:,0], 21, 3)

VortLocMin9_sav = np.zeros([VortLocMin9.shape[0], VortLocMin9.shape[1]])
VortLocMin9_sav[:,1] = oj.FilterSpikes(VortLocMin9[:,1], 5)
VortLocMin9_sav[:,1] = savgol_filter(VortLocMin9_sav[:,1], 21, 3)
VortLocMin9_sav[:,0] = oj.FilterSpikes(VortLocMin9[:,0], 5)
VortLocMin9_sav[:,0] = savgol_filter(VortLocMin9_sav[:,0], 21, 3)
Vorticity_average_position9 = np.mean([VortLocMax9_sav, VortLocMin9_sav], axis=0)


time = oj.frames_to_seconds(u0, v0, 30)
frame = 30
frameTime = frame/30
f14, ax19 = plt.subplots(nrows=1, ncols=1)
plt.title(f"Ring Velocity Profile at {frameTime} seconds")
ax19.plot(u0_gaussian[frame, :, int(Vorticity_average_position0[frame,1])], label = "0RPM")
ax19.plot(u3_gaussian[frame, :, int(Vorticity_average_position0[frame,1])], label = "3RPM")
ax19.plot(u6_gaussian[frame, :, int(Vorticity_average_position0[frame,1])], label = "6RPM")
ax19.plot(u9_gaussian[frame, :, int(Vorticity_average_position0[frame,1])], label = "9RPM")
plt.legend()
# plt.show()


frame = 60
frameTime = frame/30
f14, ax19 = plt.subplots(nrows=1, ncols=1)
plt.title(f"Ring Velocity Profile at {frameTime} seconds")
ax19.plot(u0_gaussian[frame, :, int(Vorticity_average_position0[frame,1])], label = "0RPM")
ax19.plot(u3_gaussian[frame, :, int(Vorticity_average_position0[frame,1])], label = "3RPM")
ax19.plot(u6_gaussian[frame, :, int(Vorticity_average_position0[frame,1])], label = "6RPM")
ax19.plot(u9_gaussian[frame, :, int(Vorticity_average_position0[frame,1])], label = "9RPM")
plt.legend()
# plt.show()

frame = 45
frameTime = frame/30
f15, ax20 = plt.subplots(nrows=1, ncols=1)
plt.title(f"Ring Velocity Profile at {frameTime} seconds")
ax20.plot(u0_gaussian[frame, :, int(Vorticity_average_position0[frame,1])], label = "0RPM")
ax20.plot(u3_gaussian[frame, :, int(Vorticity_average_position3[frame,1])], label = "3RPM")
ax20.plot(u6_gaussian[frame, :, int(Vorticity_average_position6[frame,1])], label = "6RPM")
ax20.plot(u9_gaussian[frame, :, int(Vorticity_average_position9[frame,1])], label = "9RPM")
plt.legend()
# plt.show()


f16, ax21 = plt.subplots(nrows=1, ncols=1)
ax21.plot(Vorticity_average_position0[:,1], label = "0RPM")
ax21.plot(Vorticity_average_position3[:,1], label = "3RPM")
ax21.plot(Vorticity_average_position6[:,1], label = "6RPM")
ax21.plot(Vorticity_average_position9[:,1], label = "9RPM")
plt.legend()
plt.show()

f22, (ax22, ax23, ax24, ax25) = plt.subplots(nrows=1, ncols=4)
plt.title("Ring Velocity Profile at 4 different rotation rates")
for i in range(0, int(u.shape[0]), 30):
    itime = int(i/30)
    ax22.plot(u0_gaussian[i, :, int(Vorticity_average_position[i,1])], label = "0RPM")
    ax23.plot(u3_gaussian[i, :, int(Vorticity_average_position[i,1])], label = "3RPM")
    ax24.plot(u6_gaussian[i, :, int(Vorticity_average_position[i,1])], label = "6RPM")
    ax25.plot(u9_gaussian[i, :, int(Vorticity_average_position[i,1])], label = "9RPM")
plt.legend()

f23, ax23 = plt.subplots(nrows=1, ncols=1)
plt.title("Ring Velocity Profile at 3RPM")
for i in range(0, int(u.shape[0]), 30):
    itime = int(i/30)
    ax23.plot(u3_gaussian[i, :, int(Vorticity_average_position[i,1])], label = f"Ring Velocity Profile at {itime} seconds")
plt.legend()

f24, ax24 = plt.subplots(nrows=1, ncols=1)
plt.title("Ring Velocity Profile at 6RPM")
for i in range(0, int(u.shape[0]), 30):
    itime = int(i/30)
    ax24.plot(u6_gaussian[i, :, int(Vorticity_average_position[i,1])], label = f"Ring Velocity Profile at {itime} seconds")
plt.legend()

f25, ax25 = plt.subplots(nrows=1, ncols=1)
plt.title("Ring Velocity Profile at 9RPM")
for i in range(0, int(u.shape[0]), 30):
    itime = int(i/30)
    ax25.plot(u9_gaussian[i, :, int(Vorticity_average_position[i,1])], label = f"Ring Velocity Profile at {itime} seconds")
plt.legend()


f26, ax26 = plt.subplots(nrows=1, ncols=1)
plt.title("Ring Velocity Profile at 0RPM")
for i in range(0, int(u.shape[0]), 30):
    itime = int(i/30)
    ax26.plot(u_gaussian[i, :, int(Vorticity_average_position[i,1])], label = f"Ring Velocity Profile at {itime} seconds")
plt.legend()

plt.show()