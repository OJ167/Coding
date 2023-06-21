import numpy as np
import os
import sys
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
# from colorspacious import cspace_converter

#####Import Ollie Tools
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)


##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("jet_r")


######## Importing multiple rings #####
n = 3
# u, v = oj.importData73("F:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/1/Data/PIV_export.mat")
# u, v = oj.importData73("F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-08__FPS-60/1/PIV_export.mat")
# u = np.zeros([n, u.shape[0], u.shape[1], u.shape[2]])
# v = np.zeros([n, v.shape[0], v.shape[1], v.shape[2]])

# for i in range(1, n+1):
#     u[(i-1),:,:,:], v[(i-1),:,:,:] = oj.importData73(f"F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-08__FPS-60/{i}/PIV_export.mat")
#######################################

#### Filter ####
# u_gaussian, v_gaussian = gaussian_filter(u, sigma=0.7), gaussian_filter(v, sigma=0.7)



#### Tracking multi rings with vorticity ####

# VortLocMax = np.zeros([n, u.shape[0], u.shape[1], u.shape[2]])
# VortLocMin = np.zeros([n, u.shape[0], u.shape[1], u.shape[2]])

# for i in range(n):
#     VortLocMax, VortLocMin = oj.vorticityPeakTracking_i(u_gaussian, v_gaussian)


# f2, ax3 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
# for i in range(n):
#     ax3.contourf(gaussian_filter(u_gaussian[(n-1), 1000,:,:], sigma = 0.4))
#     VortLocMax, VortLocMin,  = oj.vorticityPeakTracking_i(u_gaussian[i,:,:,:], v_gaussian[i,:,:,:])
#     print(VortLocMax.shape[0])
#     print(VortLocMax.shape[0])
#     # uMax_savgol = savgol_filter(uMax, uMax.shape[1], 50)
#     # ax3.plot(uMax_savgol, label = f"Ring {i}")
#     ax3.plot(VortLocMax[:,2], label = f"Ring {i}")
# plt.show()



##### Manual ring tracking #####

# u1,  v1  = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/1/Data/PIV_export.mat")
# u2,  v2  = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/2/Data/PIV_export.mat")
# u3,  v3  = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/3/Data/PIV_export.mat")
# u4,  v4  = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/4/Data/PIV_export.mat")
# u5,  v5  = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/5/Data/PIV_export.mat")
# u6,  v6  = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/6/Data/PIV_export.mat")
# u7,  v7  = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/7/Data/PIV_export.mat")
# u8,  v8  = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/8/Data/PIV_export.mat")
# u9,  v9  = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/9/Data/PIV_export.mat")
# u10, v10 = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/10/Data/PIV_export.mat")

u1,  v1  = oj.importData73(f"F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/1/PIV_export.mat")
u2,  v2  = oj.importData73(f"F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/2/PIV_export.mat")
u3,  v3  = oj.importData73(f"F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/3/PIV_export.mat")
u4,  v4  = oj.importData73(f"F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/4/PIV_export.mat")
u5,  v5  = oj.importData73(f"F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/5/PIV_export.mat")
u6,  v6  = oj.importData73(f"F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/6/PIV_export.mat")
u7,  v7  = oj.importData73(f"F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/7/PIV_export.mat")
u8,  v8  = oj.importData73(f"F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/PIV_export.mat")
u9,  v9  = oj.importData73(f"F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/9/PIV_export.mat")
u10, v10 = oj.importData73(f"F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/10/PIV_export.mat")

u1_gaussian,  v1_gaussian  = gaussian_filter(u1,  sigma=0.7), gaussian_filter(v1, sigma=0.7)
u2_gaussian,  v2_gaussian  = gaussian_filter(u2,  sigma=0.7), gaussian_filter(v2, sigma=0.7)
u3_gaussian,  v3_gaussian  = gaussian_filter(u3,  sigma=0.7), gaussian_filter(v3, sigma=0.7)
u4_gaussian,  v4_gaussian  = gaussian_filter(u4,  sigma=0.7), gaussian_filter(v4, sigma=0.7)
u5_gaussian,  v5_gaussian  = gaussian_filter(u5,  sigma=0.7), gaussian_filter(v5, sigma=0.7)
u6_gaussian,  v6_gaussian  = gaussian_filter(u6,  sigma=0.7), gaussian_filter(v6, sigma=0.7)
u7_gaussian,  v7_gaussian  = gaussian_filter(u7,  sigma=0.7), gaussian_filter(v7, sigma=0.7)
u8_gaussian,  v8_gaussian  = gaussian_filter(u8,  sigma=0.7), gaussian_filter(v8, sigma=0.7)
u9_gaussian,  v9_gaussian  = gaussian_filter(u9,  sigma=0.7), gaussian_filter(v9, sigma=0.7)
u10_gaussian, v10_gaussian = gaussian_filter(u10, sigma=0.7), gaussian_filter(v10, sigma=0.7)

