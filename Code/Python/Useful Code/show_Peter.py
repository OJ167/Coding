import numpy as np
import os
import sys
import mat73
import math as maths
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
from scipy.signal import medfilt
import matplotlib.pyplot as plt
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


# u0,  v0 = oj.importData73("G:/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/Data/PIV_export.mat")
# u3,  v3 = oj.importData73("G:/Testing/RPM-3.0__Upiston-200__Stroke-100/2023-03-14__FPS-60/2/Data/PIV_export.mat")
# u6,  v6 = oj.importData73("G:/Testing/RPM-6.0__Upiston-200__Stroke-100/2023-03-15__FPS-60/2/Data/PIV_export.mat")
# u9,  v9 = oj.importData73("G:/Testing/RPM-9.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/2/Data/PIV_export.mat")
u12,  v12 = oj.importData73("G:/Testing/RPM-12.0__Upiston-200__Stroke-100/2023-03-17__FPS-60/1/Data/PIV_export.mat")

u0, v0 = oj.importData73("F:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90/4/Data/PIV_export.mat")
u3, v3 = oj.importData73("F:/Testing/RPM-3.0__Upiston-100__Stroke-50/2023-05-15__FPS-90/4/Data/PIV_export.mat")
u6, v6 = oj.importData73("F:/Testing/RPM-6.0__Upiston-100__Stroke-50/2023-05-11__FPS-90/4/Data/PIV_export.mat")
u9, v9 = oj.importData73("F:/Testing/RPM-9.0__Upiston-100__Stroke-50/2023-05-12__FPS-90/4/Data/PIV_export.mat")

# u0,  v0 = oj.importData73("F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/PIV_export.mat")
# u3,  v3 = oj.importData73("F:/useful_data_copy_from_samsung/RPM-3.0__Upiston-200__Stroke-100/2023-02-14__FPS-60/1/PIV_export.mat")
# u6,  v6 = oj.importData73("F:/useful_data_copy_from_samsung/RPM-6.0__Upiston-200__Stroke-100/2023-03-15__FPS-60/1/PIV_export.mat")
# u9,  v9 = oj.importData73("F:/useful_data_copy_from_samsung/RPM-9.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/5/PIV_export.mat")



# u0,  v0 = oj.importData73("/Volumes/OllieSSD/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/Data/PIV_export.mat")
# u3,  v3 = oj.importData73("/Volumes/OllieSSD/Testing/RPM-3.0__Upiston-200__Stroke-100/2023-03-14__FPS-60/1/Data/PIV_export.mat")
# u6,  v6 = oj.importData73("/Volumes/OllieSSD/Testing/RPM-6.0__Upiston-200__Stroke-100/2023-03-15__FPS-60/1/Data/PIV_export.mat")
# u9,  v9 = oj.importData73("/Volumes/OllieSSD/Testing/RPM-9.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/5/Data/PIV_export.mat")

# u0,  v0 = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/PIV_export.mat")
# u3,  v3 = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-3.0__Upiston-200__Stroke-100/2023-02-14__FPS-60/8/PIV_export.mat")
# u6,  v6 = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-6.0__Upiston-200__Stroke-100/2023-03-15__FPS-60/8/PIV_export.mat")
# u9,  v9 = oj.importData73("/Volumes/Crucial X6//useful_data_copy_from_samsung/RPM-9.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/8/PIV_export.mat")
# u12, v12 = oj.importData73("/Volumes/Crucial X6/useful_data_copy_from_samsung/RPM-12.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/1/PIV_export.mat")

#### 0RPM
u0_gaussian, v0_gaussian = gaussian_filter(u0, sigma=0.7), gaussian_filter(v0, sigma=0.7)
vorticity0, vorticity_gaussian0 = oj.calculate_vorticity(u0, v0)
VortLocMax0, VortLocMin0 = oj.vorticityPeakTracking(u0_gaussian, v0_gaussian)

VortLocMax0_sav = np.zeros([VortLocMax0.shape[0], VortLocMax0.shape[1]])
VortLocMax0_sav[:,1] = oj.FilterSpikes(VortLocMax0[:,1], 5)
VortLocMax0_sav[:,1] = savgol_filter(VortLocMax0_sav[:,1], 21, 5)
VortLocMax0_sav[:,0] = oj.FilterSpikes(VortLocMax0[:,0], 5)
VortLocMax0_sav[:,0] = savgol_filter(VortLocMax0_sav[:,0], 21, 5)

