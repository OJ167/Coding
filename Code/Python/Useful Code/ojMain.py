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
# from colorspacious import cspace_converter

#####Import Ollie Tools
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)


####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding/Code"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("jet_r")



# u, v, vorticity = oj.importData("F:/Testing/RPM-6.34__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab")
# u, v, vort = oj.importData("F:/Testing/RPM-6.34__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab")
# vort = oj.importVorticity("F:/Testing/RPM-6.34__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab")

# u, v = oj.importData73("G:/Testing/RPM-3.0__Upiston-200__Stroke-100/2023-03-14__FPS-60/1/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-9.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/2/Data/PIV_export.mat")
# u, v = oj.importData73("G:/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-08__FPS-60/2/Data/PIV_export.mat")
# u, v = oj.importData("G:/Testing/PIV_Comparison/PIVlab_GUI")
# u, v = oj.importData73("G:/Testing/PIV_Comparison/PIV_export.mat")

u,  v = oj.importData73("G:/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-3.0__Upiston-200__Stroke-100/2023-03-14__FPS-60/1/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-6.0__Upiston-200__Stroke-100/2023-03-15__FPS-60/10/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-9.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/5/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-12.0__Upiston-200__Stroke-100/2023-03-17__FPS-60/1/Data/PIV_export.mat")


u_gaussian, v_gaussian = gaussian_filter(u, sigma=0.7), gaussian_filter(v, sigma=0.7)

time = oj.frames_to_seconds(u, v, 60)
print("time shape")
# print(time.shape)

#### Calculating kinetic energy ####
kinetic_energyt, sum_kinetic_energyt = oj.sum_kinetic_energy(u_gaussian[:,:,:], v_gaussian[:,:,:])
sum_kinetic_energy_max = max(sum_kinetic_energyt)
sum_kinetic_energy_max_location = np.argmax(sum_kinetic_energyt)

#### Kinetic Energy centre and sides####
kinetic_energy_left, sum_kinetic_energy_left = oj.sum_kinetic_energy(u_gaussian[:, :25,:], v_gaussian[:, :25,:])
kinetic_energy_mid, sum_kinetic_energy_mid = oj.sum_kinetic_energy(u_gaussian[:,25:50,:], v_gaussian[:,25:50,:])
kinetic_energy_right, sum_kinetic_energy_right = oj.sum_kinetic_energy(u_gaussian[:, 50: ,:], v_gaussian[:, 50: ,:])

sum_kinetic_energy_sides = sum_kinetic_energy_left + sum_kinetic_energy_right

resum_ke = sum_kinetic_energy_sides + sum_kinetic_energy_mid

f1, (ax1, ax2) = plt.subplots(nrows=1,ncols=2)
ax1.plot(sum_kinetic_energyt)
ax1.set_title("sum_kinetic_energyt")
ax2.plot(resum_ke)
ax2.set_title("resum_ke")
# plt.show()

#### calculate vorticity and track ####

VortLocMax, VortLocMin = oj.vorticityPeakTracking(u_gaussian, v_gaussian, u.shape[0])
VortLocMax_sav = np.zeros([VortLocMax.shape[0], VortLocMax.shape[1]])
VortLocMax_sav[:,1] = oj.FilterSpikes(VortLocMax[:,1], 50)
VortLocMax_sav[:,1] = savgol_filter(VortLocMax_sav[:,1], 21, 7)
VortLocMax_sav[:,0] = oj.FilterSpikes(VortLocMax[:,0], 50)
VortLocMax_sav[:,0] = savgol_filter(VortLocMax_sav[:,0], 21, 7)

VortLocMin_sav = np.zeros([VortLocMin.shape[0], VortLocMin.shape[1]])
VortLocMin_sav[:,1] = oj.FilterSpikes(VortLocMin[:,1], 5)
VortLocMin_sav[:,1] = savgol_filter(VortLocMin_sav[:,1], 21, 7)
VortLocMin_sav[:,0] = oj.FilterSpikes(VortLocMin[:,0], 5)
VortLocMin_sav[:,0] = savgol_filter(VortLocMin_sav[:,0], 21, 7)

#### average ring position ####
vort_local_avg = np.mean([VortLocMax_sav, VortLocMin_sav], axis=0)



f1, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, sharex = True, sharey = True)
plt.suptitle(f"Kinetic Energy against time 6RPM")
ax1.plot(time, vort_local_avg[:,1], c = "C1", label = "Ring Position")
ax1.plot(time, sum_kinetic_energyt, c = "C0", label = "Kinetic Energy")
ax1.set_title("Total Kinetic Energy")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Kinetic Energy")
ax2.plot(time, sum_kinetic_energy_mid, c = "C0", label = "Kinetic Energy")
ax2.set_title("Frame Centre Kinetic Energy")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Kinetic Energy")
ax3.plot(time, sum_kinetic_energy_sides, c = "C0", label = "Kinetic Energy")
ax3.set_title("Frame Edges Kinetic Energy")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Kinetic Energy")
ax1.legend()
ax2.legend()
ax3.legend()
# plt.show()


# f2, ax4 = plt.subplots(nrows=1, ncols=3, sharex = True, sharey = True)
# q = ax4.quiver(u.shape[2], u.shape[1], u[200,:,:], v[200,:,:])
# ax4.quiverkey(q, X=0.3, Y=1.1, U=10,
#              label='Quiver key, length = 10', labelpos='E')
# plt.show()


