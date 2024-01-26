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





##########################################################################################################################################
#### This script produces animations of line plots of the radial and azimuthal flow profiles in the HLS configuration. The main code for
#### calculation is taken from the 'SamHLSIdeas.py' script and any profile generated in that script can be animated in this one.
#### The
##########################################################################################################################################





h5file = h5py.File('E:/H5/3D0HLSFine.h5', 'r')

frame = 1000
fps = 150
frametime = frame/fps
d = 0.1
vels = h5file['3D0']['U100']['L100']['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
h5file.close()
u_gaussian, v_gaussian = gaussian_filter(u, sigma=6), gaussian_filter(v, sigma=6)
x = np.linspace(0 , u.shape[2], u.shape[2])
y = np.linspace(0 , u.shape[1], u.shape[1])
time = oj.frames_to_seconds(u, v, 150)
print(u.shape[0], u.shape[1], u.shape[2])


def animate_Line( 
    u, U_r_profile, interval=6.66, save=0, output="15.mp4", fps=150, scale = 1, fsize = (19, 12)
):

    """
    animates a line of a flow profile.

    INPUT:
        cube_array  : name of 3D numpy array that needs to be animated.
        2D numpy array
        interval    : no. of ms between each frame.


    OUTPUT:
        animated line graph.

    """
    ###Calculating the line for Uaz and Ur for the whole time series
    
    time = oj.frames_to_seconds(u, u, fps)

    fig, ax = plt.subplots(figsize=fsize)

    def animate(i):
        ax.clear()
        ax.plot(U_az_profile[i,:])
        ax.plot(U_r_profile[i,:])
        ax.set_title("Time " + str("%.1f") %time[i])
        ax.set_xlabel("r/D")
        ax.set_ylabel(r"$U_{r}$")
        # ax.set_ylim(np.min(u), np.max(u))

    ani = animation.FuncAnimation(
        fig, animate, frames=u.shape[0], interval=interval, blit=False
    )

    # plt.colorbar()
    if save == 0:
        plt.show()  
    else:
        ani.save(output, writer="ffmpeg", fps=fps, dpi=80)


####Azimuthal Profiles
U_az_profile = np.zeros((u.shape[0], 35611))
U_az_Mean = np.zeros(u.shape[0])
U_az_Peak = np.zeros(u.shape[0])
radial_Position = np.zeros(u.shape[0])

####Radial Profiles
U_r_profile = np.zeros((u.shape[0], 35611))
radial_Position = np.zeros(u.shape[0])
U_r_Mean = np.zeros(u.shape[0])
U_r_Peak = np.zeros(u.shape[0])


for i in range(u.shape[0]):
    oj.progressBar(i, u.shape[0], width=40)
    r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u_gaussian[i,:,:], v_gaussian[i,:,:])
    inds = (r.flatten()).argsort()
    r2 = (r.flatten())[inds]

    ####Azimuthal Results
    U_az2 = (U_az.flatten())[inds]
    paz = np.poly1d(np.polyfit(r2, U_az2, 11))(r2) #This turns the graph into a polynomial line
    maxaz = np.argmax(U_az2)
    # max = np.argmax(p)
    U_az_Mean[i] = np.mean(paz)
    U_az_Peak[i] = np.max(paz)
    radial_Position[i] = maxaz
    U_az_profile[i, :] = paz

    ####Radial Results
    U_r2 = (U_r.flatten())[inds]
    pr = np.poly1d(np.polyfit(r2, U_r2, 11))(r2) #This turns the graph into a polynomial line
    maxr = np.argmax(U_r2)
    # maxr = np.argmax(pr)
    U_r_Mean[i] = np.mean(U_r2)
    U_r_Peak[i] = np.max(U_r2)
    radial_Position[i] = maxr
    U_r_profile[i, :] = pr


# f1, ax1 = plt.subplots()
# plt.title(r"$U_{az}$ and U_{r} profiles")
# ax1.plot(U_az_profile[1000,:], label = r"$U_{az}$")
# ax1.plot(U_r_profile[1000,:] , label = r"$U_{r}$")
# plt.legend()
# plt.show()
 


animate_Line(u, U_r_profile, interval=6.66, save=0, output="15.mp4", fps=150, scale = 1, fsize = (19, 12))