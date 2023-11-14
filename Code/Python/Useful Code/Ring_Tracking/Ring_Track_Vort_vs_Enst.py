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
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from scipy.interpolate import RectBivariateSpline
import h5py
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

##### Set plot style #####
plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("jet_r")



Rotations = ['RPM0', 'RPM1', 'RPM2', 'RPM3', 'RPM6', 'RPM9', 'RPM12']
Injection = ['U50', 'U100']
Stroke = ['L50', 'L100']
I = 'U100'
S = 'L50'

h5file = h5py.File('E:/H5/meandataVLS.h5', 'r')
vels = h5file['Narrow'][str(I)][str(S)][str(Rotations[0])]
u = vels[:,:,:,0]
v = vels[:,:,:,1]


# track vorticity Old
VortLocMaxold, VortLocMinold = oj.vorticityPeakTracking(u, v)

EnstLocMaxold = oj.enstrophyPeakTracking(u, v)
EnstLocMaxnew = oj.enstrophyPeakTracking_inter(u, v)

f2, ax2 = plt.subplots()
# ax2.plot(VortLocMaxold[:,1], label = "Vortex Max Old")
# ax2.plot(VortLocMinold[:,1], label = "Vortex Min Old")
ax2.plot(EnstLocMaxold[:,1], label = "Enstrophy Max Old")
ax2.plot(EnstLocMaxnew[:,1], label = "Enstrophy Max new")
plt.legend()
plt.show()