x, y = np.meshgrid(np.arange(0, u.shape[2], 1), np.arange(0, u.shape[1], 1))
print(u.shape[2])
print(u.shape[1])
f4, ax4 = plt.subplots()
ax4.quiver(x, y, u[200,:,:], v[200,:,:], pivot="middle")
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.set_title("Velocity")
# plt.show()


# oj.quivPlot(u_gaussian[200,:,:], v_gaussian[200,:,:])
# oj.animate_cube_quiver(u, v, interval=16.7, cmap="viridis", save=0, output="15.mp4", fps=60, scale = 1, fsize = (10, 8))




# f2, ax2 = plt.subplots(nrows=1, ncols=1)
# plt.title(f"frame with peak Ke is frame {str(sum_kinetic_energy_max_location)}")
# ax2.contourf(u[sum_kinetic_energy_max_location, :, :])
# plt.show()

# def lowOrderPolyfit(x, y, order):
#     z = np.polyfit(x, y, order)
#     p = np.poly1d(z)
#     xB = np.linspace(np.min(x), np.max(x), 100)
#     Xmax = xB[np.argmax(p(xB))]
#     return p, Xmax




# vorticity, vorticity_gauss = oj.calculate_vorticity(u, v)

# f2, (ax2, ax3) = plt.subplots(nrows=2, ncols=1)
# ax2.contourf(vorticity[100,:,:])
# ax3.contourf(vorticity_gauss[100,:,:])
# plt.show()



# oj.vorticityPeakTracking(u, v, l = 350)
# oj.PlotVelocity(u , v, 50)


#### inertial wave image
vfft_u = oj.IWFilter(u, 40, 60, 9)
vfft_v = oj.IWFilter(v, 40, 60, 9)
f1, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1)
ax1.contourf(vfft_u[500,:,:], cmap="bwr")
ax2.contourf(vfft_v[500,:,:], cmap="bwr")
# plt.show()


vfft_u = oj.IWFilter(u, 30, 60, 9)
vfft_u2 = oj.IWFilter(u, 75, 60, 9)
f2, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1)
ax1.contourf(vfft_u[500,:,:], cmap="bwr")
ax2.contourf(vfft_u2[500,:,:], cmap="bwr")
# plt.show()

# vfft_u = oj.IWFilter(u, 45, 60, 6)
# f2, ax1 = plt.subplots(nrows = 1, ncols = 1)
# ax1.contourf(vfft_u[500,:,:], cmap="bwr")
# plt.show()



#### Inertial Wave Video ####
# vfft_u = oj.IWFilter(u, 15, 60, 9)
# oj.animate_cube_contourf(vfft_u, 17)


######## Importing multiple rings #####
# n = 3
# u, v = oj.importData73("G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/1/Data/PIV_export.mat")
# u, v = oj.importData73("F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-08__FPS-60/8/PIV_export.mat")
# u = np.zeros([n, u.shape[0], u.shape[1], u.shape[2]])
# v = np.zeros([n, v.shape[0], v.shape[1], v.shape[2]])

# for i in range(1, n+1):
#     u[(i-1),:,:,:], v[(i-1),:,:,:] = oj.importData73(f"G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/{i}/Data/PIV_export.mat")
#     oj.progressBar(i)
#######################################



# u, v = oj.importData73("F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-08__FPS-60/8/PIV_export.mat")
# u_gaussian, v_gaussian = gaussian_filter(u, sigma=0.7), gaussian_filter(v, sigma=0.7)


# f1, (ax1, ax2)  = plt.subplots(nrows=2, ncols=1)
# ax1.contourf(u[1000,:,:])
# ax2.contourf(gaussian_filter(u_gaussian[1000,:,:], sigma = 0.7))
# plt.show()



# f1, (ax1, ax2)  = plt.subplots(nrows=2, ncols=1)
# ax1.contourf(u[2, 1000,:,:], label = "raw")
# ax2.contourf(gaussian_filter(u_gaussian[2, 1000,:,:], sigma = 0.4), label = "gaussian")
# plt.legend()
# plt.show()


# uMax = np.zeros(n, u.shape[1])
# uMin = np.zeros(n, u.shape[1])

# f1, ax1 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
# for i in range(n):
#     ax3.contourf(gaussian_filter(u_gaussian[(n-1), 1000,:,:], sigma = 0.4))
#     uMax, uMin,  = oj.velocityTracking(u_gaussian[i,:,:,:], v_gaussian[i,:,:,:])
#     ax1.plot(uMax, label = f"Ring {i}")
# plt.show()


# f2, ax2 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
# for i in range(n):
#     # ax2.contourf(gaussian_filter(u_gaussian[(n-1), 1000,:,:], sigma = 0.4))
#     uMax, uMin,  = oj.velocityTracking(u_gaussian[i,:,:,:], v_gaussian[i,:,:,:])
#     uMax_savgol = savgol_filter(uMax, uMax.shape[0], 5)
#     ax2.plot(uMax_savgol, label = f"Ring {i}")
# plt.show()

# f3, ax3 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
# for i in range(n):
#     # ax3.contourf(gaussian_filter(u_gaussian[(n-1), 1000,:,:], sigma = 0.4))
#     uMax, uMin,  = oj.velocityTracking(u_gaussian[i,:,:,:], v_gaussian[i,:,:,:])
#     uMax_sam_fil = oj.FilterSpikes(uMax, deviation = 5)
#     ax3.plot(uMax_sam_fil, label = f"Ring {i}")
# # plt.show()

### pandas dataframe