VortLocMax1, VortLocMin1 = oj.vorticityPeakTracking(u1_gaussian, v1_gaussian)
VortLocMax2, VortLocMin2 = oj.vorticityPeakTracking(u2_gaussian, v2_gaussian)
VortLocMax3, VortLocMin3 = oj.vorticityPeakTracking(u3_gaussian, v3_gaussian)
VortLocMax4, VortLocMin4 = oj.vorticityPeakTracking(u4_gaussian, v4_gaussian)
VortLocMax5, VortLocMin5 = oj.vorticityPeakTracking(u5_gaussian, v5_gaussian)
VortLocMax6, VortLocMin6 = oj.vorticityPeakTracking(u6_gaussian, v6_gaussian)
VortLocMax7, VortLocMin7 = oj.vorticityPeakTracking(u7_gaussian, v7_gaussian)
VortLocMax8, VortLocMin8 = oj.vorticityPeakTracking(u8_gaussian, v8_gaussian)
VortLocMax9, VortLocMin9 = oj.vorticityPeakTracking(u9_gaussian, v9_gaussian)
VortLocMax10, VortLocMin10 = oj.vorticityPeakTracking(u10_gaussian, v10_gaussian)

f1, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10) = plt.subplots(nrows=10, ncols=1)
plt.title("tracking rings with vorticity")
ax1.plot(VortLocMax1[:,1], label = "ring 1")
ax2.plot(VortLocMax2[:,1], label = "ring 2")
ax3.plot(VortLocMax3[:,1], label = "ring 3")
ax4.plot(VortLocMax4[:,1], label = "ring 4")
ax5.plot(VortLocMax5[:,1], label = "ring 5")
ax6.plot(VortLocMax6[:,1], label = "ring 6")
ax7.plot(VortLocMax7[:,1], label = "ring 7")
ax8.plot(VortLocMax8[:,1], label = "ring 8")
ax9.plot(VortLocMax9[:,1], label = "ring 9")
ax10.plot(VortLocMax10[:,1], label = "ring 10")
plt.legend()
# plt.show()

f2, ax1 = plt.subplots(nrows=1, ncols=1)
plt.title("tracking rings with vorticity")
ax1.plot(VortLocMax1[:,1], label = "ring 1")
ax1.plot(VortLocMax2[:,1], label = "ring 2")
ax1.plot(VortLocMax3[:,1], label = "ring 3")
ax1.plot(VortLocMax4[:,1], label = "ring 4")
ax1.plot(VortLocMax5[:,1], label = "ring 5")
ax1.plot(VortLocMax6[:,1], label = "ring 6")
ax1.plot(VortLocMax7[:,1], label = "ring 7")
ax1.plot(VortLocMax8[:,1], label = "ring 8")
ax1.plot(VortLocMax9[:,1], label = "ring 9")
ax1.plot(VortLocMax10[:,1], label = "ring 10")
plt.legend()

# plt.show()



#################################################################################################################
# Other plots to show Peter
#################################################################################################################

vorticity10, vorticity_gaussian10 = oj.calculate_vorticity(u10, v10)

f1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
ax1.contourf(u10_gaussian[1100,:,:])
ax2.contourf(vorticity_gaussian10[1100,:,:])
plt.title("velocity vs vorticity at frame 1100")
# plt.show()


vorticity3, vorticity_gaussian3 = oj.calculate_vorticity(u3, v3)

f1, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.scatter(VortLocMax3[75:, 1], VortLocMax3[75:, 0])
ax1.scatter(VortLocMin3[75:, 1], VortLocMin3[75:, 0])

# Ploting a midline
midline = np.zeros(vorticity_gaussian3.shape[0])
midline[:] = vorticity_gaussian3.shape[1]/2
ax1.plot(midline[0:vorticity_gaussian3.shape[2]])
plt.xlim([25, 50])
# plt.show()


VortLocMax1 , VortLocMin1  = oj.vorticityPeakTracking(u1_gaussian, v1_gaussian)
VortLocMax2 , VortLocMin2  = oj.vorticityPeakTracking(u2_gaussian, v2_gaussian)
VortLocMax3 , VortLocMin3  = oj.vorticityPeakTracking(u3_gaussian, v3_gaussian)
VortLocMax4 , VortLocMin4  = oj.vorticityPeakTracking(u4_gaussian, v4_gaussian)
VortLocMax5 , VortLocMin5  = oj.vorticityPeakTracking(u5_gaussian, v5_gaussian)
VortLocMax6 , VortLocMin6  = oj.vorticityPeakTracking(u6_gaussian, v6_gaussian)
VortLocMax7 , VortLocMin7  = oj.vorticityPeakTracking(u7_gaussian, v7_gaussian)
VortLocMax8 , VortLocMin8  = oj.vorticityPeakTracking(u8_gaussian, v8_gaussian)
VortLocMax9 , VortLocMin9  = oj.vorticityPeakTracking(u9_gaussian, v9_gaussian)
VortLocMax10, VortLocMin10 = oj.vorticityPeakTracking(u10_gaussian, v10_gaussian)



