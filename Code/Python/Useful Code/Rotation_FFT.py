import csv
from scipy.fft import fftfreq, rfft, rfftfreq
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# data = np.array("/Users/olliejackson/signalFFT.csv")

data = np.genfromtxt('/Users/olliejackson/Pico Data/signalFFT3RPMish.csv', delimiter=',')

Time = data[:, 1]
X = data[:, 0]


time_from_start = Time[:] - Time[0]

meanTime = np.mean(time_from_start[-1]/ len(Time))
print(time_from_start[-1])

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

t = np.linspace(0, 10, 2500, endpoint=False)
plt.plot(t, signal.square(2 * np.pi * 1 * t))
plt.ylim(-2, 2)
plt.show()

squarefft, squarefreq = FFT(signal.square(2 * np.pi * 5 * t),1000000/meanTime) 
plt.plot(squarefreq, squarefft)
plt.show()



fftresult,fftfreq = FFT(X, 1000000/meanTime)

plt.plot(fftfreq, fftresult)
plt.show()

# plt.plot(Time, X)
# plt.show()