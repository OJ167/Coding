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
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

######## Importing multiple rings #####

#### 100/50 RINGS ####
Dir0  = "F:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90/"
u0mean, v0mean = oj.create_Mean(10, Dir0) 
u0mean, v0mean = oj.scaleVel(u0mean, v0mean, 90, 1900, 0.21918)
Dir1  = "F:/Testing/RPM-1.0__Upiston-100__Stroke-50/2023-07-24__FPS-90/"
u1mean, v1mean = oj.create_Mean(10, Dir1) 
u1mean, v1mean = oj.scaleVel(u1mean, v1mean, 90, 1900, 0.21918)
Dir2  = "F:/Testing/RPM-2.0__Upiston-100__Stroke-50/2023-07-25__FPS-90/"
u2mean, v2mean = oj.create_Mean(10, Dir2) 
u2mean, v2mean = oj.scaleVel(u2mean, v2mean, 90, 1900, 0.21918)
Dir3  = "F:/Testing/RPM-3.0__Upiston-100__Stroke-50/2023-05-15__FPS-90/"
u3mean, v3mean = oj.create_Mean(10, Dir3) 
u3mean, v3mean = oj.scaleVel(u3mean, v3mean, 90, 1900, 0.21918)
Dir6  = "F:/Testing/RPM-6.0__Upiston-100__Stroke-50/2023-05-11__FPS-90/"
u6mean, v6mean = oj.create_Mean(10, Dir6) 
u6mean, v6mean = oj.scaleVel(u6mean, v6mean, 90, 1900, 0.21918)
Dir9  = "F:/Testing/RPM-9.0__Upiston-100__Stroke-50/2023-05-12__FPS-90/"
u9mean, v9mean = oj.create_Mean(10, Dir9) 
u9mean, v9mean = oj.scaleVel(u9mean, v9mean, 90, 1900, 0.21918)
Dir12 = "F:/Testing/RPM-12.0__Upiston-100__Stroke-50/2023-05-19__FPS-90/"
u12mean, v12mean = oj.create_Mean(10, Dir12) 
u12mean, v12mean = oj.scaleVel(u12mean, v12mean, 90, 1900, 0.21918)

r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u0mean.shape[1], u0mean.shape[2])
time = oj.frames_to_seconds(u0mean, v0mean, 90)

