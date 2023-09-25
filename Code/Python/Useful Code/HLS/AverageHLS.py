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
import h5py
from matplotlib import animation
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




h5file = h5py.File('F:/H5/3D0meandataHLS.h5', 'r')

vels = h5file['3D0']['U100']['L100']['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)

Vmean = np.sqrt(np.square(umean) + np.square(vmean))


time = oj.frames_to_seconds(u, v, 60)


f1, ax1 = plt.subplots()
ax1.contourf(Vmean[:,:], cmap = "seismic")
f1.colorbar(matplotlib.cm.ScalarMappable(cmap="bwr"), ax=ax1)
# plt.show()


f2, ax = plt.subplots(2, 2, sharex=True, sharey=True)
ax[0,0].quiver(u[800,:,:],  v[800,:,:])
ax[0,1].quiver(u[1000,:,:], v[1000,:,:])
ax[1,0].quiver(u[1200,:,:], v[1200,:,:])
ax[1,1].quiver(u[1400,:,:], v[1800,:,:])
ax[0,0].set_title("Frame 800")
ax[0,1].set_title("Frame 1000")
ax[1,0].set_title("Frame 1200")
ax[1,1].set_title("Frame 1400")
plt.legend()
# plt.show()


print(umean.shape)
print(vmean.shape)
x = 55
y = 35
x = np.linspace(0 , umean.shape[1], umean.shape[1])
y = np.linspace(0 , umean.shape[0], umean.shape[0])
X, Y = np.meshgrid(x, y) 
r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(55, 35, x, y, umean, vmean)

print(r.shape)
print(theta.shape)

# f2, ax = plt.subplots(2, 2, sharex=True, sharey=True)
# ax[0,0].quiver(U_r[:,:], U_az[:,:])
# ax[0,1].quiver(U_r[:,:], U_az[:,:])
# ax[1,0].quiver(U_r[:,:], U_az[:,:])
# ax[1,1].quiver(U_r[:,:], U_az[:,:])
# ax[0,0].set_title("Frame 800")
# ax[0,1].set_title("Frame 1000")
# ax[1,0].set_title("Frame 1200")
# ax[1,1].set_title("Frame 1400")
# plt.legend()
# plt.show()


# f3, ax3 = plt.subplots()
# ax3.quiver(r, r, U_az[:,:],  )
# plt.show()

# f4, ax4 = plt.subplots()
# ax4.quiver(r[:,:])
# plt.show()

# f5, ax5 = plt.subplots()
# ax4.quiver(theta[:,:])
# plt.show()



def create_Mean(
        n, Dir
):
    ######## Importing multiple rings #####
    # n = 20
    u, v = oj.importData73(str(Dir) + "1/Data/PIV_export.mat")
    print(str(Dir), "\r")
    u = np.zeros([n, u.shape[0], u.shape[1], u.shape[2]])
    v = np.zeros([n, v.shape[0], v.shape[1], v.shape[2]])

    for i in range(1, n+1):
        u[(i-1),:,:,:], v[(i-1),:,:,:] = oj.importData73(str(Dir) + str(i) + "/Data/PIV_export.mat")
        oj.progressBar(i, n)

    u_mean = np.mean(u[1:], 0)
    v_mean = np.mean(v[1:], 0)
    u_mean, v_mean = gaussian_filter(u_mean, sigma=0.7), gaussian_filter(v_mean, sigma=0.7)

    return u_mean, v_mean, u, v

u_mean20, v_mean20, u, v = create_Mean(19, "F:/Testing/3Do/RPM-0.0__Upiston-100__Stroke-100/2023-09-21__FPS-150/")

f1, ax = plt.subplots(2, 2, sharex=True, sharey=True)
plt.suptitle("20 ring mean")
ax[0,0].quiver(u_mean20[800,:,:],  v_mean20[800,:,:])
ax[0,1].quiver(u_mean20[1000,:,:], v_mean20[1000,:,:])
ax[1,0].quiver(u_mean20[1200,:,:], v_mean20[1200,:,:])
ax[1,1].quiver(u_mean20[1400,:,:], v_mean20[1800,:,:])
ax[0,0].set_title("Frame 800")
ax[0,1].set_title("Frame 1000")
ax[1,0].set_title("Frame 1200")
ax[1,1].set_title("Frame 1400")
plt.legend()
# plt.show()


u_mean10 = np.mean(u[1:10], 0)
v_mean10 = np.mean(v[1:10], 0)

f2, ax = plt.subplots(2, 2, sharex=True, sharey=True)
plt.suptitle("first 10 ring mean")
ax[0,0].quiver(u_mean10[800,:,:],  v_mean10[800,:,:])
ax[0,1].quiver(u_mean10[1000,:,:], v_mean10[1000,:,:])
ax[1,0].quiver(u_mean10[1200,:,:], v_mean10[1200,:,:])
ax[1,1].quiver(u_mean10[1400,:,:], v_mean10[1800,:,:])
ax[0,0].set_title("Frame 800")
ax[0,1].set_title("Frame 1000")
ax[1,0].set_title("Frame 1200")
ax[1,1].set_title("Frame 1400")


u_mean1120 = np.mean(u[11:], 0)
v_mean1120 = np.mean(v[11:], 0)
f3, ax = plt.subplots(2, 2, sharex=True, sharey=True)
plt.suptitle("second 10 ring mean")
ax[0,0].quiver(u_mean1120[800,:,:],  v_mean1120[800,:,:])
ax[0,1].quiver(u_mean1120[1000,:,:], v_mean1120[1000,:,:])
ax[1,0].quiver(u_mean1120[1200,:,:], v_mean1120[1200,:,:])
ax[1,1].quiver(u_mean1120[1400,:,:], v_mean1120[1800,:,:])
ax[0,0].set_title("Frame 800")
ax[0,1].set_title("Frame 1000")
ax[1,0].set_title("Frame 1200")
ax[1,1].set_title("Frame 1400")
plt.show()

f3, ax = plt.subplots(2, 2, sharex=True, sharey=True)
plt.suptitle("second 10 ring mean")
ax[0,0].quiver(u[10,800,:,:],  v[10,800,:,:])
ax[0,1].quiver(u[10,1000,:,:], v[10,1000,:,:])
ax[1,0].quiver(u[11,800,:,:],  v[11,800,:,:])
ax[1,1].quiver(u[11,1000,:,:], v[11,1000,:,:])
ax[0,0].set_title("Ring 10, Frame 800")
ax[0,1].set_title("Ring 10, Frame 1000")
ax[1,0].set_title("Ring 11, Frame 800")
ax[1,1].set_title("Ring 11, Frame 1000")
plt.show()