# f4, ax4 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
# for i in range(n):
#     # ax3.contourf(gaussian_filter(u_gaussian[(n-1), 1000,:,:], sigma = 0.4))
#     uMax, uMin,  = oj.velocityTracking(u_gaussian[i,:,:,:], v_gaussian[i,:,:,:])
#     uMax_pd = pd.DataFrame(5)
#     ax4.plot(uMax_pd, label = f"Ring {i}")
# plt.show()


# uMax_interp = np.interp(x, u_gaussian[0,:,0,0], uMax)

# f2, ax3 = plt.subplots(ncols=1, nrows=1, sharex=True, sharey=True)
# for i in range(n):
#     ax3.contourf(gaussian_filter(u_gaussian[(n-1), 1000,:,:], sigma = 0.4))
#     uMax, uMin,  = oj.velocityTracking(u_gaussian[i,:,:,:], v_gaussian[i,:,:,:])
#     a, b = np.polyfit(u_gaussian[0,:,0,0] , uMax, 1)
#     ax3.plot(a*uMax+b)
#     ax3.plot(gaussian_filter(uMax, sigma=0.99), label = f"Ring {i}")
#     ax3.plot(uMax_interp, label = f"Ring {i}")
# plt.show()


#### Tracking rings by vorticity ####

# vorticity, vorticity_gaussian = oj.calculate_vorticity(u, v)


# VortLocMax, VortLocMin = oj.vorticityPeakTracking(u_gaussian, v_gaussian)

# f1, ax1 = plt.subplots(nrows=1, ncols = 1, sharex=True, sharey=True)
# plt.title("max and min vorticity")
# ax1.plot(VortLocMax[150:,1], label = "local Max")
# ax1.plot(VortLocMin[150:,1], label = "local Min")
# plt.title("tracking rings with maximum positive and negative vorticity")
# plt.show()

# VortLocMax_x = VortLocMax[:,1]
# VortLocMax_y = VortLocMax[:,0]
# VortLocMaxSavgol = savgol_filter(VortLocMax_x, VortLocMax.shape[0], 10)


# f1, (ax1, ax2) = plt.subplots(nrows=2, ncols = 1)
# ax1.plot(VortLocMax[150:,1])
# ax2.plot(VortLocMaxSavgol[150:])
# plt.title("Savitzky–Golay filter")
# plt.show()


# uMax, uMin,  = oj.velocityTracking(u_gaussian[:,:], v_gaussian[:,:])
# f2, (ax3, ax4) = plt.subplots(nrows=2, ncols = 1)
# ax3.plot(uMax[150:])
# ax4.plot(VortLocMax[150:,1])
# plt.title("velocity vs vorticity tracking")
# plt.show()




##### Manual ring tracking #####

# u1, v1 = oj.importData73(f"F:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/1/Data/PIV_export.mat")
# u2, v2 = oj.importData73(f"F:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/2/Data/PIV_export.mat")
# u3, v3 = oj.importData73(f"F:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/3/Data/PIV_export.mat")
# u4, v4 = oj.importData73(f"F:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/4/Data/PIV_export.mat")
# u5, v5 = oj.importData73(f"F:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/5/Data/PIV_export.mat")

# u1_gaussian, v1_gaussian = gaussian_filter(u1, sigma=0.7), gaussian_filter(v1, sigma=0.7)
# u2_gaussian, v2_gaussian = gaussian_filter(u2, sigma=0.7), gaussian_filter(v2, sigma=0.7)
# u3_gaussian, v3_gaussian = gaussian_filter(u3, sigma=0.7), gaussian_filter(v3, sigma=0.7)
# u4_gaussian, v4_gaussian = gaussian_filter(u4, sigma=0.7), gaussian_filter(v4, sigma=0.7)
# u5_gaussian, v5_gaussian = gaussian_filter(u5, sigma=0.7), gaussian_filter(v5, sigma=0.7)

# uMax1, uMin1 = oj.velocityTracking(u1_gaussian, v1_gaussian)
# uMax2, uMin2 = oj.velocityTracking(u2_gaussian, v2_gaussian)
# uMax3, uMin3 = oj.velocityTracking(u3_gaussian, v3_gaussian)
# uMax4, uMin4 = oj.velocityTracking(u4_gaussian, v4_gaussian)
# uMax5, uMin5 = oj.velocityTracking(u5_gaussian, v5_gaussian)

# f1, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, ncols=1)
# ax1.plot(uMax1, label = "ring 1")
# ax2.plot(uMax2, label = "ring 2")
# ax3.plot(uMax3, label = "ring 3")
# ax4.plot(uMax4, label = "ring 4")
# ax5.plot(uMax5, label = "ring 5")
# plt.legend()
# plt.show()

# f2, ax1 = plt.subplots(nrows=1, ncols=1)
# ax1.plot(uMax1, label = "ring 1")
# ax1.plot(uMax2, label = "ring 2")
# ax1.plot(uMax3, label = "ring 3")
# ax1.plot(uMax4, label = "ring 4")
# ax1.plot(uMax5, label = "ring 5")
# plt.legend()
# plt.show()



###### Testing Area #####
# u,  v = oj.importData("F:/NozzleFOV/RPM-0__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab.mat")
# r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2], widthM = 0.13574, HeightM = 0.21719, jetLocPix = 600, pixX = 1200, d = 0.05)

# print("u shape: " + str(u.shape))
# print("r shape: " + str(r_nd.shape))
# print("z shape: "+ str(z_nd.shape))

# print(r_nd)
# print(z_nd)


