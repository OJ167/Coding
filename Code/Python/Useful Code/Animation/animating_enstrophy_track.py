import numpy as np
import os
import sys
import mat73
import math as maths
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import h5py

#####Import Ollie Tools
# dirPath = "C:/Coding/Code"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

#####Import Ollie Tools Temp
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding/Code"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

##### Set plot style #####
# plt.style.use(["science", "vibrant", "no-latex"])
# cmap = plt.get_cmap("jet_r")

Rotations = ['RPM0', 'RPM1', 'RPM2', 'RPM3', 'RPM6', 'RPM9', 'RPM12']
Injection = ['U50', 'U100']
Stroke = ['L50', 'L100']
I = 'U100'
S = 'L50'
R = 'RPM9'
frame = 1500

h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(R)]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
time = oj.frames_to_seconds(u, v, 90)

vorticity, vorticity_gaussian = oj.calculate_vorticity(u, v)
EnstLocMax = oj.enstrophyPeakTracking_inter(u, v)


f1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
ax1.set_title("u")
ax1.contourf(u[500,:,:], cmap = "seismic")
ax2.set_title("v")
ax2.contourf(v[500,:,:], cmap = "seismic")
# plt.show()

f2, ax3 = plt.subplots(nrows=1, ncols=1)
ax3.set_title("u")
ax3.contourf(u[frame,:,:], cmap = "seismic")
ax3.vlines(EnstLocMax[frame,1], ymin = 0, ymax = (u.shape[1]-1), colors='g', linestyles='dashed')


f3,ax4 = plt.subplots(nrows=1, ncols=1)
ax4.plot(EnstLocMax[:,1])
plt.show()


#### Animating Vorticity Plots #####
oj.animate_cube_contourf_line(vorticity_gaussian[:1150,:,:], EnstLocMax[:1150,:], 11, save=0, fps=90)
oj.animate_cube_contourf_line(u[:1150,:,:], EnstLocMax[:1150,:], 11, save=0, fps=90)


# oj.animate_cube_contourf_points(vorticity_gaussian, VortLocMax_sav, VortLocMin_sav, 17)


# time = oj.frames_to_seconds(u_mean, u_mean, 150)
# oj.animate_cube_quiver(u_mean, v_mean, U_az, interval=6.67, cmap="seismic", save=0, output="new.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "new.mp4", fps=150, scale = 1, fsize = (19, 12))
# print("0RPM Done")





# vels = h5file['3D0']['U100']['L100']['RPM1']
# u = vels[:,:,:,0]
# v = vels[:,:,:,1]
# U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
# U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
# X, Y = np.meshgrid(x, y) 
# for i in range(u.shape[0]):
#     r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])


# time = oj.frames_to_seconds(u, v, 150)
# oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="1_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "1_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
# print("1RPM Done")

# vels = h5file['3D0']['U100']['L100']['RPM2']
# u = vels[:,:,:,0]
# v = vels[:,:,:,1]
# U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
# U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
# X, Y = np.meshgrid(x, y) 
# for i in range(u.shape[0]):
#     r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])


# time = oj.frames_to_seconds(u, v, 150)
# oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="2_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "2_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
# print("2RPM Done")




# vels = h5file['3D0']['U100']['L100']['RPM3']
# u = vels[:,:,:,0]
# v = vels[:,:,:,1]
# U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
# U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
# X, Y = np.meshgrid(x, y) 
# for i in range(u.shape[0]):
#     r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])

    
# time = oj.frames_to_seconds(u, v, 150)
# oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="3_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "3_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
# print("3RPM Done")



# vels = h5file['3D0']['U100']['L100']['RPM6']
# u = vels[:,:,:,0]
# v = vels[:,:,:,1]
# U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
# U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
# X, Y = np.meshgrid(x, y) 
# for i in range(u.shape[0]):
#     r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])

    
# time = oj.frames_to_seconds(u, v, 150)
# oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="6_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "6_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
# print("6RPM Done")



# vels = h5file['3D0']['U100']['L100']['RPM9']
# u = vels[:,:,:,0]
# v = vels[:,:,:,1]
# U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
# U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
# X, Y = np.meshgrid(x, y) 
# for i in range(u.shape[0]):
#     r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])

    
# time = oj.frames_to_seconds(u, v, 150)
# oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="9_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "9_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
# print("9RPM Done")




# vels = h5file['3D0']['U100']['L100']['RPM12']
# u = vels[:,:,:,0]
# v = vels[:,:,:,1]
# U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
# U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
# X, Y = np.meshgrid(x, y) 
# for i in range(u.shape[0]):
#     r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])

    
# time = oj.frames_to_seconds(u, v, 150)
# oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="12_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "12_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
# print("12RPM Done")