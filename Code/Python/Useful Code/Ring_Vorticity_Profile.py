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
# u0,  v0 = oj.importData73("G:/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/Data/PIV_export.mat")
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

u0,  v0 = oj.importData("F:/NozzleFOV/RPM-0__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab.mat")
u3,  v3 = oj.importData("F:/NozzleFOV/RPM-3.0__Upiston-100__Stroke-100/2022-11-28__FPS-30/1/Data/PIVlab.mat")
u6,  v6 = oj.importData("F:/NozzleFOV/RPM-6.34__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab.mat")
u9,  v9 = oj.importData("F:/NozzleFOV/RPM-9.0__Upiston-100__Stroke-100/2022-11-28__FPS-30/1/Data/PIVlab.mat")

u_gaussian, v_gaussian = gaussian_filter(u, sigma=0.7), gaussian_filter(v, sigma=0.7)
vorticity, vorticity_gaussian = oj.calculate_vorticity(u_gaussian, v_gaussian)
VortLocMax, VortLocMin = oj.vorticityPeakTracking(u_gaussian, v_gaussian)

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




####3RPM
# Vorticity3_average_position = np.mean([VortLocMax_sav, VortLocMin_sav], axis=0)

# u3_gaussian, v3_gaussian = gaussian_filter(u3, sigma=0.7), gaussian_filter(v3, sigma=0.7)
# vorticity3, vorticity3_gaussian = oj.calculate_vorticity(u3_gaussian, v3_gaussian)
# VortLocMax3, VortLocMin3 = oj.vorticityPeakTracking(u3_gaussian, v3_gaussian)

# VortLocMax3_sav = np.zeros([VortLocMax3.shape[0], VortLocMax3.shape[1]])
# VortLocMax3_sav[:,1] = oj.FilterSpikes(VortLocMax3[:,1], 50)
# VortLocMax3_sav[:,1] = savgol_filter(VortLocMax3_sav[:,1], 21, 3)
# VortLocMax3_sav[:,0] = oj.FilterSpikes(VortLocMax3[:,0], 50)
# VortLocMax3_sav[:,0] = savgol_filter(VortLocMax3_sav[:,0], 21, 3)

# VortLocMin3_sav = np.zeros([VortLocMin3.shape[0], VortLocMin3.shape[1]])
# VortLocMin3_sav[:,1] = oj.FilterSpikes(VortLocMin3[:,1], 5)
# VortLocMin3_sav[:,1] = savgol_filter(VortLocMin3_sav[:,1], 21, 3)
# VortLocMin3_sav[:,0] = oj.FilterSpikes(VortLocMin3[:,0], 5)
# VortLocMin3_sav[:,0] = savgol_filter(VortLocMin3_sav[:,0], 21, 3)



####6RPM
# Vorticity6_average_position = np.mean([VortLocMax6_sav, VortLocMin6_sav], axis=0)

# u3_gaussian, v3_gaussian = gaussian_filter(u3, sigma=0.7), gaussian_filter(v3, sigma=0.7)
# vorticity3, vorticity3_gaussian = oj.calculate_vorticity(u3_gaussian, v3_gaussian)
# VortLocMax3, VortLocMin3 = oj.vorticityPeakTracking(u3_gaussian, v3_gaussian)

# VortLocMax3_sav = np.zeros([VortLocMax3.shape[0], VortLocMax3.shape[1]])
# VortLocMax3_sav[:,1] = oj.FilterSpikes(VortLocMax3[:,1], 50)
# VortLocMax3_sav[:,1] = savgol_filter(VortLocMax3_sav[:,1], 21, 3)
# VortLocMax3_sav[:,0] = oj.FilterSpikes(VortLocMax3[:,0], 50)
# VortLocMax3_sav[:,0] = savgol_filter(VortLocMax3_sav[:,0], 21, 3)

# VortLocMin3_sav = np.zeros([VortLocMin3.shape[0], VortLocMin3.shape[1]])
# VortLocMin3_sav[:,1] = oj.FilterSpikes(VortLocMin3[:,1], 5)
# VortLocMin3_sav[:,1] = savgol_filter(VortLocMin3_sav[:,1], 21, 3)
# VortLocMin3_sav[:,0] = oj.FilterSpikes(VortLocMin3[:,0], 5)
# VortLocMin3_sav[:,0] = savgol_filter(VortLocMin3_sav[:,0], 21, 3)






####9RPM
# Vorticityr_average_position = np.mean([VortLocMax3_sav, VortLocMin3_sav], axis=0)

# u3_gaussian, v3_gaussian = gaussian_filter(u3, sigma=0.7), gaussian_filter(v3, sigma=0.7)
# vorticity3, vorticity3_gaussian = oj.calculate_vorticity(u3_gaussian, v3_gaussian)
# VortLocMax3, VortLocMin3 = oj.vorticityPeakTracking(u3_gaussian, v3_gaussian)

# VortLocMax3_sav = np.zeros([VortLocMax3.shape[0], VortLocMax3.shape[1]])
# VortLocMax3_sav[:,1] = oj.FilterSpikes(VortLocMax3[:,1], 50)
# VortLocMax3_sav[:,1] = savgol_filter(VortLocMax3_sav[:,1], 21, 3)
# VortLocMax3_sav[:,0] = oj.FilterSpikes(VortLocMax3[:,0], 50)
# VortLocMax3_sav[:,0] = savgol_filter(VortLocMax3_sav[:,0], 21, 3)

# VortLocMin3_sav = np.zeros([VortLocMin3.shape[0], VortLocMin3.shape[1]])
# VortLocMin3_sav[:,1] = oj.FilterSpikes(VortLocMin3[:,1], 5)
# VortLocMin3_sav[:,1] = savgol_filter(VortLocMin3_sav[:,1], 21, 3)
# VortLocMin3_sav[:,0] = oj.FilterSpikes(VortLocMin3[:,0], 5)
# VortLocMin3_sav[:,0] = savgol_filter(VortLocMin3_sav[:,0], 21, 3)

Vorticityr_average_position = np.mean([VortLocMaxr_sav, VortLocMinr_sav], axis=0)

time = oj.frames_to_seconds(u, v, 30)
frame = 60
frameTime = frame/30


f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.plot(vorticity_gaussian[frame, :, int(Vorticity_average_position[frame,1])], label = f"Ring Velocity Profile at {frameTime} seconds")
plt.legend()


f2, ax2 = plt.subplots(nrows=1, ncols=1)
ax2.plot(time, VortLocMinr_sav[:,0], label = "Vortex z Position")
plt.legend()
# plt.show()

vortexMax_average_r = int(np.mean(VortLocMax[:,0])) 
vortexMin_average_r = int(np.mean(VortLocMin[:,0])) 

vortexMaxr_average_r = int(np.mean(VortLocMaxr[:,0])) 
vortexMinr_average_r = int(np.mean(VortLocMinr[:,0])) 



f3, (ax3, ax4,) = plt.subplots(nrows=2, ncols=1, sharex= True, sharey=True)
plt.title("Vorticity vs time contour")
z1 = ax3.contourf(vorticity_gaussian[:, vortexMaxr_average_r, 12:], cmap = "bwr") # max vorticity
z2 = ax4.contourf(vorticity_gaussian[:, vortexMinr_average_r, 12:], cmap = "bwr") # min vorticity
f3.colorbar(z1)
f3.colorbar(z2)
plt.show()