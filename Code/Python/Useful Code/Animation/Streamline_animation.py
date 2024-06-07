#### Import stuff

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
import matplotlib.animation as animation

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

plt.style.use(['notebook', 'grid'])
plt.style.use(['science', 'no-latex'])#, 'grid'])

######## load data

Rotations = ['RPM0', 'RPM1', 'RPM2', 'RPM3', 'RPM6', 'RPM9', 'RPM12']
Injection = ['U50', 'U100']
Length = ['L50', 'L100']

h5file = h5py.File('E:/H5/meandataVLSFine.h5', 'r')
vels = h5file['Narrow'][str(Injection[0])][str(Length[0])][str(Rotations[6])]
u = vels[:,:,:,0]
v = vels[:,:,:,1]
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])

z_nd_star = z_nd - 0.55
frame = 350
frame = 750

V = np.sqrt(u[frame,:,:]**2 + v[frame,:,:]**2)

######## create streamline plot
#### change the axes so that the 0 is at nozzle exit

im = plt.imread('C:/Users/u2088308/Pictures/image1_bg.tiff')
f1, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.imshow(im,extent=[ z_nd_star[0], z_nd_star[-1], r_nd[0], r_nd[-1]], cmap = 'Greys_r')
ax1.streamplot(z_nd_star, r_nd, u[frame,:,:], v[frame,:,:], color = 'g', broken_streamlines = False, linewidth=V[:,:])
# ax1.streamplot(z_nd_star, r_nd, u[frame,:,:], v[frame,:,:], cmap = 'Greens', broken_streamlines = False, color=V[:,:])
ax1.set_xlim([z_nd_star[0], z_nd_star[-1]])
ax1.set_ylim([r_nd[0], r_nd[-1]])
ax1.grid(False)
ax1.set_xlabel("z/D")
ax1.set_ylabel("r/D")
plt.show()

######## create animation

def animate_cube_streamline(
    u, v, im, interval=11.1, color = 'g', save=0, output="15.mp4", fps=90, scale = 1, fsize = (12, 10), Dir = "", name = ""
):

    """
    animates a numpy 3D Array for quick visualisation (specific to contourf).

    INPUT:
        u           : 3D numpy array of axial velocity that needs to be animated.
        v           : 3D numpy array of radial velocity that needs to be animated.
        im          : background image.
        interval    : no. of ms between each frame.
        color       : color of streamlines. Default=green

    OUTPUT:
        animated window going through the cube.

    """
    r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
    z_nd = z_nd - 0.55

    output = str(Dir) + str(name)
    print(output)

    fig, ax = plt.subplots(figsize=fsize)
    def animate(i):
        V = np.sqrt(u[i,:,:]**2 + v[i,:,:]**2)
        print(i)
        ax.clear()
        ax.grid(False)
        ax.imshow(im,extent=[ z_nd_star[0], z_nd_star[-1], r_nd[0], r_nd[-1]], cmap = 'Greys_r')
        # ax.streamplot(z_nd_star, r_nd, u[i,:,:], v[i,:,:], color = color, broken_streamlines = False)
        ax.streamplot(z_nd_star, r_nd, u[i,:,:], v[i,:,:], color = color, broken_streamlines = False, linewidth=V[:,:])
        ax.set_title("%03d" % (i))
        ax.set_xlim([z_nd[0], z_nd[-1]])
        ax.set_ylim([r_nd[0], r_nd[-1]])
        ax.set_xlabel("z/D")
        ax.set_ylabel("r/D")

    ani = animation.FuncAnimation(
        fig, animate, frames=u.shape[0], interval=interval, blit=False
    )

    # plt.colorbar()
    if save == 0:
        plt.show()
    else:
        ani.save(output, writer="ffmpeg", fps=fps, dpi=160)

# animate_cube_streamline(u[75:76,:,:], v[75:76,:,:], im, interval=11.1, color = 'g', save=0, output="15.mp4", fps=90, scale = 1, fsize = (12, 10))

######## save animation

# for i in range(len(Rotations)):
#     for j in range(len(Injection)):
#         for k in range(len(Length)):
#             vels = h5file['Narrow'][str(Injection[j])][str(Length[k])][str(Rotations[i])]
#             u = vels[:,:,:,0]
#             v = vels[:,:,:,1]
#             output = str(Rotations[i]) + "_" + str(Injection[j]) + "_" + str(Length[k]) + ".mp4"
#             name = str(Rotations[i]) + "_" + str(Injection[j]) + "_" + str(Length[k]) + ".mp4"
#             print(name)
#             animate_cube_streamline(u, v, im, interval=11.1, color = 'g', save=1, output=output, Dir = "C:/Users/u2088308/Videos/", name = name, fps=90, scale = 1, fsize = (12, 10))


# for i in range(len(Rotations)):
for i in range(1):
    vels = h5file['Narrow'][str(Injection[1])][str(Length[1])][str(Rotations[i])]
    u = vels[:,:,:,0]
    v = vels[:,:,:,1]
    output = str(Rotations[0]) + "_" + str(Injection[1]) + "_" + str(Length[1]) + ".mp4"
    name = str(Rotations[0]) + "_" + str(Injection[1]) + "_" + str(Length[1]) + ".mp4"
    print(name)
    animate_cube_streamline(u, v, im, interval=11.1, color = 'g', save=1, output=output, Dir = "C:/Users/u2088308/Videos/", name = name, fps=90, scale = 1, fsize = (12, 10))