# x, y = z_nd, r_nd
# f6, ax6 = plt.subplots()
# ax6.quiver(x, y, u[100,:,:], v[100,:,:], pivot="middle")
# ax6.set_xlabel('Z')
# ax6.set_ylabel('R')
# ax6.set_title("Velocity")


# f7, (ax7, ax8) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
# ax7.quiver(x, y, u[100,:,:], v[100,:,:], pivot="middle")
# ax7.set_xlabel('Z')
# ax7.set_ylabel('R')
# ax8.contourf(x, y, u[100,:,:])
# plt.show()


# u,  v = oj.importData73("G:/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/Data/PIV_export.mat")
# r_nd, z_nd = oj.NDUnitsForPlotsWide(u.shape[1], u.shape[2])

# x, y = z_nd, r_nd
# f8, ax9 = plt.subplots()
# ax9.quiver(z_nd, r_nd, u[200,:,:], v[200,:,:], pivot="middle")
# ax9.set_xlabel('Z')
# ax9.set_ylabel('R')
# ax9.set_title("Velocity")


# f9, (ax10, ax11) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
# ax10.quiver(x, y, u[200,:,:], v[200,:,:], pivot="middle")
# ax10.set_xlabel('Z')
# ax10.set_ylabel('R')
# ax11.contourf(x, y, u[200,:,:])


# f9, (ax12, ax13) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
# ax12.quiver(x, y, u_gaussian[200,:,:], v_gaussian[200,:,:], pivot="middle")
# ax12.set_xlabel('Z')
# ax12.set_ylabel('R')
# ax13.contourf(x, y, u_gaussian[200,:,:])
# plt.show()

u0, v0 = oj.importData73("F:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90/4/Data/PIV_export.mat")
u3, v3 = oj.importData73("F:/Testing/RPM-3.0__Upiston-100__Stroke-50/2023-05-15__FPS-90/4/Data/PIV_export.mat")
u6, v6 = oj.importData73("F:/Testing/RPM-6.0__Upiston-100__Stroke-50/2023-05-11__FPS-90/4/Data/PIV_export.mat")
u9, v9 = oj.importData73("F:/Testing/RPM-9.0__Upiston-100__Stroke-50/2023-05-12__FPS-90/4/Data/PIV_export.mat")
u12, v12 = oj.importData73("F:/Testing/RPM-12.0__Upiston-100__Stroke-50/2023-05-19__FPS-90/4/Data/PIV_export.mat")
u0_gaussian, v0_gaussian = gaussian_filter(u0, sigma=0.7), gaussian_filter(v0, sigma=0.7)
u3_gaussian, v3_gaussian = gaussian_filter(u3, sigma=0.7), gaussian_filter(v3, sigma=0.7)
u6_gaussian, v6_gaussian = gaussian_filter(u6, sigma=0.7), gaussian_filter(v6, sigma=0.7)
u9_gaussian, v9_gaussian = gaussian_filter(u9, sigma=0.7), gaussian_filter(v9, sigma=0.7)
u12_gaussian, v12_gaussian = gaussian_filter(u12, sigma=0.7), gaussian_filter(v12, sigma=0.7)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u0.shape[1], u0.shape[2])

x = np.linspace(0 , u0_gaussian.shape[2], u0_gaussian.shape[2])
y = np.linspace(0 , u0_gaussian.shape[0], u0_gaussian.shape[0])
X, Y = np.meshgrid(x, y)

