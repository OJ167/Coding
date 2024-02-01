import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, rfft, rfftfreq




# Number of sample points
N = 500
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N, endpoint=False)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x) + 1.25*np.sin(10.0 * 2.0*np.pi*x)
yf = fft(y)
xf = fftfreq(N, T)[:N//2]

f6, (ax6, ax7) = plt.subplots(nrows=1, ncols=2)
ax6.plot(y)
ax7.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.show()