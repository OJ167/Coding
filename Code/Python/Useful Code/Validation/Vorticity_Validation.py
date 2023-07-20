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


# 1. create trivial flow field
    # 1.1. solve it analytically
# 2. show it is continuous
# 3. show that it is rotational
# 4. circulation by area integral of vorticity
    # 4.1. use existing code and recode to see if there is similarity
# 5. circulation by line integral of velocity


####
# Trivial velocity field
# u = ky, v = 0
####


#### Simple Vortex
vf_x = lambda x, y: y
vf_y = lambda x, y: -x
# Stream function = 1/2y^2+1/2x^2




# vf_x = lambda x, y: 4 * y
# vf_y = lambda x, y: -x
# Stream function = (2*Y**2)+(0.5*X**2))


x_lim = (0, 100)
y_lim = (0, 100)
step = 1
scale = 100
X, Y = np.meshgrid(np.arange(x_lim[0], x_lim[1], step), np.arange(y_lim[0], y_lim[1], step))
U = np.zeros(X.shape)
V = np.zeros(Y.shape)
xmod = np.sign(X)
ymod = np.sign(Y)

for i in range(X.shape[0]):
    for j in range(Y.shape[0]):
          U[i,j] = vf_x(X[i, j], Y[i, j])
          V[i,j] = vf_y(X[i, j], Y[i, j])
          
fig, ax = plt.subplots(sharex=True, sharey=True)
ax.quiver(X, Y, U, V, units='xy', pivot = 'middle', scale=scale)
ax.contour((0.5*(Y**2))+(0.5*(X**2)))

# plt.show()


def calculate_vorticity(u, v):
    """
    calculates vorticity of velocity field
     
    INPUT:
        u           : 2D Numpy tensor containing velocity data
        v           : 2D Numpy tensor containing velocity data

    OUTPUT:
        Vorticity   : 2D Numpy tensor containing velocity data

    """
    dv = np.gradient(v, axis = 1)
    du = np.gradient(u, axis = 0)
    vorticity = dv - du
    return vorticity

def calculate_continuity(u, v):
    """
    calculates continuity of a 2D velocity field
     
    INPUT:
        u           : 2D Numpy tensor containing velocity data
        v           : 2D Numpy tensor containing velocity data

    OUTPUT:
        continuity   : 2D Numpy tensor containing continuity data

    """
    du = np.gradient(u, axis = 1)
    # print(du)
    dv = np.gradient(v, axis = 0)
    # print(dv)
    continuity = dv + du
    return continuity

def sum_Vorticity(
    u, v
):
    vorticity = calculate_vorticity(u, v)
    sumVorticity = np.zeros((u.shape[0]))
    sumVorticity = np.sum(abs(vorticity[:, :]))
    return sumVorticity

vort = calculate_vorticity(U, V)
cont = calculate_continuity(U, V)
# print(cont)
sum_vort = sum_Vorticity(U, V)
sum_vort2575 = sum_Vorticity(U[25:75], V[25:75])

def path_integral_velocity(
        u, v
):
    Vel = np.sqrt(np.square(U)+np.square(V))

    point_a = [25, 25]
    point_b = [25, 75]
    point_c = [75, 75]
    point_d = [75, 25]

    # path1 = #(25,25) - (75,25) in x
    # path2 = #(75,25) - (75,75) in y
    # path3 = #(75,75) - (25,75) in -x
    # path4 = #(25,75) - (25,25) in -y

    sumpath1 = sum(abs(Vel[24, 24:76]))
    sumpath2 = sum(abs(Vel[24:76, 76]))
    sumpath3 = sum(abs(Vel[76, 76:24]))
    sumpath4 = sum(abs(Vel[76:24, 24]))

    Circulation = abs(sumpath1) + abs(sumpath2) + abs(sumpath3) + abs(sumpath4)

    return Circulation

