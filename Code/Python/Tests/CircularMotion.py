import numpy as np
import math

for i in range(-10,11):
    for j in range(-10,10):
        u = math.sqrt(i^2 + j^2) + math.cos(np.arctan(i/j))
        v = math.sqrt(i^2 + j^2) - math.sin(np.arctan(i/j))