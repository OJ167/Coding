import numpy as np
import os
import sys
import mat73
from scipy.interpolate import make_interp_spline, BSpline
from scipy import io
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import pandas as pd
import matplotlib.colors as colors
import matplotlib.cm
import matplotlib as mpl
import h5py
from matplotlib import animation
# from colorspacious import cspace_converter

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
# plt.style.reload_library()
# plt.style.use(["science", "vibrant", "no-latex"])

####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

def sum_Velocity(u, v):
    V = np.sqrt((abs(u))**2 + (abs(v))**2)
    sum_Velocity = np.sum(V, axis=(1,2))
    # print(sum_kinetic_energy.shape)
    return sum_Velocity


def sum_VelocityR(U_r, U_az):
    sum_Velocity_Radial    = np.sum(abs(U_r), axis=(1,2))
    sum_Velocity_Azimuthal = np.sum(abs(U_az), axis=(1,2))
    return sum_Velocity_Radial, sum_Velocity_Azimuthal


# h5file = h5py.File('F:/H5/3D0meandataHLS.h5', 'r')
h5file = h5py.File('E:/H5/3D0HLSFine.h5', 'r')

RPM = ['0', '1', '2', '3', '6', '9', '12']

# vels = h5file['3D0']['U100']['L100']['RPM' + str(RPM[6])]
vels = h5file['3D0']['U100']['L100']['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]


# for i in range(len(RPM[:])):
#     Revs = 'RPM' + str(RPM[i])
#     vels = h5file['3D0']['U100']['L100']['RPM' + str(RPM[1])]
#     u = vels[:,:,:,0]
#     v = vels[:,:,:,1]

V = np.sqrt(np.square(u) + np.square(v))
sV = sum_Velocity(u, v)
Ek, sEk = oj.sum_kinetic_energy(u, v)



time = oj.frames_to_seconds(u, v, 150)

f1, ax1 = plt.subplots()
ax1.plot(time, sEk)
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("$\Sigma$ Ek")

frame = 800


x = 55
y = 35
x = np.linspace(0 , u.shape[2], u.shape[2])
y = np.linspace(0 , u.shape[1], u.shape[1])
X, Y = np.meshgrid(x, y) 

r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[frame,:,:], v[frame,:,:])


f2, ax2 = plt.subplots()
cbar = ax2.contourf(U_az, cmap = "seismic")
f2.colorbar(cbar, ax=ax2)
# plt.show()



f3, ax3 = plt.subplots()
ax3.quiver(x, y, U_r, U_az)


U_r  = np.zeros([u.shape[0], u.shape[1], u.shape[2]]) 
U_az = np.zeros([u.shape[0], u.shape[1], u.shape[2]])
for i in range(u.shape[0]):
    r, theta, U_r[i,:,:], U_az[i,:,:], x0, y0 = oj.ConvertCylindrical(55, 35, x, y, u[i,:,:], v[i,:,:])


f2, ax2 = plt.subplots()
ax2.quiver(x, y, U_r[frame,:,:], U_az[frame,:,:])
plt.title("i quiver")
# plt.show()

sU_r, sU_az = sum_VelocityR(u, v)
print(sU_az[:])


f4, ax4 = plt.subplots()
ax4.plot(time, sV   , label = "sV"   )
ax4.plot(time, sU_r , label = "sU_r" )
ax4.plot(time, sU_az, label = "sU_az")
ax4.set_xlabel("Time [s]")
ax4.set_ylabel("$\Sigma$ V")
plt.legend()
plt.show()


# from matplotlib import cm
# from mpl_toolkits.mplot3d import axes3d

# f5, ax5 = plt.subplots(subplot_kw={"projection": "3d"})
# X, Y, U_az[1900,:,:] = axes3d.get_test_data(0.05)
# # surf = cm.axes3d(X, Y, U_az[1900,:,:], cmap="bwr", linewidth=0, antialiased=False)
# ax5.contour(X, Y, U_az[1900,:,:], cmap=cm.coolwarm)
# f5.colorbar(cbar, ax=ax5)