VortLocMin0_sav = np.zeros([VortLocMin0.shape[0], VortLocMin0.shape[1]])
VortLocMin0_sav[:,1] = oj.FilterSpikes(VortLocMin0[:,1], 5)
VortLocMin0_sav[:,1] = savgol_filter(VortLocMin0_sav[:,1], 21, 5)
VortLocMin0_sav[:,0] = oj.FilterSpikes(VortLocMin0[:,0], 5)
VortLocMin0_sav[:,0] = savgol_filter(VortLocMin0_sav[:,0], 21, 5)
dx0 = VortLocMin0_sav[:,1] - VortLocMax0_sav[:,1]
dy0 = VortLocMin0_sav[:,0] - VortLocMax0_sav[:,0]
ring_diameter0 = np.sqrt(abs(dx0)**2 + abs(dy0)**2)


#### 3RPM
u3_gaussian, v3_gaussian = gaussian_filter(u3, sigma=0.7), gaussian_filter(v3, sigma=0.7)
vorticity3, vorticity_gaussian3 = oj.calculate_vorticity(u3, v3)
VortLocMax3, VortLocMin3 = oj.vorticityPeakTracking(u3_gaussian, v3_gaussian)

VortLocMax3_sav = np.zeros([VortLocMax3.shape[0], VortLocMax3.shape[1]])
VortLocMax3_sav[:,1] = oj.FilterSpikes(VortLocMax3[:,1], 5)
VortLocMax3_sav[:,1] = savgol_filter(VortLocMax3_sav[:,1], 21, 3)
VortLocMax3_sav[:,0] = oj.FilterSpikes(VortLocMax3[:,0], 5)
VortLocMax3_sav[:,0] = savgol_filter(VortLocMax3_sav[:,0], 21, 3)

VortLocMin3_sav = np.zeros([VortLocMin3.shape[0], VortLocMin3.shape[1]])
VortLocMin3_sav[:,1] = oj.FilterSpikes(VortLocMin3[:,1], 5)
VortLocMin3_sav[:,1] = savgol_filter(VortLocMin3_sav[:,1], 21, 3)
VortLocMin3_sav[:,0] = oj.FilterSpikes(VortLocMin3[:,0], 5)
VortLocMin3_sav[:,0] = savgol_filter(VortLocMin3_sav[:,0], 21, 3)
dx3 = VortLocMin3_sav[:,1] - VortLocMax3_sav[:,1]
dy3 = VortLocMin3_sav[:,0] - VortLocMax3_sav[:,0]
ring_diameter3 = np.sqrt(abs(dx3)**2 + abs(dy3)**2)

#### 6RPM
u6_gaussian, v6_gaussian = gaussian_filter(u6, sigma=0.7), gaussian_filter(v6, sigma=0.7)
vorticity6, vorticity_gaussian6 = oj.calculate_vorticity(u6, v6)
VortLocMax6, VortLocMin6 = oj.vorticityPeakTracking(u6_gaussian, v6_gaussian)

VortLocMax6_sav = np.zeros([VortLocMax6.shape[0], VortLocMax6.shape[1]])
VortLocMax6_sav[:,1] = oj.FilterSpikes(VortLocMax6[:,1], 5)
VortLocMax6_sav[:,1] = savgol_filter(VortLocMax6_sav[:,1], 21, 3)
VortLocMax6_sav[:,0] = oj.FilterSpikes(VortLocMax6[:,0], 5)
VortLocMax6_sav[:,0] = savgol_filter(VortLocMax6_sav[:,0], 21, 3)

VortLocMin6_sav = np.zeros([VortLocMin6.shape[0], VortLocMin6.shape[1]])
VortLocMin6_sav[:,1] = oj.FilterSpikes(VortLocMin6[:,1], 5)
VortLocMin6_sav[:,1] = savgol_filter(VortLocMin6_sav[:,1], 21, 3)
VortLocMin6_sav[:,0] = oj.FilterSpikes(VortLocMin6[:,0], 5)
VortLocMin6_sav[:,0] = savgol_filter(VortLocMin6_sav[:,0], 21, 3)
dx6 = VortLocMin6_sav[:,1] - VortLocMax6_sav[:,1]
dy6 = VortLocMin6_sav[:,0] - VortLocMax6_sav[:,0]
ring_diameter6 = np.sqrt(abs(dx6)**2 + abs(dy6)**2)

