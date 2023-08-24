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
# Dir  = "G:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 

#### 1 RPM ####
# Dir  = "G:/Testing/RPM-1.0__Upiston-100__Stroke-100/2023-08-23__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 

#### 2 RPM ####
# Dir  = "G:/Testing/RPM-2.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 

#### 3 RPM ####
# Dir  = "F:/Testing/RPM-3.0__Upiston-50__Stroke-50/2023-05-23__FPS-90/" DON'T HAVE YET
# umean, vmean = oj.create_Mean(10, Dir) 

#### 6 RPM ####
# Dir  = "G:/Testing/RPM-6.0__Upiston-100__Stroke-100/2023-08-18__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 

#### 9 RPM ####
# Dir  = "G:/Testing/RPM-9.0__Upiston-100__Stroke-100/2023-08-19__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 

#### 12 RPM ####
# Dir = "G:/Testing/RPM-12.0__Upiston-100__Stroke-100/2023-08-21__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir) 





#### 0 RPM ####
# Dir0  = "G:/Testing/RPM-0.0__Upiston-50__Stroke-100/2023-08-22__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir0) 

#### 1 RPM ####
# Dir1  = "G:/Testing/RPM-1.0__Upiston-50__Stroke-100/2023-08-23__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir1) 

#### 2 RPM ####
# Dir2  = "G:/Testing/RPM-2.0__Upiston-50__Stroke-100/2023-08-17__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir2) 

#### 3 RPM ####
# Dir3  = "F:/Testing/RPM-3.0__Upiston-100__Stroke-50/2023-05-15__FPS-90/" DON'T HAVE YET
# umean, vmean = oj.create_Mean(10, Dir3) 

#### 6 RPM ####
# Dir6  = "G:/Testing/RPM-6.0__Upiston-50__S/troke-100/2023-08-18__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir6) 

#### 9 RPM ####
# Dir9  = "G:/Testing/RPM-9.0__Upiston-50__Stroke-100/2023-08-19__FPS-90/"
# umean, vmean = oj.create_Mean(10, Dir9) 

#### 12 RPM ####
Dir12 = "G:/Testing/RPM-12.0__Upiston-50__Stroke-100/2023-08-21__FPS-90/"
umean, vmean = oj.create_Mean(10, Dir12) 



#################################################################################################################################
Vels = np.stack((umean, vmean), axis=-1)

### Use this to write ‘w’
# h5file = h5py.File('F:/H5/meandataVLS.h5', 'w')

### Use this to append ‘a’
h5file = h5py.File('G:/H5/meandataVLS.h5', 'a')

############# these exist to correct incorrectly saved data 
# h5file = h5py.File('E:/H5/dataHLS.h5', 'r+')

# data = h5file['Lower/RPM0/INJ2']
# data[...] = Vels



h5file.create_dataset('Narrow/U50/L100/RPM12', data=Vels)

descend_obj(h5file)

h5file.close()

