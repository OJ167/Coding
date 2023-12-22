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




# h5file = h5py.File('F:/H5/3D0meandataHLS.h5', 'r')
h5file = h5py.File('F:/H5/3D0HLSFine.h5', 'r')
vels = h5file['3D0']['U100']['L50']['RPM0']
u_mean = vels[:,:,:,0]
v_mean = vels[:,:,:,1]



# uold,  vold = oj.importData73("G:/Testing/3Do/RPM-3.0__Upiston-100__Stroke-100/2023-09-18__FPS-150/2/Data/PIV_export.mat")
# uold,  vold = gaussian_filter(uold, sigma=0.7), gaussian_filter(vold, sigma=0.7)
# r_ndold, z_ndold = oj.NDUnitsForPlotsWide(uold.shape[1], uold.shape[2])


# unew,  vnew = oj.importData73("G:/Testing/3Do/Repeat test/3RPM_100_100_Ring_2/Data/PIV_export.mat")
# unew,  vnew = gaussian_filter(unew, sigma=5), gaussian_filter(vnew, sigma=5)
# r_ndnew, z_ndnew = oj.NDUnitsForPlotsWide(unew.shape[1], unew.shape[2])


# unewavg = np.mean(uold, axis=0)
# vnewavg = np.mean(vold, axis=0)
# xNEW, yNEW, vort, gaus = oj.find_vortex_center_Vorticity(unewavg, vnewavg)
# # x = unew.shape[2]/2
# # y = unew.shape[1]/2
# x = np.linspace(0 , uold.shape[2], uold.shape[2])
# y = np.linspace(0 , uold.shape[1], uold.shape[1])
# r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(55, 35, x, y, uold[720,:,:], vold[720,:,:])


# f2, ax2 = plt.subplots()
# cbar = ax2.contourf(U_az, cmap = "seismic")
# f2.colorbar(cbar, ax=ax2)

# U_r  = np.zeros([uold.shape[0], uold.shape[1], uold.shape[2]]) 
# U_az = np.zeros([uold.shape[0], uold.shape[1], uold.shape[2]])
# X, Y = np.meshgrid(x, y) 
# for i in range(uold.shape[0]):
#     r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, uold[i,:,:], vold[i,:,:])


# f2, ax2 = plt.subplots()
# cbar = ax2.contourf(U_az[1900,:,:], cmap = "seismic")
# f2.colorbar(cbar, ax=ax2)

# f3, ax = plt.subplots(2, 2, sharex = True, sharey=True)
# plt.suptitle("second 10 ring mean")
# ax[0,0].plot(U_az[800 ,:,122])
# ax[0,1].plot(U_az[1000,:,122])
# ax[1,0].plot(U_az[1200,:,122])
# ax[1,1].plot(U_az[1800,:,122])
# ax[0,0].set_title("Frame 800")
# ax[0,1].set_title("Frame 1000")
# ax[1,0].set_title("Frame 1200")
# ax[1,1].set_title("Frame 1400")



# fig, ax = plt.subplots(2, 2, sharex=True, sharey=True)
# ax[0,0].plot(unew[720 ,int(yNEW),:], c = "b") # u deviation in x
# # ax[0,1].plot(unew[720 ,:,int(unew.shape[2]/2)], c = "b") # u deviation in y
# ax[0,1].plot(unew[720 ,:,int(xNEW)], c = "b") # u deviation in y
# ax[1,0].plot(vnew[720 ,int(yNEW),:], c = "b") # v deviation in x
# ax[1,1].plot(vnew[720 ,:,int(xNEW)], c = "b") # v deviation in y
# ax[0,0].set_title("u deviation in x")
# ax[0,1].set_title("u deviation in y")
# ax[1,0].set_title("v deviation in x")
# ax[1,1].set_title("v deviation in y")
# plt.legend()
# plt.show()


def create_Mean(
        n, Dir
):
    ######## Importing multiple rings #####
    # n = 20
    u, v = oj.importData73(str(Dir) + "1/Data/PIV_export_fine.mat")
    print(str(Dir), "\r")
    u = np.zeros([n, u.shape[0], u.shape[1], u.shape[2]])
    v = np.zeros([n, v.shape[0], v.shape[1], v.shape[2]])

    for i in range(1, n+1):
        u[(i-1),:,:,:], v[(i-1),:,:,:] = oj.importData73(str(Dir) + str(i) + "/Data/PIV_export_fine.mat")
        oj.progressBar(i, n)

    u_mean = np.mean(u[1:], 0)
    v_mean = np.mean(v[1:], 0)
    u_mean, v_mean = gaussian_filter(u_mean, sigma=1.4), gaussian_filter(v_mean, sigma=1.4)

    return u_mean, v_mean, u, v

# u_mean, v_mean, u, v = create_Mean(10, "F:/Testing/3Do/RPM-3.0__Upiston-100__Stroke-100/2023-09-18__FPS-150/")

# x = u_mean.shape[2]/2
# y = u_mean.shape[1]/2
x = np.linspace(0 , u_mean.shape[2], u_mean.shape[2])
y = np.linspace(0 , u_mean.shape[1], u_mean.shape[1])
U_r  = np.zeros([u_mean.shape[0], u_mean.shape[1], u_mean.shape[2]]) 
U_az = np.zeros([u_mean.shape[0], u_mean.shape[1], u_mean.shape[2]])
X, Y = np.meshgrid(x, y) 

for i in range(u_mean.shape[0]):
    r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(120, 73, x, y, u_mean[i,:,:], v_mean[i,:,:])

time = oj.frames_to_seconds(u_mean, u_mean, 150)
oj.animate_cube_quiver(u_mean, v_mean, U_az, interval=6.67, cmap="seismic", save=0, output="new.mp4", Dir = "C:/Users/u2088308/Videos/3D0_100_100/", name = "new.mp4", fps=150, scale = 1, fsize = (19, 12))
print("0RPM Done")





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