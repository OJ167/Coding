import numpy as np
import os
import sys
import h5py
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import pandas as pd
import matplotlib.colors as colors
import matplotlib.cm
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
cmap = plt.get_cmap("jet_r")




h5file = h5py.File('F:/H5/3D0meandataHLS.h5', 'r')

vels = h5file['3D0']['U100']['L100']['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]




x = 55
y = 35
x = np.linspace(0 , u.shape[2], u.shape[2])
y = np.linspace(0 , u.shape[1], u.shape[1])
r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[1900,:,:], v[1900,:,:])


f2, ax2 = plt.subplots()
cbar = ax2.contourf(U_az, cmap = "seismic")
f2.colorbar(cbar, ax=ax2)

U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
X, Y = np.meshgrid(x, y) 
for i in range(u.shape[0]):
    r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])


f2, ax2 = plt.subplots()
cbar = ax2.contourf(U_az[1900,:,:], cmap = "seismic")
f2.colorbar(cbar, ax=ax2)
plt.show()

time = oj.frames_to_seconds(u, v, 150)
oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="1_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "0_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
print("0RPM Done")





vels = h5file['3D0']['U100']['L100']['RPM1']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
X, Y = np.meshgrid(x, y) 
for i in range(u.shape[0]):
    r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])


time = oj.frames_to_seconds(u, v, 150)
oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="1_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "1_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
print("1RPM Done")

vels = h5file['3D0']['U100']['L100']['RPM2']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
X, Y = np.meshgrid(x, y) 
for i in range(u.shape[0]):
    r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])


time = oj.frames_to_seconds(u, v, 150)
oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="2_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "2_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
print("2RPM Done")




vels = h5file['3D0']['U100']['L100']['RPM3']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
X, Y = np.meshgrid(x, y) 
for i in range(u.shape[0]):
    r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])

    
time = oj.frames_to_seconds(u, v, 150)
oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="3_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "3_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
print("3RPM Done")



vels = h5file['3D0']['U100']['L100']['RPM6']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
X, Y = np.meshgrid(x, y) 
for i in range(u.shape[0]):
    r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])

    
time = oj.frames_to_seconds(u, v, 150)
oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="6_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "6_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
print("6RPM Done")



vels = h5file['3D0']['U100']['L100']['RPM9']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
X, Y = np.meshgrid(x, y) 
for i in range(u.shape[0]):
    r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])

    
time = oj.frames_to_seconds(u, v, 150)
oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="9_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "9_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
print("9RPM Done")




vels = h5file['3D0']['U100']['L100']['RPM12']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
X, Y = np.meshgrid(x, y) 
for i in range(u.shape[0]):
    r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])

    
time = oj.frames_to_seconds(u, v, 150)
oj.animate_cube_quiver(u, v, U_az, interval=6.67, cmap="seismic", save=1, output="12_100_100_mean.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "12_100_100_mean.mp4", fps=150, scale = 1, fsize = (19, 12))
print("12RPM Done")