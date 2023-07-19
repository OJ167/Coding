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
# dirPath = "C:/Coding/Code"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)


####Import Ollie Tools MAC
dirPath = "/Users/olliejackson/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

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


x_lim = (0, 101)
y_lim = (0, 101)
step = 1
scale = 3
# X, Y = np.meshgrid(np.arange(x_lim[0], x_lim[1], step), np.arange(y_lim[0], y_lim[1], step))


x = np.arange(0 , 100, 1)
y = np.arange(0 , 100, 1)
X, Y = np.meshgrid(x, y)
U = np.zeros(X.shape)
V = np.zeros(Y.shape)
xmod = np.sign(X)
ymod = np.sign(Y)

for i in range(X.shape[0]):
    for j in range(Y.shape[0]):
          U[i,j] = vf_x(X[i, j], Y[i, j])
          V[i,j] = vf_y(X[i, j], Y[i, j])
          
fig, ax = plt.subplots(sharex=True, sharey=True)
ax.quiver(X, Y, U, V, units='xy', pivot = 'middle', scale=50)
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

    sumpath1 = sum(abs(Vel[25, 25:75]))
    sumpath2 = sum(abs(Vel[25:75, 75]))
    sumpath3 = sum(abs(Vel[75, 75:25]))
    sumpath4 = sum(abs(Vel[75:25, 25]))

    Circulation = abs(sumpath1) + abs(sumpath2) + abs(sumpath3) + abs(sumpath4)

    return Circulation


pathCirc = path_integral_velocity(U, V)
print(pathCirc)


point_a = [25, 25]
point_b = [25, 75]
point_c = [75, 75]
point_d = [75, 25]

f2, ax2 = plt.subplots()
# ax2.contourf(vort)
ax2.plot(point_a, point_b, point_c, point_d)
plt.show()

print(sum_vort)
print(sum_vort2575)