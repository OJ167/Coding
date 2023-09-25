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


# dir = (askdirectory())
# print(dir)
# u, v = oj.importData73(str(dir + '/Data/PIV_export.mat'))

#### 0 RPM ####
Dir  = "F:/Testing/3Do/RPM-0.0__Upiston-100__Stroke-100/2023-09-21__FPS-150/"
umean, vmean = oj.create_Mean(19, Dir) 

#### 1 RPM ####
# Dir  = "F:/Testing/3Do/RPM-1.0__Upiston-100__Stroke-100/2023-09-22__FPS-150/"
# umean, vmean = oj.create_Mean(10, Dir) 

#### 2 RPM ####
# Dir  = "F:/Testing/3Do/RPM-2.0__Upiston-100__Stroke-100/2023-09-21__FPS-150/"
# umean, vmean = oj.create_Mean(10, Dir) 

#### 3 RPM ####
# Dir  = "F:/Testing/3Do/RPM-3.0__Upiston-100__Stroke-100/2023-09-18__FPS-150/"
# umean, vmean = oj.create_Mean(10, Dir) 

#### 6 RPM ####
# Dir  = "F:/Testing/3Do/RPM-6.0__Upiston-100__Stroke-100/2023-09-20__FPS-150/"
# umean, vmean = oj.create_Mean(10, Dir) 

#### 9 RPM ####
# Dir  = "F:/Testing/3Do/RPM-9.0__Upiston-100__Stroke-100/2023-09-19__FPS-150/"
# umean, vmean = oj.create_Mean(10, Dir) 

#### 12 RPM ####
# Dir = "F:/Testing/3Do/RPM-12.0__Upiston-100__Stroke-100/2023-09-20__FPS-150/"
# umean, vmean = oj.create_Mean(10, Dir) 






#################################################################################################################################
Vels = np.stack((umean, vmean), axis=-1)

## Use this to write ‘w’
# h5file = h5py.File('F:/H5/3D0meandataHLS.h5', 'w')

# ### Use this to append ‘a’
# h5file = h5py.File('F:/H5/3D0meandataHLS.h5', 'a')

############# these exist to correct incorrectly saved data and comment out the create_dataset line
h5file = h5py.File('F:/H5/3D0meandataHLS.h5', 'r+')
data = h5file['3D0/U100/L100/RPM0']
data[...] = Vels



# h5file.create_dataset('3D0/U100/L100/RPM0', data=Vels)

descend_obj(h5file)

h5file.close()

