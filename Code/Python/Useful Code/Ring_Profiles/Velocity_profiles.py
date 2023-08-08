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

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])

Rotations = ['RPM0', 'RPM1', 'RPM2', 'RPM3', 'RPM6', 'RPM9', 'RPM12']
Injection = ['U50', 'U100']
I = 'U50'


h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)]['L50'][str(Rotations[0])]
u0mean = vels[:,:,:,0]
v0mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)]['L50'][str(Rotations[1])]
u1mean = vels[:,:,:,0]
v1mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)]['L50'][str(Rotations[2])]
u2mean = vels[:,:,:,0]
v2mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)]['L50'][str(Rotations[3])]
u3mean = vels[:,:,:,0]
v3mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)]['L50'][str(Rotations[4])]
u6mean = vels[:,:,:,0]
v6mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)]['L50'][str(Rotations[5])]
u9mean = vels[:,:,:,0]
v9mean = vels[:,:,:,1]

h5file = h5py.File('F:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)]['L50'][str(Rotations[6])]
u12mean = vels[:,:,:,0]
v12mean = vels[:,:,:,1]

time = oj.frames_to_seconds(u0mean, v0mean, 90)
r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u0mean.shape[1], u0mean.shape[2])

#### Animation of Profiles ####

def animate_Line( 
    u, v, row = 13, interval=11.1, save=0, output="15.mp4", fps=90, scale = 1, fsize = (19, 12)
):

    """
    animates a Line from a 3D Array for quick visualisation.

    INPUT:
        cube_array  : name of 3D numpy array that needs to be animated.
        interval    : no. of ms between each frame.


    OUTPUT:
        animated line graph.

    """

    x, y = np.meshgrid(np.arange(0, 111, 1), np.arange(0, 69, 1))
    V = np.sqrt((np.square(u) + np.square(v)))
    r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])
    time = oj.frames_to_seconds(u, v, 90)

    fig, ax = plt.subplots(figsize=fsize)

    def animate(i):
        ax.clear()
        ax.plot(r_nd, u[i,:, row])
        ax.set_title("Time " + str("%.1f") %time[i])
        ax.set_xlabel("r/D")
        ax.set_ylim(np.min(u0mean), np.max(u0mean))

    ani = animation.FuncAnimation(
        fig, animate, frames=V.shape[0], interval=interval, blit=False
    )

    # plt.colorbar()
    if save == 0:
        plt.show()  
    else:
        ani.save(output, writer="ffmpeg", fps=fps, dpi=80)

animate_Line(u0mean, v0mean,)

x, y = np.meshgrid(np.arange(0, 111, 1), np.arange(0, 69, 1))
f1, ax1 = plt.subplots()
ax1.quiver(x, y, u0mean[78,:,:], v0mean[78,:,:])
ax1.scatter(14, 30)
plt.show()

vort, gauss = oj.calculate_vorticity(u0mean, v0mean)

f1, ax1 = plt.subplots()
ax1.contourf(gauss[78,:,:])
ax1.scatter(13, 25)
plt.show()


#### Profiles in radial direction ####



