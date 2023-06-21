import numpy as np
import os
from scipy import io

def importData(dir): 

    os.chdir(os.path.dirname(dir))
    mat_contents = io.loadmat(os.path.basename(dir))
    u_temp = np.squeeze(mat_contents['u_filtered'])
    v_temp = np.squeeze(mat_contents['v_filtered'])
    print("Filtered Data Imported")
    u = np.empty((u_temp.shape[0], u_temp[0].shape[0], u_temp[0].shape[1]))
    for i in range(u.shape[0]):
        u[i] = u_temp[i]
    v = np.empty((v_temp.shape[0], v_temp[0].shape[0], v_temp[0].shape[1]))
    for i in range(v.shape[0]):
        v[i] = v_temp[i]

    return u, v

u, v = importData('/Volumes/Samsung SSD T5/.EXPERIMENTS/2021-05-24/RPM-6_Pump-5_FPS-60_JET/1/Data/PIV_export.mat')

a = np.mean(u)
print(a)