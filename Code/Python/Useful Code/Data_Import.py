import numpy as np
import os
import sys
import mat73
from scipy import io
import matplotlib.pyplot as plt

#####Import Ollie Tools
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)


def importData73(dir):
    """
    loads matlab data from a .MAT file. Crucially the variables loaded in the file are 'u_filtered' and v_filtered.

    INPUT:
        dir         : Full path of file to be opened, must include file extension.

    OUTPUT:
        u           : 3D Numpy tensor containing velocity data, has not been scaled.
        v           : 3D Numpy tensor containing velocity data, has not been scaled.
    """

    os.chdir(os.path.dirname(dir))
    mat_contents = mat73.loadmat(os.path.basename(dir))
    u_temp = np.squeeze(mat_contents["u_filtered"])
    v_temp = np.squeeze(mat_contents["v_filtered"])
    u = np.empty((u_temp.shape[0], u_temp[0].shape[0], u_temp[0].shape[1]))
    for i in range(u.shape[0]):
        u[i] = u_temp[i]
    v = np.empty((v_temp.shape[0], v_temp[0].shape[0], v_temp[0].shape[1]))
    for i in range(v.shape[0]):
        v[i] = v_temp[i]
    print(str("Filtered Data Imported  -  " + str(u.shape)))
    u, v = oj.FlipArrayVert(u, v)
    return u, v

def importData(dir):
    """
    loads matlab data from a .MAT file. Crucially the variables loaded in the file are 'u_filtered' and v_filtered.

    INPUT:
        dir         : Full path of file to be opened, must include file extension.

    OUTPUT:
        u           : 3D Numpy tensor containing velocity data, has not been scaled.
        v           : 3D Numpy tensor containing velocity data, has not been scaled.
    """

    os.chdir(os.path.dirname(dir))
    mat_contents = io.loadmat(os.path.basename(dir))
    u_temp = np.squeeze(mat_contents["u_filtered"])
    v_temp = np.squeeze(mat_contents["v_filtered"])
    u = np.empty((u_temp.shape[0], u_temp[0].shape[0], u_temp[0].shape[1]))
    for i in range(u.shape[0]):
        u[i] = u_temp[i]
    v = np.empty((v_temp.shape[0], v_temp[0].shape[0], v_temp[0].shape[1]))
    for i in range(v.shape[0]):
        v[i] = v_temp[i]
    print(str("Filtered Data Imported  -  " + str(u.shape)))
    u, v = oj.FlipArrayVert(u, v)
    return u, v

def scaleVel(u, v, fps, heightPixels=1976, heightImage=0.405):
    """
    Scales velocity fields for u and v based on image height, n pixels and the fps of the camera.

    INPUT:
        u           : 3D Numpy tensor containing velocity data, has not been scaled.
        v           : 3D Numpy tensor containing velocity data, has not been scaled.

    OUTPUT:
        u           : 3D Numpy tensor containing scaled velocity data.
        v           : 3D Numpy tensor containing scaled velocity data.
    """

    factor = fps * heightImage / heightPixels
    u = factor * u
    v = factor * v
    return u, v


# u, v = importData("F:/Testing/RPM-6.34__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab")
u, v = importData("F:/Testing/RPM-0__Upiston-100__Stroke-100/2022-11-24__FPS-30/1/Data/PIVlab")

f1, ax1 = plt.subplots(nrows=1, ncols=1)

for i in range(100, 251, 30):
    ax1.plot(u[i, 12, :])  
# plt.show()

# def lowOrderPolyfit(x, y, order):

#     z = np.polyfit(x, y, order)

#     p = np.poly1d(z)

#     xB = np.linspace(np.min(x), np.max(x), 100)

#     Xmax = xB[np.argmax(p(xB))]

#     return p, Xmax



# x = np.arange(u.shape[2])
# xLoc = np.zeros((10, 10))
# gradT = np.zeros(10)

# for t in range(10):
#     for i in range(10):
#         uSlice = u[(t*20+100), i, :]
#         plt.plot(uSlice)
#         maxPos = np.argmax(uSlice)
#         plt.scatter(x[maxPos], uSlice[maxPos])
#         p, xLoc[t, i] = lowOrderPolyfit(x[maxPos-2:maxPos+3], uSlice[maxPos-2:maxPos+3], 2)
#         # print(maxPos, "- ", xLoc[t, i])
#         plt.show

#     gradT[t] = np.tan(np.mean(np.gradient(xLoc[t,:])))

# print(gradT)
# f2, ax2 = plt.subplots(nrows=1, ncols=1)
# ax2.plot(gradT[:])
# plt.show()





oj.velocityTracking(u, v)