Z1 = u0_gaussian[:, int(u0_gaussian.shape[1]/2), :]
Z2 = u3_gaussian[:, int(u0_gaussian.shape[1]/2), :]
Z3 = u6_gaussian[:, int(u0_gaussian.shape[1]/2), :]
Z4 = u9_gaussian[:, int(u0_gaussian.shape[1]/2), :]
vmin = min(np.min(u0_gaussian), np.min(u3_gaussian), np.min(u6_gaussian), np.min(u9_gaussian))
vmax = max(np.max(u0_gaussian), np.max(u3_gaussian), np.max(u6_gaussian), np.max(u9_gaussian))
norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
frame = 200
fig, axs = plt.subplots(2, 2, sharex= True, sharey=True)
axs[0, 0].contourf(z_nd, r_nd, u0_gaussian[frame,:,:], norm=norm, cmap='bwr')
axs[0, 0].quiver(z_nd, r_nd, u0_gaussian[frame,:,:], v0_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[0, 0].set_title('0RPM')
axs[0, 0].set_xlabel("z/D")
axs[0, 0].set_ylabel("r/D")
axs[0, 1].contourf(z_nd, r_nd, u3_gaussian[frame,:,:], norm=norm, cmap='bwr')
axs[0, 1].quiver(z_nd, r_nd, u3_gaussian[frame,:,:], v3_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[0, 1].set_title('3RPM')
axs[0, 1].set_xlabel("z/D")
axs[0, 1].set_ylabel("r/D")
axs[1, 0].contourf(z_nd, r_nd, u6_gaussian[frame,:,:], norm=norm, cmap='bwr')
axs[1, 0].quiver(z_nd, r_nd, u6_gaussian[frame,:,:], v6_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[1, 0].set_title('6RPM')
axs[1, 0].set_xlabel("z/D")
axs[1, 0].set_ylabel("r/D")
axs[1, 1].contourf(z_nd, r_nd, u9_gaussian[frame,:,:], norm=norm, cmap='bwr')
axs[1, 1].quiver(z_nd, r_nd, u9_gaussian[frame,:,:], v9_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[1, 1].set_title('9RPM')
axs[1, 1].set_xlabel("z/D")
axs[1, 1].set_ylabel("r/D")
fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap="bwr"), ax=axs)
fig.suptitle('Velocity at frame 200 (2.22s)')

x = np.linspace(0 , u0_gaussian.shape[2], u0_gaussian.shape[2])
y = np.linspace(0 , u0_gaussian.shape[0], u0_gaussian.shape[0])
X, Y = np.meshgrid(x, y)

Z1 = u0_gaussian[:, 35, :]
Z2 = u3_gaussian[:, 35, :]
Z3 = u6_gaussian[:, 35, :]
Z4 = u9_gaussian[:, 35, :]
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



time = oj.frames_to_seconds(u0, v0, 90)
sumVorticity0 = oj.sum_Vorticity(u0_gaussian[:,23:47,:], v0_gaussian[:,23:47,:])
sumVorticity3 = oj.sum_Vorticity(u3_gaussian[:,23:47,:], v3_gaussian[:,23:47,:])
sumVorticity6 = oj.sum_Vorticity(u6_gaussian[:,23:47,:], v6_gaussian[:,23:47,:])
sumVorticity9 = oj.sum_Vorticity(u9_gaussian[:,23:47,:], v9_gaussian[:,23:47,:])
sumVorticity12 = oj.sum_Vorticity(u12_gaussian[:,23:47,:], v12_gaussian[:,23:47,:])

f13, ax16 = plt.subplots(nrows=1, ncols=1)
ax16.plot(time, sumVorticity0, label = "0 RPM")
ax16.plot(time, sumVorticity3, label = "3 RPM")
ax16.plot(time, sumVorticity6, label = "6 RPM")
ax16.plot(time, sumVorticity9, label = "9 RPM")
ax16.plot(time, sumVorticity12, label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of vorticity")
plt.legend()


sumVorticity0 = oj.sum_Vorticity(u0_gaussian[:,13:56,18:], v0_gaussian[:,13:56,18:])
sumVorticity3 = oj.sum_Vorticity(u3_gaussian[:,13:56,18:], v3_gaussian[:,13:56,18:])
sumVorticity6 = oj.sum_Vorticity(u6_gaussian[:,13:56,18:], v6_gaussian[:,13:56,18:])
sumVorticity9 = oj.sum_Vorticity(u9_gaussian[:,13:56,18:], v9_gaussian[:,13:56,18:])
sumVorticity12 = oj.sum_Vorticity(u12_gaussian[:,13:56,18:], v12_gaussian[:,13:56,18:])

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.suptitle("Middle frame - without stopping vortex 50/100")
ax16.plot(time, sumVorticity0, label = "0 RPM")
ax16.plot(time, sumVorticity3, label = "3 RPM")
ax16.plot(time, sumVorticity6, label = "6 RPM")
ax16.plot(time, sumVorticity9, label = "9 RPM")
ax16.plot(time, sumVorticity12, label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of vorticity")
plt.legend()

sumEnstrophy0 = oj.sum_Enstrophy(u0_gaussian[:,:,18:], v0_gaussian[:,:,18:])
sumEnstrophy3 = oj.sum_Enstrophy(u3_gaussian[:,:,18:], v3_gaussian[:,:,18:])
sumEnstrophy6 = oj.sum_Enstrophy(u6_gaussian[:,:,18:], v6_gaussian[:,:,18:])
sumEnstrophy9 = oj.sum_Enstrophy(u9_gaussian[:,:,18:], v9_gaussian[:,:,18:])
sumEnstrophy12 = oj.sum_Enstrophy(u12_gaussian[:,:,18:], v12_gaussian[:,:,18:])

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.suptitle("Enstrophy Middle Frame - without stopping vortex 50/100")
ax16.plot(time, sumEnstrophy0, label = "0 RPM")
ax16.plot(time, sumEnstrophy3, label = "3 RPM")
ax16.plot(time, sumEnstrophy6, label = "6 RPM")
ax16.plot(time, sumEnstrophy9, label = "9 RPM")
ax16.plot(time, sumEnstrophy12, label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of enstrophy")
plt.legend()



u0, v0 = oj.importData73("F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/4/Data/PIV_export.mat")
u3, v3 = oj.importData73("F:/Testing/RPM-3.0__Upiston-50__Stroke-50/2023-05-23__FPS-90/4/Data/PIV_export.mat")
# u6, v6 = oj.importData73("F:/Testing/RPM-6.0__Upiston-50__Stroke-50/2023-05-23__FPS-90/4/Data/PIV_export.mat") # OLD
u6, v6 = oj.importData73("F:/Testing/RPM-6.0__Upiston-50__Stroke-50/2023-06-07__FPS-90/4/Data/PIV_export.mat") # NEW
u9, v9 = oj.importData73("F:/Testing/RPM-9.0__Upiston-50__Stroke-50/2023-05-24__FPS-90/4/Data/PIV_export.mat")
u12, v12 = oj.importData73("F:/Testing/RPM-12.0__Upiston-50__Stroke-50/2023-05-19__FPS-90/4/Data/PIV_export.mat")

u0_gaussian, v0_gaussian = gaussian_filter(u0, sigma=0.7), gaussian_filter(v0, sigma=0.7)
u3_gaussian, v3_gaussian = gaussian_filter(u3, sigma=0.7), gaussian_filter(v3, sigma=0.7)
u6_gaussian, v6_gaussian = gaussian_filter(u6, sigma=0.7), gaussian_filter(v6, sigma=0.7)
u9_gaussian, v9_gaussian = gaussian_filter(u9, sigma=0.7), gaussian_filter(v9, sigma=0.7)
u12_gaussian, v12_gaussian = gaussian_filter(u12, sigma=0.7), gaussian_filter(v12, sigma=0.7)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u0.shape[1], u0.shape[2])


f9, (ax12, ax13) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
ax12.quiver(z_nd, r_nd, u3_gaussian[200,:,:], v3_gaussian[200,:,:], pivot="middle")
ax12.set_xlabel('Z')
ax12.set_ylabel('R')
ax13.contourf(z_nd, r_nd, u3_gaussian[200,:,:])
# plt.show()

f10, ax14 = plt.subplots()
ax14.contourf(z_nd, r_nd, u3_gaussian[200,:,:])
ax14.quiver(z_nd, r_nd, u3_gaussian[200,:,:], v3_gaussian[200,:,:], pivot="middle")
ax14.set_xlabel('Z')
ax14.set_ylabel('R')
# plt.show()

f11, ax15 = plt.subplots()
ax15.contourf(z_nd, r_nd, u9_gaussian[200,:,:])
ax15.quiver(z_nd, r_nd, u9_gaussian[200,:,:], v9_gaussian[200,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
ax15.set_xlabel('Z')
ax15.set_ylabel('R')
# plt.show()





x = np.linspace(0 , u0_gaussian.shape[2], u0_gaussian.shape[2])
y = np.linspace(0 , u0_gaussian.shape[0], u0_gaussian.shape[0])
X, Y = np.meshgrid(x, y)

Z1 = u0_gaussian[:, int(u0_gaussian.shape[1]/2), :]
Z2 = u3_gaussian[:, int(u0_gaussian.shape[1]/2), :]
Z3 = u6_gaussian[:, int(u0_gaussian.shape[1]/2), :]
Z4 = u9_gaussian[:, int(u0_gaussian.shape[1]/2), :]
vmin = min(np.min(u0_gaussian), np.min(u3_gaussian), np.min(u6_gaussian), np.min(u9_gaussian))
vmax = max(np.max(u0_gaussian), np.max(u3_gaussian), np.max(u6_gaussian), np.max(u9_gaussian))
norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)


# frame = 400
fig, axs = plt.subplots(2, 2, sharex= True, sharey=True)
axs[0, 0].contourf(z_nd, r_nd, u0_gaussian[frame,:,:], norm=norm, cmap='bwr')
axs[0, 0].quiver(z_nd, r_nd, u0_gaussian[frame,:,:], v0_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[0, 0].set_title('0RPM')
axs[0, 0].set_xlabel("z/D")
axs[0, 0].set_ylabel("r/D")
axs[0, 1].contourf(z_nd, r_nd, u3_gaussian[frame,:,:], norm=norm, cmap='bwr')
axs[0, 1].quiver(z_nd, r_nd, u3_gaussian[frame,:,:], v3_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[0, 1].set_title('3RPM')
axs[0, 1].set_xlabel("z/D")
axs[0, 1].set_ylabel("r/D")
axs[1, 0].contourf(z_nd, r_nd, u6_gaussian[frame,:,:], norm=norm, cmap='bwr')
axs[1, 0].quiver(z_nd, r_nd, u6_gaussian[frame,:,:], v6_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[1, 0].set_title('6RPM')
axs[1, 0].set_xlabel("z/D")
axs[1, 0].set_ylabel("r/D")
axs[1, 1].contourf(z_nd, r_nd, u9_gaussian[frame,:,:], norm=norm, cmap='bwr')
axs[1, 1].quiver(z_nd, r_nd, u9_gaussian[frame,:,:], v9_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[1, 1].set_title('9RPM')
axs[1, 1].set_xlabel("z/D")
axs[1, 1].set_ylabel("r/D")
fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap="bwr"), ax=axs)
fig.suptitle('Velocity at frame 200 (2.22s)')


x = np.linspace(0 , u0_gaussian.shape[2], u0_gaussian.shape[2])
y = np.linspace(0 , u0_gaussian.shape[0], u0_gaussian.shape[0])
X, Y = np.meshgrid(x, y)

Z1 = u0_gaussian[:, 35, :]
Z2 = u3_gaussian[:, 35, :]
Z3 = u6_gaussian[:, 35, :]
Z4 = u9_gaussian[:, 35, :]
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
# plt.show()







### Sum total vorticity in frame
time = oj.frames_to_seconds(u0, v0, 90)
sumVorticity0 = oj.sum_Vorticity(u0_gaussian[:,13:56,:], v0_gaussian[:,13:56,:])
sumVorticity3 = oj.sum_Vorticity(u3_gaussian[:,13:56,:], v3_gaussian[:,13:56,:])
sumVorticity6 = oj.sum_Vorticity(u6_gaussian[:,13:56,:], v6_gaussian[:,13:56,:])
sumVorticity9 = oj.sum_Vorticity(u9_gaussian[:,13:56,:], v9_gaussian[:,13:56,:])
sumVorticity12 = oj.sum_Vorticity(u12_gaussian[:,13:56,:], v12_gaussian[:,13:56,:])

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.suptitle("Middle frame - 50/50")
ax16.plot(time, sumVorticity0, label = "0 RPM")
ax16.plot(time, sumVorticity3, label = "3 RPM")
ax16.plot(time, sumVorticity6, label = "6 RPM")
ax16.plot(time, sumVorticity9, label = "9 RPM")
ax16.plot(time, sumVorticity12, label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of vorticity")
plt.legend()

sumVorticity0 = oj.sum_Vorticity(u0_gaussian[:,13:56,18:], v0_gaussian[:,13:56,18:])
sumVorticity3 = oj.sum_Vorticity(u3_gaussian[:,13:56,18:], v3_gaussian[:,13:56,18:])
sumVorticity6 = oj.sum_Vorticity(u6_gaussian[:,13:56,18:], v6_gaussian[:,13:56,18:])
sumVorticity9 = oj.sum_Vorticity(u9_gaussian[:,13:56,18:], v9_gaussian[:,13:56,18:])
sumVorticity12 = oj.sum_Vorticity(u12_gaussian[:,13:56,18:], v12_gaussian[:,13:56,18:])

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.suptitle("Middle frame vorticity - without stopping vortex 50/50")
ax16.plot(time, sumVorticity0, label = "0 RPM")
ax16.plot(time, sumVorticity3, label = "3 RPM")
ax16.plot(time, sumVorticity6, label = "6 RPM")
ax16.plot(time, sumVorticity9, label = "9 RPM")
ax16.plot(time, sumVorticity12, label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of vorticity")
plt.legend()
 


sumEnstrophy0 = oj.sum_Enstrophy(u0_gaussian[:,:,18:], v0_gaussian[:,:,18:])
sumEnstrophy3 = oj.sum_Enstrophy(u3_gaussian[:,:,18:], v3_gaussian[:,:,18:])
sumEnstrophy6 = oj.sum_Enstrophy(u6_gaussian[:,:,18:], v6_gaussian[:,:,18:])
sumEnstrophy9 = oj.sum_Enstrophy(u9_gaussian[:,:,18:], v9_gaussian[:,:,18:])
sumEnstrophy12 = oj.sum_Enstrophy(u12_gaussian[:,:,18:], v12_gaussian[:,:,18:])

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.suptitle("Enstrophy - without stopping vortex 50/50")
ax16.plot(time, sumEnstrophy0, label = "0 RPM")
ax16.plot(time, sumEnstrophy3, label = "3 RPM")
ax16.plot(time, sumEnstrophy6, label = "6 RPM")
ax16.plot(time, sumEnstrophy9, label = "9 RPM")
ax16.plot(time, sumEnstrophy12, label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of enstrophy")
plt.legend()

sumEnstrophy0 =  oj.sum_Enstrophy(u0_gaussian [:,13:56,18:], v0_gaussian [:,13:56,18:])
sumEnstrophy3 =  oj.sum_Enstrophy(u3_gaussian [:,13:56,18:], v3_gaussian [:,13:56,18:])
sumEnstrophy6 =  oj.sum_Enstrophy(u6_gaussian [:,13:56,18:], v6_gaussian [:,13:56,18:])
sumEnstrophy9 =  oj.sum_Enstrophy(u9_gaussian [:,13:56,18:], v9_gaussian [:,13:56,18:])
sumEnstrophy12 = oj.sum_Enstrophy(u12_gaussian[:,13:56,18:], v12_gaussian[:,13:56,18:])

f13, ax16 = plt.subplots(nrows=1, ncols=1)
plt.suptitle("Middle frame Enstrophy - without stopping vortex 50/50")
ax16.plot(time, sumEnstrophy0, label = "0 RPM")
ax16.plot(time, sumEnstrophy3, label = "3 RPM")
ax16.plot(time, sumEnstrophy6, label = "6 RPM")
ax16.plot(time, sumEnstrophy9, label = "9 RPM")
ax16.plot(time, sumEnstrophy12, label = "12 RPM")
ax16.set_xlabel("time [s]")
ax16.set_ylabel("sum of enstrophy")
plt.legend()

vort0 , vort0gauss = oj.calculate_vorticity(u0_gaussian, v0_gaussian)
vort3 , vort3gauss = oj.calculate_vorticity(u3_gaussian, v3_gaussian)
vort6 , vort6gauss = oj.calculate_vorticity(u6_gaussian, v6_gaussian)
vort9 , vort9gauss = oj.calculate_vorticity(u9_gaussian, v9_gaussian)
vort12, vort12gauss = oj.calculate_vorticity(u12_gaussian, v12_gaussian)

x = np.linspace(0 , u0_gaussian.shape[2], u0_gaussian.shape[2])
y = np.linspace(0 , u0_gaussian.shape[0], u0_gaussian.shape[0])
X, Y = np.meshgrid(x, y)

vmin = min(np.min(vort0), np.min(vort3), np.min(vort6), np.min(vort9))
vmax = max(np.max(vort0), np.max(vort3), np.max(vort6), np.max(vort9))
norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)



fig, axs = plt.subplots(2, 2, sharex= True, sharey=True)
axs[0, 0].contourf(z_nd, r_nd, vort0gauss[400,:,:], norm=norm, cmap='bwr')
# axs[0, 0].quiver(z_nd, r_nd, vort0[frame,:,:], v0_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[0, 0].set_title('0RPM')
axs[0, 0].set_xlabel("z/D")
axs[0, 0].set_ylabel("r/D")
axs[0, 1].contourf(z_nd, r_nd, vort3gauss[400,:,:], norm=norm, cmap='bwr')
# axs[0, 1].quiver(z_nd, r_nd, u3_gaussian[frame,:,:], v3_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[0, 1].set_title('3RPM')
axs[0, 1].set_xlabel("z/D")
axs[0, 1].set_ylabel("r/D")
axs[1, 0].contourf(z_nd, r_nd, vort6gauss[400,:,:], norm=norm, cmap='bwr')
# axs[1, 0].quiver(z_nd, r_nd, u6_gaussian[frame,:,:], v6_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[1, 0].set_title('6RPM')
axs[1, 0].set_xlabel("z/D")
axs[1, 0].set_ylabel("r/D")
axs[1, 1].contourf(z_nd, r_nd, vort9gauss[400,:,:], norm=norm, cmap='bwr')
# axs[1, 1].quiver(z_nd, r_nd, u9_gaussian[frame,:,:], v9_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[1, 1].set_title('9RPM')
axs[1, 1].set_xlabel("z/D")
axs[1, 1].set_ylabel("r/D")
fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap="bwr"), ax=axs)
fig.suptitle('Vorticity at frame 200 (2.22s)')
plt.show() 


f14, (ax17, ax18, ax19) = plt.subplots(nrows=3, ncols=1)
plt.suptitle("u0, vs u6 v u9 for piston speed")
ax17.imshow(u0[260,:,:])
ax18.imshow(u6[260,:,:])
ax19.imshow(u9[260,:,:])
# plt.show()

f14, (ax17, ax18, ax19) = plt.subplots(nrows=3, ncols=1)
plt.suptitle("u0, vs u6 v u9 for piston speed")
ax17.contourf(u0[260,:,:], cmap = "bwr")
f14.colorbar(matplotlib.cm.ScalarMappable(cmap="bwr"), ax=ax17)
ax18.contourf(u6[260,:,:], cmap = "bwr")
f14.colorbar(matplotlib.cm.ScalarMappable(cmap="bwr"), ax=ax18)
ax19.contourf(u9[260,:,:], cmap = "bwr")
f14.colorbar(matplotlib.cm.ScalarMappable(cmap="bwr"), ax=ax19)
plt.show()


# vfftu0 = oj.IWFilter(u, 30, 90, 6)
vfftu3 = oj.IWFilter(u3_gaussian, 30, 90, 3)
vfftu6 = oj.IWFilter(u6_gaussian, 30, 90, 6)
vfftu9 = oj.IWFilter(u9_gaussian, 30, 90, 9)
vfftu12 = oj.IWFilter(u12_gaussian, 30, 90, 12)

# vmin = min(np.min(vfftu3), np.min(vfftu6), np.min(vfftu9), np.min(vfftu12))
# vmax = max(np.max(vfftu3), np.max(vfftu6), np.max(vfftu9), np.max(vfftu12))
# norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

fig, axs = plt.subplots(2, 2, sharex= True, sharey=True)
axs[0, 0].contourf(vfftu3[200,:,:],  cmap='bwr')
# axs[0, 0].quiver(z_nd, r_nd, vort0[frame,:,:], v0_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[0, 0].set_title('3RPM')
axs[0, 0].set_xlabel("z/D")
axs[0, 0].set_ylabel("r/D")
axs[0, 1].contourf(vfftu6[200,:,:],  cmap='bwr')
# axs[0, 1].quiver(z_nd, r_nd, u3_gaussian[frame,:,:], v3_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[0, 1].set_title('6RPM')
axs[0, 1].set_xlabel("z/D")
axs[0, 1].set_ylabel("r/D")
axs[1, 0].contourf(vfftu9[200,:,:],  cmap='bwr')
# axs[1, 0].quiver(z_nd, r_nd, u6_gaussian[frame,:,:], v6_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[1, 0].set_title('9RPM')
axs[1, 0].set_xlabel("z/D")
axs[1, 0].set_ylabel("r/D")
axs[1, 1].contourf(vfftu12[200,:,:],  cmap='bwr')
# axs[1, 1].quiver(z_nd, r_nd, u9_gaussian[frame,:,:], v9_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[1, 1].set_title('12RPM')
axs[1, 1].set_xlabel("z/D")
axs[1, 1].set_ylabel("r/D")
# fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap="bwr"), ax=axs)
fig.suptitle('Vorticity at frame 200 (2.22s)')
plt.show() 

fig, axs = plt.subplots(2, 2, sharex= True, sharey=True)
axs[0, 0].contourf(vfftu3[400,:,:],  cmap='bwr')
# axs[0, 0].quiver(z_nd, r_nd, vort0[frame,:,:], v0_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[0, 0].set_title('3RPM')
axs[0, 0].set_xlabel("z/D")
axs[0, 0].set_ylabel("r/D")
axs[0, 1].contourf(vfftu6[400,:,:],  cmap='bwr')
# axs[0, 1].quiver(z_nd, r_nd, u3_gaussian[frame,:,:], v3_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[0, 1].set_title('6RPM')
axs[0, 1].set_xlabel("z/D")
axs[0, 1].set_ylabel("r/D")
axs[1, 0].contourf(vfftu9[400,:,:],  cmap='bwr')
# axs[1, 0].quiver(z_nd, r_nd, u6_gaussian[frame,:,:], v6_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[1, 0].set_title('9RPM')
axs[1, 0].set_xlabel("z/D")
axs[1, 0].set_ylabel("r/D")
axs[1, 1].contourf(vfftu12[400,:,:],  cmap='bwr')
# axs[1, 1].quiver(z_nd, r_nd, u9_gaussian[frame,:,:], v9_gaussian[frame,:,:], pivot="middle", scale = 100, headwidth = 1, headlength = 2)
axs[1, 1].set_title('12RPM')
axs[1, 1].set_xlabel("z/D")
axs[1, 1].set_ylabel("r/D")
# fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap="bwr"), ax=axs)
fig.suptitle('Vorticity at frame 400 (4.44s)')
plt.show() 