#### 9RPM
u9_gaussian, v9_gaussian = gaussian_filter(u9, sigma=0.7), gaussian_filter(v9, sigma=0.7)
vorticity9, vorticity_gaussian9 = oj.calculate_vorticity(u9, v9)
VortLocMax9, VortLocMin9 = oj.vorticityPeakTracking(u9_gaussian, v9_gaussian)

VortLocMax9_sav = np.zeros([VortLocMax9.shape[0], VortLocMax9.shape[1]])
VortLocMax9_sav[:,1] = oj.FilterSpikes(VortLocMax9[:,1], 5)
VortLocMax9_sav[:,1] = savgol_filter(VortLocMax9_sav[:,1], 21, 3)
VortLocMax9_sav[:,0] = oj.FilterSpikes(VortLocMax9[:,0], 5)
VortLocMax9_sav[:,0] = savgol_filter(VortLocMax9_sav[:,0], 21, 3)

VortLocMin9_sav = np.zeros([VortLocMin9.shape[0], VortLocMin9.shape[1]])
VortLocMin9_sav[:,1] = oj.FilterSpikes(VortLocMin9[:,1], 5)
VortLocMin9_sav[:,1] = savgol_filter(VortLocMin9_sav[:,1], 21, 3)
VortLocMin9_sav[:,0] = oj.FilterSpikes(VortLocMin9[:,0], 5)
VortLocMin9_sav[:,0] = savgol_filter(VortLocMin9_sav[:,0], 21, 3)
dx9 = VortLocMin9_sav[:,1] - VortLocMax9_sav[:,1]
dy9 = VortLocMin9_sav[:,0] - VortLocMax9_sav[:,0]
ring_diameter9 = np.sqrt(abs(dx9)**2 + abs(dy9)**2)

#### 12RPM
u12_gaussian, v12_gaussian = gaussian_filter(u12, sigma=0.7), gaussian_filter(v12, sigma=0.7)
vorticity12, vorticity_gaussian12 = oj.calculate_vorticity(u12, v12)
VortLocMax12, VortLocMin12 = oj.vorticityPeakTracking(u12_gaussian, v12_gaussian)

VortLocMax12_sav = np.zeros([VortLocMax12.shape[0], VortLocMax12.shape[1]])
VortLocMax12_sav[:,1] = oj.FilterSpikes(VortLocMax12[:,1], 50)
VortLocMax12_sav[:,1] = savgol_filter(VortLocMax12_sav[:,1], 21, 3)
VortLocMax12_sav[:,0] = oj.FilterSpikes(VortLocMax12[:,0], 50)
VortLocMax12_sav[:,0] = savgol_filter(VortLocMax12_sav[:,0], 21, 3)

VortLocMin12_sav = np.zeros([VortLocMin12.shape[0], VortLocMin12.shape[1]])
VortLocMin12_sav[:,1] = oj.FilterSpikes(VortLocMin12[:,1], 5)
VortLocMin12_sav[:,1] = savgol_filter(VortLocMin12_sav[:,1], 21, 3)
VortLocMin12_sav[:,0] = oj.FilterSpikes(VortLocMin12[:,0], 5)
VortLocMin12_sav[:,0] = savgol_filter(VortLocMin12_sav[:,0], 21, 3)
dx12 = VortLocMin12_sav[:,1] - VortLocMax12_sav[:,1]
dy12 = VortLocMin12_sav[:,0] - VortLocMax12_sav[:,0]
ring_diameter12 = np.sqrt(abs(dx12)**2 + abs(dy12)**2)



f1, ax1 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True, layout='constrained')
ax1.set_title("Line Length")
ax1.plot(ring_diameter0, label = "0 RPM")
ax1.plot(ring_diameter3, label = "3 RPM")
ax1.plot(ring_diameter6, label = "6 RPM")
ax1.plot(ring_diameter9, label = "9 RPM")
plt.xlabel("Time (frames at 60FPS)")
plt.ylabel("x Position")
plt.legend()
# plt.show()


