import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import random
import numpy as np

x = np.random.randint(0, 100, size=100)
    
x_gaussian = gaussian_filter(x, sigma=0.7)
plt.plot(x[:])
plt.plot(x_gaussian[:])
plt.show()