def path_integral_velocityall(
        u, v
):
    Vel = np.sqrt(np.square(U)+np.square(V))

    point_a = [25, 25]
    point_b = [25, 75]
    point_c = [75, 75]
    point_d = [75, 25]

    # path1 = #(25,25) - (75,25) in x
    # path2 = #(75,25) - (75,75) in y
    # path3 = #(75,75) - (25,75) in -x
    # path4 = #(25,75) - (25,25) in -y

    sumpath1 = sum(abs(Vel[0, :]))
    sumpath2 = sum(abs(Vel[:, 99]))
    sumpath3 = sum(abs(Vel[99, :]))
    sumpath4 = sum(abs(Vel[:, 0]))

    Circulation = abs(sumpath1) + abs(sumpath2) + abs(sumpath3) + abs(sumpath4)

    return Circulation


pathCirc = path_integral_velocity(U, V)
print("path Circ synthetic", pathCirc)
pathCircall = path_integral_velocityall(U, V)
print("pathCircall synthetic", pathCircall)

point_a = [25, 25]
point_b = [25, 75]
point_c = [75, 75]
point_d = [75, 25]

f2, ax2 = plt.subplots()
ax2.contourf(vort)
ax2.scatter(point_a[1],point_a[0]) 
ax2.scatter(point_b[1],point_b[0])
ax2.scatter(point_c[1],point_c[0])
ax2.scatter(point_d[1],point_d[0])
# plt.show()

print("sum_vort", sum_vort)
print("sum_vort2575", sum_vort2575)


def path_integral_velocity97(
        u, v
):
    Vel = np.sqrt(np.square(U)+np.square(V))

    sumpath1 = sum(abs(Vel[0, :]))
    sumpath2 = sum(abs(Vel[:, 97]))
    sumpath3 = sum(abs(Vel[97, :]))
    sumpath4 = sum(abs(Vel[:, 0]))

    Circulation = abs(sumpath1) + abs(sumpath2) + abs(sumpath3) + abs(sumpath4)

    return Circulation

u, v = oj.importData("G:/AftificialVortex/Hamel-Oseen Vortex/PIVlab.mat")
Hamel_Osseen = oj.sum_Vorticity(u, v)
V_mag = np.sqrt((np.square(u) + np.square(v)))
Hamel_Osseen_Circ = path_integral_velocity97(u[0,:,:], v[0,:,:])
print("Hamel_Osseen_Circ: ",  int(Hamel_Osseen_Circ))
print("Hamel_Osseen_sum_vort: ",  int(Hamel_Osseen[0]))

f3, ax3 = plt.subplots()
ax3.quiver(u[0,:,:],v[0,:,:])
ax3.scatter(point_a[1],point_a[0], label = "Point a") 
ax3.scatter(point_b[1],point_b[0], label = "Point b")
ax3.scatter(point_c[1],point_c[0], label = "Point c")
ax3.scatter(point_d[1],point_d[0], label = "Point d")
plt.legend()
# plt.show()

Hamel_Osseen_Vort, gauss = oj.calculate_vorticity(u, v)


f4, ax4 = plt.subplots()
ax4.contourf(gauss[0,:,:])
ax4.scatter(point_a[1],point_a[0], label = "Point a") 
ax4.scatter(point_b[1],point_b[0], label = "Point b")
ax4.scatter(point_c[1],point_c[0], label = "Point c")
ax4.scatter(point_d[1],point_d[0], label = "Point d")
plt.legend()

print(int(Hamel_Osseen_Vort[0, int(Hamel_Osseen_Vort.shape[1]/2), int(Hamel_Osseen_Vort.shape[2]/2)]))

f5, ax5 = plt.subplots()
plt.title("Velocity Magnitude Profile midline")
ax5.plot(V_mag[0,50,:])
plt.legend()


f6, ax6 = plt.subplots()
plt.title("Vorticity Magnitude Profile midline")
ax6.plot(Hamel_Osseen_Vort[0, int(Hamel_Osseen_Vort.shape[1]/2), :])
plt.legend()


f7, ax7 = plt.subplots()
plt.title("v velocity Profile midline in y")
ax7.plot(v[0, int(Hamel_Osseen_Vort.shape[1]/2), :])
plt.legend()


f8, ax8 = plt.subplots()
plt.title("u velocity Profile midline in x")
ax8.plot(u[0, :, int(Hamel_Osseen_Vort.shape[2]/2)])
plt.legend()
plt.show()