VortLocMax1_spike  =  oj.FilterSpikes(VortLocMax1[:,1],  deviation = 5) 
VortLocMax2_spike  =  oj.FilterSpikes(VortLocMax2[:,1],  deviation = 5) 
VortLocMax3_spike  =  oj.FilterSpikes(VortLocMax3[:,1],  deviation = 5) 
VortLocMax4_spike  =  oj.FilterSpikes(VortLocMax4[:,1],  deviation = 5) 
VortLocMax5_spike  =  oj.FilterSpikes(VortLocMax5[:,1],  deviation = 5) 
VortLocMax6_spike  =  oj.FilterSpikes(VortLocMax6[:,1],  deviation = 5) 
VortLocMax7_spike  =  oj.FilterSpikes(VortLocMax7[:,1],  deviation = 5) 
VortLocMax8_spike  =  oj.FilterSpikes(VortLocMax8[:,1],  deviation = 5) 
VortLocMax9_spike  =  oj.FilterSpikes(VortLocMax9[:,1],  deviation = 5) 
VortLocMax10_spike =  oj.FilterSpikes(VortLocMax10[:,1], deviation = 5)

f1, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10) = plt.subplots(nrows=10, ncols=1)
plt.title("Filtered")
ax1.plot(VortLocMax1_spike[:], label = "ring 1")
ax2.plot(VortLocMax2_spike[:], label = "ring 2")
ax3.plot(VortLocMax3_spike[:], label = "ring 3")
ax4.plot(VortLocMax4_spike[:], label = "ring 4")
ax5.plot(VortLocMax5_spike[:], label = "ring 5")
ax6.plot(VortLocMax6_spike[:], label = "ring 6")
ax7.plot(VortLocMax7_spike[:], label = "ring 7")
ax8.plot(VortLocMax8_spike[:], label = "ring 8")
ax9.plot(VortLocMax9_spike[:], label = "ring 9")
ax10.plot(VortLocMax10_spike[:], label = "ring 10")
plt.legend()
plt.show()

f1, ax1 = plt.subplots(nrows=1, ncols=1)
plt.title("Filtered")
ax1.plot(VortLocMax1_spike [:], label = "ring 1")
ax1.plot(VortLocMax2_spike [:], label = "ring 2")
ax1.plot(VortLocMax3_spike [:], label = "ring 3")
ax1.plot(VortLocMax4_spike [:], label = "ring 4")
ax1.plot(VortLocMax5_spike [:], label = "ring 5")
ax1.plot(VortLocMax6_spike [:], label = "ring 6")
ax1.plot(VortLocMax7_spike [:], label = "ring 7")
ax1.plot(VortLocMax8_spike [:], label = "ring 8")
ax1.plot(VortLocMax9_spike [:], label = "ring 9")
ax1.plot(VortLocMax10_spike[:], label = "ring 10")
plt.legend()
# plt.show()

f3, ax11 = plt.subplots(nrows=1, ncols=1)
ax11.loglog(VortLocMax3_spike[150:], label = "ring 3")
# plt.show()


f4, ax11 = plt.subplots(nrows=1, ncols=1)
ax11.plot(VortLocMax3_spike[150:], label = "ring 3")
plt.yscale("log")
plt.show()


time = oj.frames_to_seconds(u3, v3, 60)
f5, ax12 = plt.subplots(nrows=1, ncols=1)
plt.title("Location vs Log Time")
ax12.plot(VortLocMax3_spike[:], time, label = "ring 3")
plt.yscale("log")
plt.show()

#### different spike removal ####

VortLocMax8_5  = oj.FilterSpikes(VortLocMax8[:,1], 5)
VortLocMax8_10 = oj.FilterSpikes(VortLocMax8[:,1], 10)
VortLocMax8_20 = oj.FilterSpikes(VortLocMax8[:,1], 20)
VortLocMax8_40 = oj.FilterSpikes(VortLocMax8[:,1], 40)



f4, (ax13, ax14, ax15, ax16, ax17) = plt.subplots(nrows=5, ncols=1, sharex=True, sharey=True)
ax13.plot(VortLocMax8[:,1]   , label = "no")
ax14.plot(VortLocMax8_5[:] , label = "5")
ax15.plot(VortLocMax8_10[:], label = "10")
ax16.plot(VortLocMax8_20[:], label = "20")
ax17.plot(VortLocMax8_40[:], label = "40")
plt.legend()
# plt.show()

f5, ax18 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True)
ax18.plot(VortLocMax8[:,1]   , label = "no")
ax18.plot(VortLocMax8_5[:] , label = "5")
ax18.plot(VortLocMax8_10[:], label = "10")
ax18.plot(VortLocMax8_20[:], label = "20")
ax18.plot(VortLocMax8_40[:], label = "40")
plt.legend()
plt.show()