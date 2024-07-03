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
# Dir  = "F:/Testing/3Do/RPM-0.0__Upiston-100__Stroke-50/2023-12-18__FPS-150/"
# umean, vmean = oj.create_Mean(10, Dir) 

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
# Dir = "F:/Testing/3Do/RPM-12.0__Upiston-100__Stroke-50/2023-12-21__FPS-150/"


#################blue drive
# Dir = 'F:/Testing/RPM-0.0__Upiston-50__Stroke-100/2023-08-22__FPS-90/'
# Dir = 'F:/Testing/RPM-0.0__Upiston-50__Stroke-50/2023-05-25__FPS-90/'
# Dir = 'F:/Testing/RPM-1.0__Upiston-50__Stroke-50/2023-07-24__FPS-90/'
# Dir = 'F:/Testing/RPM-1.0__Upiston-50__Stroke-100/2023-08-23__FPS-90/'
# Dir = 'F:/Testing/RPM-2.0__Upiston-50__Stroke-100/2023-08-17__FPS-90/'
# Dir = 'F:/Testing/RPM-2.0__Upiston-50__Stroke-50/2023-07-25__FPS-90/'
# Dir = 'F:/Testing/RPM-3.0__Upiston-50__Stroke-100/2023-08-24__FPS-90/'
# Dir = 'F:/Testing/RPM-3.0__Upiston-50__Stroke-50/2023-05-23__FPS-90/'
# Dir = 'F:/Testing/RPM-6.0__Upiston-50__Stroke-100/2023-08-18__FPS-90/'
# Dir = 'F:/Testing/RPM-6.0__Upiston-50__Stroke-50/2023-06-07__FPS-90/'
# Dir = 'F:/Testing/RPM-9.0__Upiston-50__Stroke-100/2023-08-19__FPS-90/'
# Dir = 'F:/Testing/RPM-9.0__Upiston-50__Stroke-50/2023-05-24__FPS-90/'
# Dir = 'F:/Testing/RPM-12.0__Upiston-50__Stroke-50/2023-05-19__FPS-90/'
# Dir = 'F:/Testing/RPM-12.0__Upiston-50__Stroke-100/2023-08-21__FPS-90/'


#################red drive
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90/'
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/'
# Dir = 'G:/Testing/RPM-1.0__Upiston-100__Stroke-50/2023-07-24__FPS-90/'
# Dir = 'G:/Testing/RPM-1.0__Upiston-100__Stroke-100/2023-08-23__FPS-90/'
# Dir = 'G:/Testing/RPM-2.0__Upiston-100__Stroke-50/2023-07-25__FPS-90/'
# Dir = 'G:/Testing/RPM-2.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/'
# Dir = 'G:/Testing/RPM-3.0__Upiston-100__Stroke-50/2023-05-15__FPS-90/'
# Dir = 'G:/Testing/RPM-3.0__Upiston-100__Stroke-100/2023-08-24__FPS-90/'
# Dir = 'G:/Testing/RPM-6.0__Upiston-100__Stroke-50/2023-05-11__FPS-90/'
# Dir = 'G:/Testing/RPM-6.0__Upiston-100__Stroke-100/2023-08-18__FPS-90/'
# Dir = 'G:/Testing/RPM-9.0__Upiston-100__Stroke-50/2023-05-12__FPS-90/'
# Dir = 'G:/Testing/RPM-9.0__Upiston-100__Stroke-100/2023-08-19__FPS-90/'
# Dir = 'G:/Testing/RPM-12.0__Upiston-100__Stroke-50/2023-05-19__FPS-90/'
# Dir = 'G:/Testing/RPM-12.0__Upiston-100__Stroke-100/2023-08-21__FPS-90/'
# umean, vmean = oj.create_Mean(10, Dir) 


######################0D0
# Dir = 'F:/Testing/HLS/RPM-0.0__Upiston-100__Stroke-100/2024-04-05__FPS-150/'
# Dir = '/'
# Dir = '/'
# Dir = '/'
# Dir = '/'
# Dir = '/'
# Dir = 'F:/Testing/HLS/RPM-12.0__Upiston-100__Stroke-100/2024-04-05__FPS-150/'
# umean, vmean = oj.create_Mean(10, Dir) 


######################Length Change testing
# Dir = 'F:/Testing/RPM-0.0__Upiston-100__Stroke-25/2024-06-10__FPS-90/' need to redo this one
# Dir = 'F:/0RPM/RPM-0.0__Upiston-100__Stroke-25/2024-06-12__FPS-90/'
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-50/2023-05-10__FPS-90/'
# Dir = 'F:/Testing/RPM-0.0__Upiston-100__Stroke-75/2024-06-10__FPS-90/'
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/'
# Dir = 'F:/0RPM/RPM-0.0__Upiston-100__Stroke-125/2024-06-12__FPS-90/'
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-150/2024-06-11__FPS-90/'
# Dir = 'F:/Testing/RPM-0.0__Upiston-100__Stroke-175/2024-06-11__FPS-90/'
# Dir = 'F:/Testing/RPM-0.0__Upiston-100__Stroke-200/2024-06-11__FPS-90/'
# Dir = 'F:/Testing/RPM-0.0__Upiston-100__Stroke-225/2024-06-11__FPS-90/'
# Dir = 'F:/0RPM/RPM-0.0__Upiston-100__Stroke-240/2024-06-12__FPS-90/'
# umean, vmean = oj.create_Mean(10, Dir) 



#######################NEW LENGTH CHANGE TESTING
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-25/2024-07-01__FPS-90/'
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-50/2024-07-02__FPS-90/' #NEW ONE
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-75/2024-07-01__FPS-90/'
# Dir = 'G:/Testing/Pre_Clean/RPM-0.0__Upiston-100__Stroke-75/2024-06-10__FPS-90/' # OLD OND
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-100/2024-07-01__FPS-90/' #NEW ONE
# Dir = 'F:/Testing/RPM-0.0__Upiston-100__Stroke-100/2023-08-22__FPS-90/' #OLD ONE
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-125/2024-06-28__FPS-90/'
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-150/2024-06-28__FPS-90/'
# Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-175/2024-06-28__FPS-90/'
Dir = 'G:/Testing/RPM-0.0__Upiston-100__Stroke-200/2024-07-02__FPS-90/'
# Dir = '/'
# Dir = '/'
umean, vmean = oj.create_Mean(10, Dir) 


#################################################################################################################################
Vels = np.stack((umean, vmean), axis=-1)

# Use this to write ‘w’
# h5file = h5py.File('G:/H5/LengthTestNEW.h5', 'w')

### Use this to append ‘a’
# h5file = h5py.File('G:/H5/LengthTestNEW.h5', 'a')

############# these exist to correct incorrectly saved data and comment out the create_dataset line
h5file = h5py.File('G:/H5/LengthTestNEW.h5', 'r+')
data = h5file['Narrow/U100/L200/RPM0']
data[...] = Vels



# h5file.create_dataset('0D0/U100/L25/RPM0', data=Vels)
# h5file.create_dataset('Narrow/U100/L200/RPM0', data=Vels)

descend_obj(h5file)

h5file.close()

