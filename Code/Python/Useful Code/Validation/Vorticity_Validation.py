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
# from colorspacious import cspace_converter

#####Import Ollie Tools
# dirPath = "C:/Coding/Code"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)


####Import Ollie Tools MAC
dirPath = "/Users/olliejackson/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("jet_r")
