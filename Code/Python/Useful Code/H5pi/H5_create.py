import matplotlib.pyplot as plt
import numpy as np
import h5py

import os
import sys

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)
plt.style.use(["science", "vibrant", "no-latex"])

from tkinter.filedialog import askdirectory

def descend_obj(obj,sep='\t'):
    """
    Iterate through groups in a HDF5 file and prints the groups and datasets names and datasets attributes
    """
    if type(obj) in [h5py._hl.group.Group,h5py._hl.files.File]:
        for key in obj.keys():
            print(sep,'-',key,':',obj[key])
            descend_obj(obj[key],sep=sep+'\t')
    elif type(obj)==h5py._hl.dataset.Dataset:
        for key in obj.attrs.keys():
            print(sep+'\t','-',key,':',obj.attrs[key])

fps = 30

dir = (askdirectory())
print(dir)

u, v = oj.importData73(str(dir + '/Data/PIV_export.mat'))
# u, v = sb.scaleVel(u, v, fps)
# u, v = oj.scaleHLSLower(u, v, fps)

Vels = np.stack((u, v), axis=-1)


h5file = h5py.File('G:/H5/dataHLS.h5', 'w')

### Use this to append ‘a’
h5file = h5py.File('G:/H5/dataHLS.h5', 'a')

############# these exist to correct incorrectly saved data 
# h5file = h5py.File('E:/H5/dataHLS.h5', 'r+')

# data = h5file['Lower/RPM0/INJ2']
# data[...] = Vels

h5file.create_dataset('Lower/RPM40/INJ64', data=Vels)

descend_obj(h5file)

h5file.close()

################ To load in. move this to another file 

h5file = h5py.File('G:/H5/dataHLS.h5', 'r')

vels0 = h5file['Lower']['RPM40']['INJ64']
u = vels0[:,:,:,0]
v = vels0[:,:,:,1]

umean = np.mean(u, axis=0)
vmean = np.mean(v, axis=0)

h5file.close()


f1, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.contourf(umean[:,:])
plt.title("Velocity Contour")
plt.legend()
plt.show()