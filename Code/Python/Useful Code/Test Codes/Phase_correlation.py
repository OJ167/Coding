import numpy as np
import matplotlib.pyplot as plt
from scipy. signal import correlate
# Define parameters
f1 = 1  # Frequency of first signal
f2 = 1.2  # Frequency of second signal
phase_shift = np.pi/3  # Phase shift between signals
t = np.linspace(0, 5, 1000)  # Time range

# Generate signals
signal1 = np.sin(2 * np.pi * f1 * t)
signal2 = 2* np.sin(2 * np.pi * f2 * t + phase_shift)

# Calculate cross-correlation
corr = np.correlate(signal1, signal2, mode='full')
lag = np.argmax(corr) - len(signal1) // 2  # Find peak lag

# Align signals
aligned_signal2 = np.roll(signal2, lag)

# Plot signals
corr = correlate(signal1, signal2, 'same')
plt.plot(t, signal1, label='Signal 1')
plt.plot(t, aligned_signal2, label='Aligned Signal 2')
plt.plot(t, corr, label='CORR')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Phase-aligned sine waves')
plt.legend()
plt.show()


print(corr)
print(corr.shape)