##### full frame vorticity #####
sumVorticity0  = oj.sum_Vorticity(u0mean [:,:,18:], v0mean [:,:,18:])
print(sumVorticity0.shape)
maxloc0  = np.argmax(sumVorticity0)
print(maxloc0)
sumVorticity1  = oj.sum_Vorticity(u1mean [:,:,18:], v1mean [:,:,18:])
sumVorticity2  = oj.sum_Vorticity(u2mean [:,:,18:], v2mean [:,:,18:])
sumVorticity3  = oj.sum_Vorticity(u3mean [:,:,18:], v3mean [:,:,18:])
sumVorticity6  = oj.sum_Vorticity(u6mean [:,:,18:], v6mean [:,:,18:])
sumVorticity9  = oj.sum_Vorticity(u9mean [:,:,18:], v9mean [:,:,18:])
sumVorticity12 = oj.sum_Vorticity(u12mean[:,:,18:], v12mean[:,:,18:])

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.title("Circulation without stopping vortex 50/100, full")
ax16.plot(time, sumVorticity0, label = "0 RPM")
ax16.plot(time, sumVorticity1, label = "1 RPM")
ax16.plot(time, sumVorticity2, label = "2 RPM")
ax16.plot(time, sumVorticity3, label = "3 RPM")
ax16.plot(time, sumVorticity6, label = "6 RPM")
ax16.plot(time, sumVorticity9, label = "9 RPM")
ax16.plot(time, sumVorticity12, label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of vorticity")
plt.legend()


maxloc0  = np.argmax(sumVorticity0)
maxloc1  = np.argmax(sumVorticity1)
maxloc2  = np.argmax(sumVorticity2)
maxloc3  = np.argmax(sumVorticity3)
maxloc6  = np.argmax(sumVorticity6)
maxloc9  = np.argmax(sumVorticity9)
maxloc12 = np.argmax(sumVorticity12)

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.title("Circulation without stopping vortex 50/100, full")
ax16.scatter(maxloc0, sumVorticity0 [maxloc0] , label = "0 RPM")
ax16.scatter(maxloc1, sumVorticity1 [maxloc1] , label = "1 RPM")
ax16.scatter(maxloc2, sumVorticity2 [maxloc2] , label = "2 RPM")
ax16.scatter(maxloc3, sumVorticity3 [maxloc3] , label = "3 RPM")
ax16.scatter(maxloc6, sumVorticity6 [maxloc6] , label = "6 RPM")
ax16.scatter(maxloc9, sumVorticity9 [maxloc9] , label = "9 RPM")
ax16.scatter(maxloc12, sumVorticity12[maxloc12], label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of vorticity")
plt.legend()


normmaxloc1  = maxloc1  * 1 * 2 * np.pi / 60
normmaxloc2  = maxloc2  * 2 * 2 * np.pi / 60
normmaxloc3  = maxloc3  * 3 * 2 * np.pi / 60
normmaxloc6  = maxloc6  * 6 * 2 * np.pi / 60
normmaxloc9  = maxloc9  * 9 * 2 * np.pi / 60
normmaxloc12 = maxloc12 * 12 * 2 * np.pi / 60

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.title("Circulation without stopping vortex 50/100, full")
# ax16.plot(time, sumVorticity0 [normmaxloc0] , label = "0 RPM")
ax16.scatter(normmaxloc1, sumVorticity1 [normmaxloc1] , label = "1 RPM")
ax16.scatter(normmaxloc2, sumVorticity2 [normmaxloc2] , label = "2 RPM")
ax16.scatter(normmaxloc3, sumVorticity3 [normmaxloc3] , label = "3 RPM")
ax16.scatter(normmaxloc6, sumVorticity6 [normmaxloc6] , label = "6 RPM")
ax16.scatter(normmaxloc9, sumVorticity9 [normmaxloc9] , label = "9 RPM")
ax16.scatter(normmaxloc12, sumVorticity12[normmaxloc12], label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of vorticity")
plt.legend()


sumVorticity0  = oj.sum_Vorticity(u0mean [:,23:46, 18:], v0mean [:,23:46, 18:])
sumVorticity1  = oj.sum_Vorticity(u1mean [:,23:46, 18:], v1mean [:,23:46, 18:])
sumVorticity2  = oj.sum_Vorticity(u2mean [:,23:46, 18:], v2mean [:,23:46, 18:])
sumVorticity3  = oj.sum_Vorticity(u3mean [:,23:46, 18:], v3mean [:,23:46, 18:])
sumVorticity6  = oj.sum_Vorticity(u6mean [:,23:46, 18:], v6mean [:,23:46, 18:])
sumVorticity9  = oj.sum_Vorticity(u9mean [:,23:46, 18:], v9mean [:,23:46, 18:])
sumVorticity12 = oj.sum_Vorticity(u12mean[:,23:46, 18:], v12mean[:,23:46, 18:])

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.title("Circulation without stopping vortex 50/100, 23-46 middle 33%")
ax16.plot(time, sumVorticity0, label = "0 RPM")
ax16.plot(time, sumVorticity1, label = "1 RPM", color = "b")
ax16.plot(time, sumVorticity2, label = "2 RPM")
ax16.plot(time, sumVorticity3, label = "3 RPM")
ax16.plot(time, sumVorticity6, label = "6 RPM")
ax16.plot(time, sumVorticity9, label = "9 RPM")
ax16.plot(time, sumVorticity12, label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of vorticity")
plt.legend()


sumVorticity0  = oj.sum_Vorticity(u0mean [:,13:56,18:], v0mean [:,13:56,18:])
sumVorticity1  = oj.sum_Vorticity(u1mean [:,13:56,18:], v1mean [:,13:56,18:])
sumVorticity2  = oj.sum_Vorticity(u2mean [:,13:56,18:], v2mean [:,13:56,18:])
sumVorticity3  = oj.sum_Vorticity(u3mean [:,13:56,18:], v3mean [:,13:56,18:])
sumVorticity6  = oj.sum_Vorticity(u6mean [:,13:56,18:], v6mean [:,13:56,18:])
sumVorticity9  = oj.sum_Vorticity(u9mean [:,13:56,18:], v9mean [:,13:56,18:])
sumVorticity12 = oj.sum_Vorticity(u12mean[:,13:56,18:], v12mean[:,13:56,18:])

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.suptitle("Circulation without stopping vortex 50/100, 13-56 middle 60%")
ax16.plot(time, sumVorticity0, label = "0 RPM")
ax16.plot(time, sumVorticity1, label = "1 RPM")
ax16.plot(time, sumVorticity2, label = "2 RPM")
ax16.plot(time, sumVorticity3, label = "3 RPM")
ax16.plot(time, sumVorticity6, label = "6 RPM")
ax16.plot(time, sumVorticity9, label = "9 RPM")
ax16.plot(time, sumVorticity12, label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of vorticity")
plt.legend()

sumEnstrophy0 =  oj.sum_Enstrophy(u0mean [:,:,18:], v0mean [:,:,18:])
sumEnstrophy1 =  oj.sum_Enstrophy(u1mean [:,:,18:], v1mean [:,:,18:])
sumEnstrophy2 =  oj.sum_Enstrophy(u2mean [:,:,18:], v2mean [:,:,18:])
sumEnstrophy3 =  oj.sum_Enstrophy(u3mean [:,:,18:], v3mean [:,:,18:])
sumEnstrophy6 =  oj.sum_Enstrophy(u6mean [:,:,18:], v6mean [:,:,18:])
sumEnstrophy9 =  oj.sum_Enstrophy(u9mean [:,:,18:], v9mean [:,:,18:])
sumEnstrophy12 = oj.sum_Enstrophy(u12mean[:,:,18:], v12mean[:,:,18:])

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.suptitle("Enstrophy Full Frame - without stopping vortex 50/100")
ax16.plot(time, sumEnstrophy0, label = "0 RPM")
ax16.plot(time, sumEnstrophy1, label = "1 RPM")
ax16.plot(time, sumEnstrophy2, label = "2 RPM")
ax16.plot(time, sumEnstrophy3, label = "3 RPM")
ax16.plot(time, sumEnstrophy6, label = "6 RPM")
ax16.plot(time, sumEnstrophy9, label = "9 RPM")
ax16.plot(time, sumEnstrophy12, label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of enstrophy")
plt.legend()
plt.show()


#### 50/50 RINGS ####

# u0, v0 = oj.importData73("F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/4/Data/PIV_export.mat")
# u1, v1 = oj.importData73("F:/Testing/RPM-1.0__Upiston-50__Stroke-50/2023-07-24__FPS-90/4/Data/PIV_export.mat")
# u2, v2 = oj.importData73("F:/Testing/RPM-2.0__Upiston-50__Stroke-50/2023-07-25__FPS-90/4/Data/PIV_export.mat")
# u3, v3 = oj.importData73("F:/Testing/RPM-3.0__Upiston-50__Stroke-50/2023-05-23__FPS-90/4/Data/PIV_export.mat")
# u6, v6 = oj.importData73("F:/Testing/RPM-6.0__Upiston-50__Stroke-50/2023-06-07__FPS-90/4/Data/PIV_export.mat")
# u9, v9 = oj.importData73("F:/Testing/RPM-9.0__Upiston-50__Stroke-50/2023-05-24__FPS-90/4/Data/PIV_export.mat")
# u12, v12 = oj.importData73("F:/Testing/RPM-12.0__Upiston-50__Stroke-50/2023-05-19__FPS-90/4/Data/PIV_export.mat")

# Dir0  = "F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/"
# u0mean, v0mean = oj.create_Mean(10, Dir0) 
# u0mean, v0mean = oj.scaleVel(u0mean, v0mean, 90, 1900, 0.21918)
# Dir1  = "F:/Testing/RPM-1.0__Upiston-50__Stroke-50/2023-07-24__FPS-90/"
# u1mean, v1mean = oj.create_Mean(10, Dir1) 
# u1mean, v1mean = oj.scaleVel(u1mean, v1mean, 90, 1900, 0.21918)
# Dir2  = "F:/Testing/RPM-2.0__Upiston-50__Stroke-50/2023-07-25__FPS-90/"
# u2mean, v2mean = oj.create_Mean(10, Dir2) 
# u2mean, v2mean = oj.scaleVel(u2mean, v2mean, 90, 1900, 0.21918)
# Dir3  = "F:/Testing/RPM-3.0__Upiston-50__Stroke-50/2023-05-23__FPS-90/"
# u3mean, v3mean = oj.create_Mean(10, Dir3) 
# u3mean, v3mean = oj.scaleVel(u3mean, v3mean, 90, 1900, 0.21918)
# Dir6  = "F:/Testing/RPM-6.0__Upiston-50__Stroke-50/2023-06-07__FPS-90/"
# u6mean, v6mean = oj.create_Mean(10, Dir6) 
# u6mean, v6mean = oj.scaleVel(u6mean, v6mean, 90, 1900, 0.21918)
# Dir9  = "F:/Testing/RPM-9.0__Upiston-50__Stroke-50/2023-05-24__FPS-90/"
# u9mean, v9mean = oj.create_Mean(10, Dir9) 
# u9mean, v9mean = oj.scaleVel(u9mean, v9mean, 90, 1900, 0.21918)
# Dir12 = "F:/Testing/RPM-12.0__Upiston-50__Stroke-50/2023-05-19__FPS-90/"
# u12mean, v12mean = oj.create_Mean(10, Dir12) 
# u12mean, v12mean = oj.scaleVel(u12mean, v12mean, 90, 1900, 0.21918)
# r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u0mean.shape[1], u0mean.shape[2])


# time = oj.frames_to_seconds(u0mean, v0mean, 90)


# sumVorticity0  = oj.sum_Vorticity(u0mean [:,:,18:], v0mean [:,:,18:])
# sumVorticity1  = oj.sum_Vorticity(u1mean [:,:,18:], v1mean [:,:,18:])
# sumVorticity2  = oj.sum_Vorticity(u2mean [:,:,18:], v2mean [:,:,18:])
# sumVorticity3  = oj.sum_Vorticity(u3mean [:,:,18:], v3mean [:,:,18:])
# sumVorticity6  = oj.sum_Vorticity(u6mean [:,:,18:], v6mean [:,:,18:])
# sumVorticity9  = oj.sum_Vorticity(u9mean [:,:,18:], v9mean [:,:,18:])
# sumVorticity12 = oj.sum_Vorticity(u12mean[:,:,18:], v12mean[:,:,18:])

# f13, ax16 = plt.subplots(nrows=1, ncols=1)
# plt.title("Circulation without stopping vortex 50/50, full")
# ax16.plot(time, sumVorticity0, label = "0 RPM")
# ax16.plot(time, sumVorticity1, label = "1 RPM", color = "b")
# ax16.plot(time, sumVorticity2, label = "2 RPM")
# ax16.plot(time, sumVorticity3, label = "3 RPM")
# ax16.plot(time, sumVorticity6, label = "6 RPM")
# ax16.plot(time, sumVorticity9, label = "9 RPM")
# ax16.plot(time, sumVorticity12, label = "12 RPM")
# ax16.set_xlabel("time [s]")
# ax16.set_ylabel("sum of vorticity")
# plt.legend()

# sumVorticity0  = oj.sum_Vorticity(u0mean [:,23:46, 18:], v0mean [:,23:46, 18:])
# sumVorticity1  = oj.sum_Vorticity(u1mean [:,23:46, 18:], v1mean [:,23:46, 18:])
# sumVorticity2  = oj.sum_Vorticity(u2mean [:,23:46, 18:], v2mean [:,23:46, 18:])
# sumVorticity3  = oj.sum_Vorticity(u3mean [:,23:46, 18:], v3mean [:,23:46, 18:])
# sumVorticity6  = oj.sum_Vorticity(u6mean [:,23:46, 18:], v6mean [:,23:46, 18:])
# sumVorticity9  = oj.sum_Vorticity(u9mean [:,23:46, 18:], v9mean [:,23:46, 18:])
# sumVorticity12 = oj.sum_Vorticity(u12mean[:,23:46, 18:], v12mean[:,23:46, 18:])

# f13, ax16 = plt.subplots(nrows=1, ncols=1)
# plt.title("Circulation without stopping vortex 50/50, 23-46 middle 33%")
# ax16.plot(time, sumVorticity0, label = "0 RPM")
# ax16.plot(time, sumVorticity1, label = "1 RPM", color = "b")
# ax16.plot(time, sumVorticity2, label = "2 RPM")
# ax16.plot(time, sumVorticity3, label = "3 RPM")
# ax16.plot(time, sumVorticity6, label = "6 RPM")
# ax16.plot(time, sumVorticity9, label = "9 RPM")
# ax16.plot(time, sumVorticity12, label = "12 RPM")
# ax16.set_xlabel("time [s]")
# ax16.set_ylabel("sum of vorticity")
# plt.legend()


# sumVorticity0  = oj.sum_Vorticity(u0mean [:,13:56,18:], v0mean [:,13:56,18:])
# sumVorticity1  = oj.sum_Vorticity(u1mean [:,13:56,18:], v1mean [:,13:56,18:])
# sumVorticity2  = oj.sum_Vorticity(u2mean [:,13:56,18:], v2mean [:,13:56,18:])
# sumVorticity3  = oj.sum_Vorticity(u3mean [:,13:56,18:], v3mean [:,13:56,18:])
# sumVorticity6  = oj.sum_Vorticity(u6mean [:,13:56,18:], v6mean [:,13:56,18:])
# sumVorticity9  = oj.sum_Vorticity(u9mean [:,13:56,18:], v9mean [:,13:56,18:])
# sumVorticity12 = oj.sum_Vorticity(u12mean[:,13:56,18:], v12mean[:,13:56,18:])

# f13, ax16 = plt.subplots(nrows=1, ncols=1)
# plt.suptitle("Circulation without stopping vortex 50/50, 13-56 middle 60%")
# ax16.plot(time, sumVorticity0, label = "0 RPM")
# ax16.plot(time, sumVorticity1, label = "1 RPM")
# ax16.plot(time, sumVorticity2, label = "2 RPM")
# ax16.plot(time, sumVorticity3, label = "3 RPM")
# ax16.plot(time, sumVorticity6, label = "6 RPM")
# ax16.plot(time, sumVorticity9, label = "9 RPM")
# ax16.plot(time, sumVorticity12, label = "12 RPM")
# ax16.set_xlabel("time [s]")
# ax16.set_ylabel("sum of vorticity")
# plt.legend()

# sumEnstrophy0 =  oj.sum_Enstrophy(u0mean [:,:,18:], v0mean [:,:,18:])
# sumEnstrophy1 =  oj.sum_Enstrophy(u1mean [:,:,18:], v1mean [:,:,18:])
# sumEnstrophy2 =  oj.sum_Enstrophy(u2mean [:,:,18:], v2mean [:,:,18:])
# sumEnstrophy3 =  oj.sum_Enstrophy(u3mean [:,:,18:], v3mean [:,:,18:])
# sumEnstrophy6 =  oj.sum_Enstrophy(u6mean [:,:,18:], v6mean [:,:,18:])
# sumEnstrophy9 =  oj.sum_Enstrophy(u9mean [:,:,18:], v9mean [:,:,18:])
# sumEnstrophy12 = oj.sum_Enstrophy(u12mean[:,:,18:], v12mean[:,:,18:])

# f13, ax16 = plt.subplots(nrows=1, ncols=1)
# plt.suptitle("Enstrophy Full Frame - without stopping vortex 50/50")
# ax16.plot(time, sumEnstrophy0, label = "0 RPM")
# ax16.plot(time, sumEnstrophy1, label = "1 RPM")
# ax16.plot(time, sumEnstrophy2, label = "2 RPM")
# ax16.plot(time, sumEnstrophy3, label = "3 RPM")
# ax16.plot(time, sumEnstrophy6, label = "6 RPM")
# ax16.plot(time, sumEnstrophy9, label = "9 RPM")
# ax16.plot(time, sumEnstrophy12, label = "12 RPM")
# ax16.set_xlabel("time [s]")
# ax16.set_ylabel("sum of enstrophy")
# plt.legend()
# plt.show()