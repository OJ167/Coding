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
from scipy.fft import fft, fftfreq, rfft, rfftfreq
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

oj.tic()
# h5file = h5py.File('E:/H5/3D0meandataHLS.h5', 'r')
h5file = h5py.File('E:/H5/3D0HLSFine.h5', 'r')

frame = 750
frametime = frame/150
d = 0.1
vels = h5file['3D0']['U100']['L100']['RPM0']
u = vels[:,:,:,0]
v = vels[:,:,:,1]
h5file.close()
u_gaussian, v_gaussian = gaussian_filter(u, sigma=6), gaussian_filter(v, sigma=6)
time = oj.frames_to_seconds(u, v, 150)
print(u.shape[0], u.shape[1], u.shape[2])

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)


x = 55
y = 35
x = np.linspace(0 , umean.shape[1], umean.shape[1])
y = np.linspace(0 , umean.shape[0], umean.shape[0])
X, Y = np.meshgrid(x, y) 




r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u_gaussian[frame,:,:], v_gaussian[frame,:,:])
r_arr, theta_arr, U_rBins, U_azBins = oj.binCylindrical(r, theta, U_r, U_az, thetaBins=30, rBins=45)
inds = (r.flatten()).argsort()
r2 = (r.flatten())[inds]
U_az2 = (U_az.flatten())[inds]
pf = np.poly1d(np.polyfit(r2, U_az2, 11))(r2) #This turns the graph into a polynomial line
# max = np.argmax(p)
max = np.max(pf)
print(pf.shape)

f3, ax3 =plt.subplots()
# ax3.scatter(r2*d, U_az2)
plt.title(r"$U_{az}$ " + f"against Radius for frame {frame}")
ax3.plot(r2*d, pf)
ax3.set_xlabel("$r/d$")
ax3.set_ylabel(r"$U_{az}$")

f1, ax = plt.subplots(2, 2,)
ax[0,0].scatter(r2*d, U_az)
ax[0,0].set_title(r"$U_{az}$")
ax[0,1].scatter(r2*d, U_az2)
ax[0,1].set_title("U_az2")
ax[1,0].scatter(r2*d, pf)
ax[1,0].set_title("Pf")
ax[1,1].plot(r_arr, np.mean(U_azBins, axis = 1))
ax[1,1].set_title(r"$U_{az}$ bins")


#### Averaging the value frame by frame and seeing what happens

radial_Position = np.zeros(u.shape[0])
U_az_Mean = np.zeros(u.shape[0])
U_az_Peak = np.zeros(u.shape[0])

for i in range(u.shape[0]):
# for i in range(10): # for testing
    r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u_gaussian[i,:,:], v_gaussian[i,:,:])
    inds = (r.flatten()).argsort()
    r2 = (r.flatten())[inds]
    U_az2 = (U_az.flatten())[inds]
    p = np.poly1d(np.polyfit(r2, U_az2, 11))(r2) #This turns the graph into a polynomial line
    # max = np.argmax(U_az2)
    max = np.argmax(p)
    U_az_Mean[i] = np.mean(p)
    U_az_Peak[i] = np.max(p)
    radial_Position[i] = max


f4, ax = plt.subplots(2, 2)
plt.suptitle("Azimuthal Velocity Graphs")
ax[0,0].plot(r2*d, pf)
# ax[0,0].plot( pf)
ax[0,0].set_title(r"$U_{az}$ Polynomial" + f" - Time = {frametime}")
ax[0,0].set_xlabel("$r/d$")
ax[0,0].set_ylabel(r"$U_{az}$")
ax[0,1].plot(time, U_az_Mean)
ax[0,1].set_title(r"$U_{az}$ Mean/time")
ax[0,1].set_xlabel("$Time [s]$")
ax[0,1].set_ylabel(r"$\bar{U}_{az}$")
ax[1,0].plot(time, U_az_Peak)
ax[1,0].set_title(r"$U_{az}$ Peak/time")
ax[1,0].set_xlabel("$Time [s]$")
ax[1,0].set_ylabel(r"$U_{az} Peak$")
ax[1,1].plot(time, radial_Position)
ax[1,1].set_title(r"$U_{az}$ Peak location")
ax[1,1].set_xlabel("not defined")
ax[1,1].set_ylabel("radial location")
# plt.show()


#################################################################################
#### Radial flow Graphs:
#################################################################################


r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u_gaussian[frame,:,:], v_gaussian[frame,:,:])
r_arr, theta_arr, U_rBins, U_azBins = oj.binCylindrical(r, theta, U_r, U_az, thetaBins=30, rBins=45)
inds = (r.flatten()).argsort()
r2 = (r.flatten())[inds]
U_r2 = (U_r.flatten())[inds]
pr = np.poly1d(np.polyfit(r2, U_r2, 11))(r2) #This turns the graph into a polynomial line


