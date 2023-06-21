import numpy as np
import os
import sys
import mat73
import math as maths
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter


#####Import Ollie Tools
# dirPath = "C:/Coding/Code"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

#####Import Ollie Tools Temp
# dirPath = "C:/Coding/Code"
# sys.path.insert(0, dirPath)
# import OllieTools_Temp as ojT
# print(dirPath)

####Import Ollie Tools MAC
dirPath = "/Users/olliejackson/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

#####Import Ollie Tools Temp MAC
# dirPath = "/Users/olliejackson/Coding/Code"
# sys.path.insert(0, dirPath)
# import OllieTools_Temp as ojT
# print(dirPath)

##### Set plot style #####
# plt.style.use(["science", "vibrant", "no-latex"])
# cmap = plt.get_cmap("jet_r")

# u, v = oj.importData73("/Volumes/OllieSSD/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-08__FPS-60/3/Data/PIV_export.mat")
# u, v = oj.importData73("G:/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-08__FPS-60/3/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-0.0__Upiston-200__Stroke-50/2023-02-08__FPS-60/6/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-3.0__Upiston-200__Stroke-100/2023-03-14__FPS-60/1/Data/PIV_export.mat")
# u,  v = oj.importData73("G:/Testing/RPM-6.0__Upiston-200__Stroke-100/2023-03-15__FPS-60/1/Data/PIV_export.mat")
# u,  v = oj.importData73("F:/useful_data_copy_from_samsung/RPM-0.0__Upiston-200__Stroke-100/2023-02-08__FPS-60/3/PIV_export.mat")
# u,  v = oj.importData73("/Volumes/OllieSSD/Testing/RPM-0.0__Upiston-200__Stroke-100/2023-02-27__FPS-60/8/Data/PIV_export.mat")
u,  v = oj.importData73("/Volumes/OllieSSD/Testing/RPM-9.0__Upiston-200__Stroke-100/2023-03-16__FPS-60/5/Data/PIV_export.mat")

u_gaussian, v_gaussian = gaussian_filter(u, sigma=0.7), gaussian_filter(v, sigma=0.7)
vorticity, vorticity_gaussian = oj.calculate_vorticity(u, v)
VortLocMax, VortLocMin = oj.vorticityPeakTracking(u_gaussian, v_gaussian)

f1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
ax1.set_title("u")
ax1.contourf(u[500,:,:], cmap = "bwr")
ax2.set_title("v")
ax2.contourf(v[500,:,:], cmap = "bwr")
# plt.show()

f1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
ax1.set_title("u")
ax1.contourf(u_gaussian[500,:,:], cmap = "bwr")
ax2.set_title("Vorticity")
ax2.contourf(vorticity_gaussian[500,:,:], cmap = "bwr")
# plt.show()

f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.set_title("Vorticity")
ax1.contourf(vorticity_gaussian[500,:,:], cmap = "bwr")
# plt.show()

f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.set_title("Velocity")
ax1.contourf(u_gaussian[500,:,:], cmap = "bwr")
# plt.show()

# f2, ax2 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
# plt.title("VortLocMin")
# ax2.plot(VortLocMin[:,0], label = "index 0")
# ax2.plot(VortLocMin[:,1], label = "index 1")
# plt.legend()
# plt.show()

# f3, ax3 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
# plt.title("VortLocMax")
# ax3.plot(VortLocMax[:,0], label = "index 0")
# ax3.plot(VortLocMax[:,1], label = "index 1")
# plt.legend()
# plt.show()



# f4, ax4 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
# plt.title("vorticity, VortLocMax, VortLocMin")
# ax4.contourf(vorticity_gaussian[1000,:,:])
# ax4.scatter(VortLocMax[1000,1],VortLocMax[1000,0], label = "Max Vorticity", color = "k")
# ax4.scatter(VortLocMin[1000,1],VortLocMin[1000,0], label = "Min Vorticity", color = "w")
# plt.legend()
# plt.show()



#### Plotting the line between points ####

# f5,ax5 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
# plt.title("connectiong poits")
# x1, x2 = VortLocMax[1000,1], VortLocMin[1000,1]
# y1, y2 = VortLocMax[1000,0], VortLocMin[1000,0]
# ax5.scatter(VortLocMax[1000,1],VortLocMax[1000,0], label = "Max Vorticity")
# ax5.scatter(VortLocMin[1000,1],VortLocMin[1000,0], label = "Min Vorticity")
# plt.plot([x1,x2],[y1,y2], "--", color = "c")
# plt.show()



#### For Any Frame ####

frame = 500
x1, x2 = VortLocMax[frame,1], VortLocMin[frame,1]
y1, y2 = VortLocMax[frame,0], VortLocMin[frame,0]

# f6,ax6 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
# plt.title("Connectiong Points")
# ax6.contourf(vorticity_gaussian[frame,:,:])#, cmap = "seismic")
# ax6.scatter(VortLocMax[frame,1],VortLocMax[frame,0], label = "Max Vorticity", color = "k")
# ax6.scatter(VortLocMin[frame,1],VortLocMin[frame,0], label = "Min Vorticity", color = "w")
# plt.plot([x1,x2],[y1,y2], "--", linewidth=2.0)#, color = "c")
# plt.legend()
# plt.show()


#### Animating Vorticity Plots #####
# oj.animate_cube_contourf_points(vorticity_gaussian, VortLocMax_sav, VortLocMin, 17)

