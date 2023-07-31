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
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)


####Import Ollie Tools MAC
# dirPath = "/Users/olliejackson/Coding/Code"
# sys.path.insert(0, dirPath)
# import OllieTools as oj
# print(dirPath)

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("jet_r")


# Dir  = "F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 
# umean, vmean = oj.scaleVel(umean, vmean, 90, 1900, 0.21918)
# time = oj.frames_to_seconds(umean, vmean, 90)

u,  v = oj.importData73("F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/2/Data/PIV_export.mat")

oj.animate_cube_quiver(u, v, interval=11.1, cmap="bwr", save=1, output="0/50/50.mp4", fps=90, scale = 1, fsize = (19, 12))