radial_Position = np.zeros(u.shape[0])
U_r_Mean = np.zeros(u.shape[0])
U_r_Peak = np.zeros(u.shape[0])

for i in range(u.shape[0]):
# for i in range(10): # for testing
    r, theta, U_r, U_az, x0, y0 = oj.ConvertCylindrical(120, 75, x, y, u_gaussian[i,:,:], v_gaussian[i,:,:])
    inds = (r.flatten()).argsort()
    r2 = (r.flatten())[inds]
    U_r2 = (U_r.flatten())[inds]
    p = np.poly1d(np.polyfit(r2, U_r2, 11))(r2) #This turns the graph into a polynomial line
    # max = np.argmax(U_az2)
    max = np.argmax(p)
    U_r_Mean[i] = np.mean(U_r2)
    U_r_Peak[i] = np.max(U_r2)
    radial_Position[i] = max
oj.toc()


f5, ax = plt.subplots(2, 2)
plt.suptitle("Radial Velocity Graphs")
# ax[0,0].plot(U_r2)
ax[0,0].plot(pr)
ax[0,0].set_title(r"$U_{r}$ Polynomial" + f" - Time = {frametime}")
ax[0,0].set_xlabel("$r/d$")
ax[0,0].set_ylabel(r"$U_{r}$")
ax[0,1].plot(time, U_r_Mean)
ax[0,1].set_title(r"$U_{r}$ Mean/time")
ax[0,1].set_xlabel("$Time [s]$")
ax[0,1].set_ylabel(r"$\bar{U}_{r}$")
ax[1,0].plot(time, U_r_Peak)
ax[1,0].set_title(r"$U_{r}$ Peak/time")
ax[1,0].set_xlabel("$Time [s]$")
ax[1,0].set_ylabel(r"$U_{r} Peak$")
ax[1,1].plot(time, radial_Position)
ax[1,1].set_title(r"$U_{r}$ Peak location")
ax[1,1].set_xlabel("not defined")
ax[1,1].set_ylabel("radial location")
# plt.show()


#########################################################################################################
#### FFT on the results
#########################################################################################################

def FFT(Array, captureRate):
    """
    Uses Scipy real FFT function to give the frequencies and magnitudes of oscillations up to 1/2 of the sampling rate of the input data (fps). Abs value of spectra output.

    INPUT:
        Array       : 1D or 3D array containing velocity vectors over time.
        captureRate : The sampling rate of the data, this is usually fps. Do not input the frequency, instead number of samples per second. 

    OUTPUT:
        Fourier     : Magnitude of oscillations. 
        FFTfreq     : The frequency spectra correlating to the number of data points given and scaled using the sampling rate.

    """

    if Array.ndim == 1:
        Array = Array - np.mean(Array)
        Fourier = np.abs(rfft(Array))  # F[1:Array.shape[0]//2]
        FFTfreq = rfftfreq(Array.shape[0], 1 / captureRate)
        # FFTfreq = FFTfreq[1:Array.shape[0]//2]
    elif Array.ndim == 3:
        print('3D FFT')
        Array -= np.mean(Array, axis=0)
        Fourier = rfft(Array, axis=0)  # F[1:Array.shape[0]//2]
        FFTfreq = rfftfreq(Array.shape[0], 1 / captureRate)
        Fourier = np.mean(Fourier, axis=1)
        Fourier = np.mean(Fourier, axis=1)
        Fourier = np.abs(Fourier)
    return Fourier, FFTfreq

#fft of U_az 
Fourieraz, U_az_Mean_fft = FFT(U_az_Mean, 1/150)


#fft of U_r 
Fourierr, U_r_Mean_fft = FFT(U_r_Mean, 1/150)


f4, (ax4, ax5) = plt.subplots(ncols=2, nrows = 1)
ax4.plot(Fourieraz)
ax5.plot(Fourierr)
# plt.show()


# Number of sample points
N = 35611
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N, endpoint=False)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
yf = fft(y)
xf = fftfreq(N, T)[:N//2]

f6, (ax6, ax7) = plt.subplots(nrows=1, ncols=2)
ax6.plot(y)
ax7.plot(xf, 2.0/N * np.abs(yf[0:N//2]))



# Number of sample points
N = 2999
# sample spacing
T = 1 / 150
# x = np.linspace(0.0, N*T, N, endpoint=False)
y = U_az_Mean
yf = fft(y)
xf = fftfreq(N, T)[:N//2]

f7, (ax8, ax9) = plt.subplots(nrows=1, ncols=2)
ax8.plot(y)
ax9.plot(xf, 2.0/N * np.abs(yf[0:N//2]))



plt.show()