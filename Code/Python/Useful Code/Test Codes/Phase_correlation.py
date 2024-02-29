import numpy as np
import matplotlib.pyplot as plt
from scipy. signal import correlate, correlation_lags
import random

# Define parameters
f1 = 1  # Frequency of first signal
f2 = 1  # Frequency of second signal
phase_shift = 0# np.pi/3  # Phase shift between signals
t = np.linspace(0, np.pi, 1000)  # Time range

# Generate signals
signal1 = np.sin(2 * np.pi * f1 * t)
signal2 = np.sin(2 * np.pi * f2 * t + phase_shift)

# Calculate cross-correlation
corr = np.correlate(signal1, signal2, mode='full')
autocorr = np.correlate(signal1, signal1, mode='same')
lag = np.argmax(corr) - len(signal1) // 2  # Find peak lag

# Align signals
aligned_signal2 = np.roll(signal2, lag)

# Plot signals
corr = correlate(signal1, signal2, 'same')
plt.plot(t, signal1, label='Signal 1')
plt.plot(t, aligned_signal2, label='Aligned Signal 2')
# plt.plot(t, signal2, label='Aligned Signal 2')
# plt.plot(t, corr, label='CORR')
# plt.plot(t, autocorr/np.max(autocorr), label='auto CORR')
plt.plot(t, corr/np.max(corr), label='normalised Correlation')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Phase-aligned sine waves')
plt.legend()


# print(corr)
# print(corr.shape)



################## Attempt 2

### two cubic functions of different powers, with different 'phase'

h = random.uniform(0, 1000)
print('random shift = ' + str(h))
x = np.linspace(-10, 10, 1000)
# y1 = 3*x**3 + h
# y2 = x**3

y1 = np.sin(x + h)
y2 = np.sin(x)

cubic_cor = correlate(y1, y2, 'same')
maxcor = np.argmax(cubic_cor)

correlation = correlate(y1, y2, mode='full')
lags = correlation_lags(y1.size, y2.size, mode='full')
lag = lags[np.argmax(correlation)]

print(lag)

print('correlation peak location = ' +str(maxcor))
phase_correct = y1 - lag
xphase_correct = x - lag

f1, (ax1, ax2, ax3) = plt.subplots(ncols = 3)
ax1.plot(x, y1, label = 'y1')
ax1.plot(x, y2, label = 'y2')
ax2.plot(cubic_cor)
ax3.plot(xphase_correct, y1, label = 'phase corrected')
ax3.plot(x, y2, label = 'y2')
plt.legend()
# plt.show()



# attempt 3

x = np.linspace(0, 10, 1000)
shift = 3
sig1 = np.sin(x)
sig2 = np.sin(x + shift)

correlation = correlate(sig1, sig2, mode='full')
lags = correlation_lags(sig1.size, sig2.size, mode='full')
lag = lags[np.argmax(correlation)]

print(lag)

f2, (ax4, ax5) = plt.subplots(ncols=2)
ax4.plot(x, sig1, label = 'sig1')
ax4.plot(x, sig2, label = 'sig2')
ax5.plot(x, sig1, label = 'sig1')
ax5.plot(x[:-296], sig2[296:], label = 'sig2')
plt.legend()
plt.show()
