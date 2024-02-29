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


#### Import Rings

u, v = oj.importData73("F:/Testing/3Do/No_Ring/RPM3/60FPS_3000Frame/Data/PIV_export_fine.mat")

r_nd, z_nd = oj.NDUnitsForPlotsNozzle(u.shape[1], u.shape[2])

umean, vmean = np.mean(u, axis=0), np.mean(v, axis=0)

V = np.sqrt((abs(umean**2) + abs(vmean**2)))

f1, (ax1, ax2) = plt.subplots(ncols=2)
ax1.imshow(umean[:,:], cmap = 'bwr')
ax1.set_title('U mean')
ax2.imshow(vmean[:,:], cmap = 'bwr')
ax2.set_title('V mean')
plt.legend()






ufilt, vfilt = oj.filterTankRPM2(u, v, 60, 6)
ufiltmean, vfiltmean = np.mean(ufilt, axis=0), np.mean(vfilt, axis=0)
Vfilt = np.sqrt((abs(ufiltmean**2) + abs(vfiltmean**2)))


vmin = min(np.min(u), np.min(ufilt))
vmax = max(np.max(u), np.max(ufilt))
norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

f2, (ax3, ax4) = plt.subplots(ncols=2)
ax3.imshow(V, cmap = 'bwr')
ax3.set_title('Velocity magnitude')
ax4.imshow(Vfilt, cmap = 'bwr')
ax4.set_title('filtered Velocity magnitude')

f1, ax = plt.subplots(ncols=2, nrows=2)
ax[0,0].imshow(umean[:,:], cmap = 'bwr')
ax[0,0].set_title('U mean')
ax[0,1].imshow(vmean[:,:], cmap = 'bwr')
ax[0,1].set_title('V mean')
ax[1,0].imshow(ufiltmean[:,:], cmap = 'bwr')
ax[1,0].set_title('U filtered mean')
ax[1,1].imshow(vfiltmean[:,:], cmap = 'bwr')
ax[1,1].set_title('V filtered mean')
plt.legend()




##### doing a fourier analysis of a single point

uf = fft(u[:, int(u.shape[1]/2),int(u.shape[2]/2) ])
xf = fftfreq(u.shape[0], 1/60)

f6, (ax6, ax7) = plt.subplots(nrows=1, ncols=2)
ax6.plot(uf)
ax7.plot(xf)[:int(u.shape[0]//2)]
plt.show()


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
        Fourier = np.zeros[[Array.shape[:]]]
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



Fourieru, U_u_Mean_fft = FFT(umean, 1/60)
f4, (ax4, ax5) = plt.subplots(ncols=2, nrows = 1)
ax4.plot(Fourieru)
ax5.plot(U_u_Mean_fft)
plt.show()