f2, (ax2, ax3, ax4, ax5) = plt.subplots(nrows=4, ncols=1, sharex = True, sharey = True, layout='constrained')
ax1.set_title("Line Length")
ax2.plot(ring_diameter0, label = "0 RPM")
ax3.plot(ring_diameter3, label = "3 RPM")
ax4.plot(ring_diameter6, label = "6 RPM")
ax5.plot(ring_diameter9, label = "9 RPM")
plt.xlabel("Time (frames at 60FPS)")
plt.ylabel("x Position")
plt.legend()
# plt.show()


shapeX, shapeY = 1200, 1900
r_nd, z_nd, = oj.NDUnitsForPlotsWide(shapeX, shapeY, widthM = 0.66, HeightM = 1.066, jetLocPix = 600, pixX = 1200, d = 0.05)


f1, ax1 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
plt.title("Single Frame Axial Velocity")
ax1.contourf(u0_gaussian[500,:,:], cmap = "bwr")
ax1.xaxis.set_major_formatter(plt.NullFormatter())
ax1.yaxis.set_major_formatter(plt.NullFormatter())
# plt.show()

f1, ax1 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
plt.title("Single Frame Axial Velocity")
ax1.contourf(u9_gaussian[177,:,:], cmap = "bwr")
ax1.xaxis.set_major_formatter(plt.NullFormatter())
ax1.yaxis.set_major_formatter(plt.NullFormatter())

f2, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex = True, sharey = True)
ax1.set_title("u velocity")
ax1.contourf(u0_gaussian[500,:,:], cmap = "bwr")
ax1.xaxis.set_major_formatter(plt.NullFormatter())
ax1.yaxis.set_major_formatter(plt.NullFormatter())
ax2.set_title("v velocity")
ax2.contourf(v0_gaussian[500,:,:], cmap = "bwr")
ax2.xaxis.set_major_formatter(plt.NullFormatter())
ax2.yaxis.set_major_formatter(plt.NullFormatter())
# plt.show()

V_total = u0 + v0
f1, ax1 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
plt.title("Single Frame Axial Velocity")
ax1.contourf(V_total[500,:,:], cmap = "bwr")
ax1.xaxis.set_major_formatter(plt.NullFormatter())
ax1.yaxis.set_major_formatter(plt.NullFormatter())
# plt.show()


#### Plotting with Max Vorticity
f3, (ax15, ax25, ax35, ax45) = plt.subplots(nrows=4, ncols=1)
ax15 = plt.plot(VortLocMax0_sav[:,1], label = "0RPM")
ax25 = plt.plot(VortLocMax3_sav[:,1], label = "3RPM")
ax35 = plt.plot(VortLocMax6_sav[:,1], label = "6RPM")
ax45 = plt.plot(VortLocMax9_sav[:,1], label = "9RPM")
plt.legend()
plt.show()

time = oj.frames_to_seconds(u0, v0, 90)

f3, ax1 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
plt.title("Ring Displacement Axial Against Time")
ax1 = plt.plot(time[10:], VortLocMax0_sav[10:,1], label = "0RPM")
ax1 = plt.plot(time[10:1500],VortLocMax3_sav[10:1500,1], label = "3RPM")
ax1 = plt.plot(time[0:1000],VortLocMax6_sav[0:1000,1], label = "6RPM")
ax1 = plt.plot(time[45:1000],VortLocMax9_sav[45:1000,1], label = "9RPM")
# ax1 = plt.plot(time[:], VortLocMin12_sav[:,1], label = "Min 12RPM")
plt.ylabel("displacement")
plt.xlabel("time [s]")
plt.legend()
# plt.show()



f4, ax1 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
ax1 = plt.plot(VortLocMin0_sav[:,1], label = "Min 0RPM")
ax1 = plt.plot(VortLocMin3_sav[10:1600,1], label = "Min 3RPM")
ax1 = plt.plot(VortLocMin6_sav[0:1000,1], label = "Min 6RPM")
ax1 = plt.plot(VortLocMin9_sav[0:1000,1], label = "Min 9RPM")
plt.legend()
# plt.show()


VortLocMax0_medfilt = medfilt(VortLocMax0[:,1], kernel_size=7)

f5, ax1 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
ax1 = plt.plot(VortLocMax0_medfilt[:], label = "Min 0RPM")
ax1 = plt.plot(VortLocMax0_sav[:,1], label = "Min 0RPM")
plt.legend()
plt.show()


f2, ax3 = plt.subplots()
ax3.imshow(u0_gaussian[350,:,:])
plt.show()