#### Putting vorticity local Min/Max through Savgol ####

VortLocMax_sav = np.zeros([VortLocMax.shape[0], VortLocMax.shape[1]])
VortLocMax_sav[:,1] = oj.FilterSpikes(VortLocMax[:,1], 50)
VortLocMax_sav[:,1] = savgol_filter(VortLocMax_sav[:,1], 51, 3)
VortLocMax_sav[:,0] = oj.FilterSpikes(VortLocMax[:,0], 50)
VortLocMax_sav[:,0] = savgol_filter(VortLocMax_sav[:,0], 51, 3)

VortLocMin_sav = np.zeros([VortLocMin.shape[0], VortLocMin.shape[1]])
VortLocMin_sav[:,1] = oj.FilterSpikes(VortLocMin[:,1], 5)
VortLocMin_sav[:,1] = savgol_filter(VortLocMin_sav[:,1], 51, 3)
VortLocMin_sav[:,0] = oj.FilterSpikes(VortLocMin[:,0], 5)
VortLocMin_sav[:,0] = savgol_filter(VortLocMin_sav[:,0], 51, 3)


f3, ax3 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
plt.title("VortLocMax")
ax3.plot(VortLocMax[:,0], label = "index 0")
ax3.plot(VortLocMax[:,1], label = "index 1")
ax3.plot(VortLocMax_sav[:,0], label = "index 0 Savgol")
ax3.plot(VortLocMax_sav[:,1], label = "index 1 Savgol")
plt.xlabel("Time (frames at 60FPS)")
plt.ylabel("x Position")
plt.legend()

f3, ax3 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
plt.title("VortLocMin")
ax3.plot(VortLocMin[:,0], label = "index 0")
ax3.plot(VortLocMin[:,1], label = "index 1")
ax3.plot(VortLocMin_sav[:,0], label = "index 0 Savgol")
ax3.plot(VortLocMin_sav[:,1], label = "index 1 Savgol")
plt.xlabel("Time (frames at 60FPS)")
plt.ylabel("x Position")
plt.legend()
# plt.show()

x1, x2 = VortLocMax_sav[frame,1], VortLocMin_sav[frame,1]
y1, y2 = VortLocMax_sav[frame,0], VortLocMin_sav[frame,0]

f6,ax6 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
plt.title("Connecting Points")
ax6.contourf(vorticity_gaussian[frame,:,:], cmap = "bwr")
ax6.scatter(VortLocMax_sav[frame,1],VortLocMax_sav[frame,0], label = "Max Vorticity", color = "k")
ax6.scatter(VortLocMin_sav[frame,1],VortLocMin_sav[frame,0], label = "Min Vorticity", color = "w")
plt.plot([x1,x2],[y1,y2], "--", linewidth=2.0)#, color = "c")
plt.legend()
# plt.show()

# oj.animate_cube_contourf_points(vorticity_gaussian, VortLocMax_sav, VortLocMin_sav, 17)


### Calculating line length ####

dx = VortLocMin_sav[:,1] - VortLocMax_sav[:,1]
# print("dx shape: " + str(dx.shape))
dy = VortLocMin_sav[:,0] - VortLocMax_sav[:,0]
# print("dy shape: " + str(dy.shape))

# f9, ax9 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
# plt.title("dx & dy")
# ax9.plot(dx, label = "dx")
# ax9.plot(dy, label = "dy")
# plt.legend
# plt.show()

ring_diameter = np.sqrt(abs(dx)**2 + abs(dy)**2)
f10, ax10 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
plt.title("diameter")
ax10.plot(ring_diameter, label = "Line Length")
plt.xlabel("Time (frames at 60FPS)")
plt.ylabel("x Position")
plt.legend
plt.show()
# plt.close('all')


### line length at a specific point
#vortlocmax and vortlocmin at a specific frame (coords) done
#dx and dy at that frame done
#line length at that frame
# plot the frame to see if that works in reality done
# frame 500 seems good

frame = 500
x1, x2 = VortLocMax_sav[frame,1], VortLocMin_sav[frame,1]
y1, y2 = VortLocMax_sav[frame,0], VortLocMin_sav[frame,0]

f11, ax11 = plt.subplots(nrows=1, ncols=1, sharex = True, sharey = True)
plt.title("frame 500 vorticity")
ax11.contourf(vorticity_gaussian[frame,:,:], cmap = "bwr")
ax11.scatter(VortLocMax_sav[frame,1],VortLocMax_sav[frame,0], label = "Max Vorticity", color = "k")
ax11.scatter(VortLocMin_sav[frame,1],VortLocMin_sav[frame,0], label = "Min Vorticity", color = "w")
plt.plot([x1,x2],[y1,y2], "--", linewidth=2.0)#, color = "c")
plt.legend()
# plt.show()

print("y coordinates: max, min")
print(VortLocMax_sav[frame, 0], VortLocMin_sav[frame, 0])
print("x coordinates: max, min")
print(VortLocMax_sav[frame, 1], VortLocMin_sav[frame, 1])

print("dx, dx abs, dx**2: " + str(dx[frame]) + ", " + str(abs(dx[frame])) + ", " + str(abs(dx[frame])**2))
print("dy, dy abs, dy**2: " + str(dy[frame]) + ", " + str(abs(dy[frame])) + ", " + str(abs(dy[frame])**2))

print(f"line length at frame {frame}")
print(ring_diameter[frame])
# plt.show()