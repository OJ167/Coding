import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

import os
import sys

import cv2
import glob
from scipy import ndimage, io
from scipy.ndimage.filters import gaussian_filter
from scipy import interpolate
import concurrent.futures
from scipy.fft import fft2,fftshift, ifft2, fft, fftfreq, ifft
import mat73


#####Import Ollie Tools
dirPath = "C:/Coding/Code"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

plt.style.use(["science", "vibrant", "no-latex"])
cmap = plt.get_cmap("jet_r")


def animate_cube_contourf(
    cube_array, interval=16.7, cmap="bwr", save=0, output="15.mp4", fps=60, scale = 1, fsize = (10, 8)
):

    """
    animates a numpy 3D Array for quick visualisation (specific to contourf).

    INPUT:
        cube_array  : name of 3D numpy array that needs to be animated.
        interval    : #of ms between each frame.
        cmap        : colormap. Default='bwr'

    OUTPUT:
        animated window going through the cube.

    """

    fig, ax = plt.subplots(figsize=fsize)
    vmin = -np.max(np.abs(cube_array))
    vmax = np.max(np.abs(cube_array))
    def animate(i):
        ax.clear()
        ax.contourf(cube_array[i, :, :], cmap=cmap, levels = np.linspace(scale*vmin,scale*vmax,20))
        ax.set_title("%03d" % (i))

    ani = animation.FuncAnimation(
        fig, animate, frames=cube_array.shape[0], interval=interval, blit=False
    )

    # plt.colorbar()
    if save == 0:
        plt.show()
    # else:
    # ani.save(output, writer="ffmpeg", fps=fps, dpi=160)


def AppendSave(str, array, file):
    """
    Appends a new variable (only one) to an existing .npz file. If one does not exist use np.savez(os.path.join(directory, OutputStr), varaible = variable)

    INPUT:
        str             : Name for appended data variable
        array           : Data to be appended to existing file,
        file            : String for filename and location of file to adjust.

    """

    data = np.load(file)
    data = dict(data)
    data[str] = array
    np.savez(file, **data)
    print(f"Data saved - {file}")


def draw_cicle(shape, diameter):
    """
    Input:
    shape    : tuple (height, width)
    diameter : scalar

    Output:
    np.array of shape  that has value 1 within a circle with diameter =  around center
    """
    assert len(shape) == 2
    TF = np.zeros(shape)  # ,dtype=np.bool)
    center = np.array(TF.shape) / 2.0
    XYRatio = shape[1] / shape[0]
    for iy in range(shape[0]):
        for ix in range(shape[1]):
            TF[iy, ix] = (int((iy - center[0]))) ** 2 + (int((ix - center[1])/XYRatio)) ** 2 < diameter**2
    TF = np.abs(TF - 1)
    return TF


def LowPass2D(Im, Circle, FiltStrength = 4):
    # 100, 5 for background lightsheet
    FFT1 = fft2(Im)
    FiltFFT = fftshift(FFT1)
    RemovedFFT = FiltFFT * Circle
    InvFFT = np.abs(ifft2(RemovedFFT))
    Subtracted = Im - InvFFT
    Guass = ndimage.gaussian_filter(Subtracted, FiltStrength)
    return Guass


def FlipArrayVert(u, v):
    """
    Rotates velocity fields for u and v
    INPUT:
        u           : 3D Numpy tensor containing velocity data
        v           : 3D Numpy tensor containing velocity data

    OUTPUT:
        u           : 3D Numpy tensor containing velocity data, flipped vertically.
        v           : 3D Numpy tensor containing velocity data, flipped vertically.

    """
    u = np.flip(u, axis=1)
    v = -np.flip(v, axis=1)
    return u, v


def velocityTracking(u, v):
    """
    finding the location of the ring using velocity
    """
    uMax = np.zeros(u.shape[0])
    uMin = np.zeros(u.shape[0])
    for t in range(0, u.shape[0]):
        uMax[t] = np.argmax(u[t,int(u.shape[1]/2),:])
        uMin[t] = np.argmin(u[t,int(u.shape[1]/2),:])
    # f2, ax2 = plt.subplots(nrows=1, ncols=1)
    # ax2.plot(uMax)
    # ax2.plot(uMin)
    # plt.show()
    return uMax, uMin


def velocityPeakTracking(vort, l = 0):
    VortLocMax = np.zeros((vort.shape[0], 2))
    VortLocMin = np.zeros((vort.shape[0], 2))
    if l == 0:
        l = vort.shape[0]
    elif l > vort.shape[0]:
        l = vort.shape[0]
    for i in range(l):
    # for i in range(500,vort.shape[0]):
        color = cmap(float(i) / l)
        vortTemp = vort[i, :, :]
        VortLocMax[i,:] = np.argwhere(vortTemp == np.max(vortTemp))
        VortLocMin[i,:] = np.argwhere(vortTemp == np.min(vortTemp))
        plt.scatter(VortLocMax[i,1], VortLocMax[i,0], color = color)
        plt.scatter(VortLocMin[i,1], VortLocMin[i,0], color = color)        
    plt.show()


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
    u, v = FlipArrayVert(u, v)
    return u, v


def importData(dir):
    """
    loads matlab data from a .MAT file. Crucially the variables loaded in the file are 'u_filtered', 'v_filtered', and 'vorticity'.

    INPUT:
        dir         : Full path of file to be opened, must include file extension.

    OUTPUT:
        u           : 3D Numpy tensor containing velocity data, has not been scaled.
        v           : 3D Numpy tensor containing velocity data, has not been scaled.
        vort        : 3D Numpy tensor containing vorticity data, has not been scaled.
    """

    os.chdir(os.path.dirname(dir))
    mat_contents = io.loadmat(os.path.basename(dir))
    u_temp = np.squeeze(mat_contents["u_filtered"])
    print(u_temp.shape)
    v_temp = np.squeeze(mat_contents["v_filtered"])
    # vort_temp = np.squeeze(mat_contents["vorticity"])
    u = np.empty((u_temp.shape[0], u_temp[0].shape[0], u_temp[0].shape[1]))
    print(u_temp[0].shape[0])
    for i in range(u.shape[0]):
    # for i in range(1499):
        u[i] = u_temp[i]
    v = np.empty((v_temp.shape[0], v_temp[0].shape[0], v_temp[0].shape[1]))
    for i in range(v.shape[0]):
    # for i in range(1499):
        v[i] = v_temp[i]
    print(str("Filtered Data Imported  -  " + str(u.shape)))
    u, v = FlipArrayVert(u, v)

    # vorticity = np.empty((vort_temp.shape[0], vort_temp[0].shape[0], vort_temp[0].shape[1]))
    # for i in range(vorticity.shape[0]):
    #     vorticity[i] = vort_temp[i]

    return u, v, #vorticity


def importVorticity(dir):
    """
    loads matlab data from a .MAT file. Crucially the variables loaded in the file are 'u_filtered', 'v_filtered', and 'vorticity'.

    INPUT:
        dir         : Full path of file to be opened, must include file extension.

    OUTPUT:
        vort        : 3D Numpy tensor containing vorticity data, has not been scaled.
    """

    os.chdir(os.path.dirname(dir))
    mat_contents = io.loadmat(os.path.basename(dir))
    vort_temp = np.squeeze(mat_contents["vorticity"])
    vorticity = np.empty((vort_temp.shape[0], vort_temp[0].shape[0], vort_temp[0].shape[1]))
    for i in range(vorticity.shape[0]):
        vorticity[i] = vort_temp[i]
    print(str("Filtered Data Imported  -  " + str(vorticity.shape)))

    return vorticity


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


def calculate_vorticity(u, v):
    """
    calculates vorticity of velocity field
     
    INPUT:
        u           : 3D Numpy tensor containing velocity data
        v           : 3D Numpy tensor containing velocity data

    OUTPUT:
        Vorticity   : 3D Numpy tensor containing velocity data
        vorticity_gauss : 3D Numpy tensor containing velocity data after a gausian filter

    """
    dv = np.gradient(v, axis = 2)
    du = np.gradient(u, axis = 1)
    vorticity = dv - du
    vorticity_gauss = gaussian_filter(vorticity, sigma = 0.7)
    return vorticity, vorticity_gauss


def vorticity_animation(u, v): 
    """
    calculates vorticity of velocity field

    INPUT:
        u           : 3D Numpy tensor containing velocity data
        v           : 3D Numpy tensor containing velocity data

    OUTPUT:
        Vorticity   : 3D Numpy tensor containing velocity data
        vorticity_gauss : 3D Numpy tensor containing velocity data after a gausian filter

    """
    dv = np.gradient(v, axis = 2)
    du = np.gradient(u, axis = 1)
    
    vorticity = dv - du
    vorticity_gauss = gaussian_filter(vorticity, sigma = 0.7)

    fig3, (ax3 , ax4)= plt.subplots(nrows=2, ncols=1)
    ax3.contourf(vorticity[100,:,:])
    ax4.contourf(vorticity_gauss[100,:,:])
    plt.show()

    plt.figure()
    plt.ion()
    for i in range(vorticity.shape[0]):
        print(i)
        plt.contourf(vorticity_gauss[i,:,:])
        plt.pause(0.01)


def vorticityPeakTracking(u, v, l = 0):
    vorticity, vort_gauss = calculate_vorticity(u, v)
    VortLocMax = np.zeros((vort_gauss.shape[0], 2)) #same length in time as vorticity field, 2 rows - 0 for y, 1 for x
    VortLocMin = np.zeros((vort_gauss.shape[0], 2)) #same length in time as vorticity field, 2 rows - 0 for y, 1 for x
    
    if l == 0:
        l = vort_gauss.shape[0]
    elif l > vort_gauss.shape[0]:
        l = vort_gauss.shape[0]
    
    for i in range(l):
    # for i in range(150, 1200):
        vortTemp = vort_gauss[i, :, :]
        VortLocMax[i,:] = np.argwhere(vortTemp == np.max(vortTemp))
        VortLocMin[i,:] = np.argwhere(vortTemp == np.min(vortTemp))

    # f1, (ax1) = plt.subplots(nrows=1, ncols=1)
    # ax1.scatter(VortLocMax[:, 1], VortLocMax[:, 0])
    # ax1.scatter(VortLocMin[:, 1], VortLocMin[:, 0])

    # # Ploting a midline
    # midline = np.zeros(vort_gauss.shape[0])
    # midline[:] = vort_gauss.shape[1]/2
    # ax1.plot(midline[0:vort_gauss.shape[2]])
    # plt.show()

    return VortLocMax, VortLocMin


    #calculating tilt

    # delta_y = np.zeros((gauss.shape[0], 2))
    # delta_x = np.zeros((gauss.shape[0], 2))

    # delta_y = VortLocMax[:, 0] - VortLocMin[:, 0]
    # delta_x = VortLocMax[:, 1] - VortLocMin[:, 1]

    # # print(delta_y)
    # # print(delta_x)

    # tilt = np.arctan(abs(delta_y / delta_x))
    # print(tilt)
    # f1, (ax2) = plt.subplots(nrows=1, ncols=1)
    # ax2.plot(tilt)
    # plt.show()


def vorticityPeakTracking_i(u, v, l = 0, n = 0):
    vorticity, vort_gauss = calculate_vorticity(u, v)
    VortLocMax_i = np.zeros((n, vort_gauss.shape[0], 2)) #same length in time as vorticity field, 2 rows - 0 for y, 1 for x
    VortLocMin_i = np.zeros((n, vort_gauss.shape[0], 2)) #same length in time as vorticity field, 2 rows - 0 for y, 1 for x
    Core_gradient = np.zeros((vort_gauss.shape[0], 2)) # not working yet

    if l == 0:
        l = vort_gauss.shape[0]
    elif l > vort_gauss.shape[0]:
        l = vort_gauss.shape[0]
    
    for j in range(n):
        for i in range(l):
        # for i in range(150, 1200):
            vortTemp = vort_gauss[i, :, :]
            VortLocMax_i[ i,:] = np.argwhere(vortTemp == np.max(vortTemp))
            VortLocMin_i[j, i,:] = np.argwhere(vortTemp == np.min(vortTemp))

    # f1, (ax1) = plt.subplots(nrows=1, ncols=1)
    # ax1.scatter(VortLocMax[:, 1], VortLocMax[:, 0])
    # ax1.scatter(VortLocMin[:, 1], VortLocMin[:, 0])

    # # Ploting a midline
    # midline = np.zeros(vort_gauss.shape[0])
    # midline[:] = vort_gauss.shape[1]/2
    # ax1.plot(midline[0:vort_gauss.shape[2]])
    # plt.show()

    return VortLocMax_i, VortLocMin_i


def PlotVelocity(u, v, frame):
    V = u + v
    print(V.shape)
    f1, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.contourf(V[frame,:,:])
    plt.show()   


def IWFilter(inputArray, input_ang, fps, rpm, forcedFreq = 0):
    """
    FFT filter for inertial wave frequency.
    
    Parameters
    ----------
    inputArray : array
        3D Array to be filtered.

    input_ang : int

    fps : int

    rpm : int

    Returns
    -------
    v_postFFT : array
        3D output array of filtered data.  

    """
    v_fluc = inputArray.copy()
    v1 = np.mean(v_fluc, axis=0)
    v_fluc -= v1
    if forcedFreq == 0:
        filtfreq = FiltFreqCalc(input_ang,fps=fps,rpm=rpm)
    else:
        filtfreq = forcedFreq
    
    print(f'Filter Frequency = {np.round(filtfreq, 4)}Hz')

    thresh = 0.03
    # thresh = 0.09
    # thresh = 0.1

    v_FFT = fft(v_fluc, axis=0)
    FFTFreq = fftfreq(v_fluc.shape[0], 1 / fps)
    
    mask1 = np.where(np.logical_and(filtfreq-thresh<FFTFreq, filtfreq+thresh>FFTFreq))
    mask2 = np.where(np.logical_and(-filtfreq-thresh<FFTFreq, -filtfreq+thresh>FFTFreq))
    
    window1 = np.zeros_like(FFTFreq)
    window1[mask1] = 1
    width = np.sum(window1)
    window1[mask1] = np.hanning(width)
    
    window2 = np.zeros_like(FFTFreq)
    window2[mask2] = 1
    window2[mask2] = np.hanning(width)

    windowT = window1 + window2

    v_FFT = v_FFT*windowT[:, None, None]

    v = ifft(v_FFT, axis=0)
    v_postFFT = np.real(v)

    return v_postFFT


def FiltFreqCalc(angle, fps, rpm):
    """
    Calculates the Inertial wave oscillation frequency using given parameters. 
    
    Parameters
    ----------
    angle : int

    fps : int

    rpm : int

    Returns
    -------
    filt_freq : float
        Frequency in Hz. 

    """
    f_omega = (rpm/60)
    ang = np.cos(np.deg2rad(angle))
    filt_freq = 2*f_omega*ang

    return filt_freq


def quivPlot(u, v):
    quiv, ax = plt.subplots(constrained_layout=True)
    uM = u
    vM = v
    mag = np.sqrt(uM**2 + vM**2)
    vmax = np.amax(vM)
    ax.contourf(mag)
    quiver = ax.quiver(uM, vM, pivot="middle")
    quiv.colorbar(
        plt.cm.ScalarMappable(),
        shrink=0.8,
        label="Axial Velocity (m/s)",
    )
    # cbar.set_label('Velocity (m/s)')
    # quiv.title('Contour / Quiver showing u, v')
    ax.set_xlabel("x Location")
    ax.set_ylabel("y Location")
    plt.show()


def progressBar(step,nSteps, width=40):

    percent = int(np.ceil(step*100/nSteps))

    left = width * percent // 100
    right = width - left
    
    tags = "#" * left
    spaces = " " * right
    percents = f"{percent:.0f}%"
    
    print("\r[", tags, spaces, "]", percents, sep="", end="", flush=True)


def NDUnitsForPlotsWide(shapeX, shapeY, widthM = 0.66, HeightM = 1.066, jetLocPix = 600, pixX = 1200, d = 0.05):
    """
    shapeX becomes Radial
    shapeY becomes Z
    """
    shapeX = shapeX -1
    zeroPos = int(jetLocPix/pixX * shapeX)

    r = np.linspace(-widthM * zeroPos/shapeX, widthM * (shapeX-zeroPos)/shapeX, shapeX+1)
    r_nd = r / d

    z = np.linspace(0, HeightM, shapeY)
    z_nd = z / d

    return r_nd, z_nd


def NDUnitsForPlotsNozzle(shapeX, shapeY, widthM = 0.13574, HeightM = 0.21719, jetLocPix = 600, pixX = 1200, d = 0.05):
    """
    shapeX becomes Radial
    shapeY becomes Z
    """
    shapeX = shapeX -1
    zeroPos = int(jetLocPix/pixX * shapeX)

    r = np.linspace(-widthM * zeroPos/shapeX, widthM * (shapeX-zeroPos)/shapeX, shapeX+1)
    r_nd = r / d

    z = np.linspace(0, HeightM, shapeY)
    z_nd = z / d

    return r_nd, z_nd


def InterpZeros(y):
    if (y==0).any() == True:
        y = np.array(y)
        x = np.arange(y.shape[0])
        idx = np.nonzero(y)
        f = interpolate.interp1d(x[idx], y[idx], fill_value="extrapolate" )
        ynew = f(x)
    else:
        ynew = y
    return ynew


def FilterSpikes(inputArray, deviation = 50):
    diffArray = np.diff(inputArray)
    inputArray[1:] = np.where(diffArray>deviation,0,inputArray[1:])
    inputArray = InterpZeros(inputArray)
    return inputArray


def animate_cube_contourf_points(
    cube_array, VortLocMax, VortLocMin, interval=17, cmap="seismic", save=0, output="points2.mp4", fps=60, scale = 1, fsize = (10, 8), 
):

    """
    animates a numpy 3D Array for quick visualisation (specific to contourf). This function animates the vorticity field with points indicating 
    max and min vorticity.

    INPUT:
        cube_array  : name of 3D numpy array that needs to be animated.
        interval    : #of ms between each frame.
        cmap        : colormap. Default='bwr'

    OUTPUT:
        animated window going through the cube.

    """
    print("Start")
    fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize=fsize, sharex = True, sharey = True)
    vmin = -np.max(np.abs(cube_array))
    vmax = np.max(np.abs(cube_array))
    def animate(i):
        ax1.clear()
        ax1.contourf(cube_array[i, :, :], cmap=cmap, levels = np.linspace(scale*vmin,scale*vmax,20))
        ax1.scatter(VortLocMax[i,1],VortLocMax[i,0], label = "Max Vorticity", color = "k")
        ax1.scatter(VortLocMin[i,1],VortLocMin[i,0], label = "Min Vorticity", color = "w")
        x1, x2 = VortLocMax[i,1], VortLocMin[i,1]
        y1, y2 = VortLocMax[i,0], VortLocMin[i,0]
        ax1.plot([x1,x2],[y1,y2], "g--", linewidth=2.0)
        ax1.set_title("%03d" % (i))
    print("2")
    anim = animation.FuncAnimation(
        fig, animate, frames=cube_array.shape[0], interval=interval, blit=False
    )

    if save == 0:
        plt.show()
    # else:
    #     print("save loop")
    #     anim.save(output, writer="ffmpeg", fps=fps, dpi=160)

    # writervideo = animation.FFMpegWriter(fps=60)
    # anim.save(output, writer=writervideo, dpi=160)

    # anim.save(output, writer="ffmpeg", fps=fps, dpi=160)


def load():
    global dirRoot, mtx, dist, short, FileListTop, FileListBot, number, n 
    Port = 'F'
    short = 1
    dirRoot = "F:/1.Experiments/RPM-30__Pump-10/2022-09-08__FPS-30/1"

    mtx, dist = oj.load_coefficients(f'{Port}:/1. Calibration files/07-03-23/calibration_chessboard.yml')
    # mtxB, distB = sb.load_coefficients(f'{Port}:/.EXPERIMENTS/Calibration Files/22-09-01/CalB/calibration_chessboard.yml')
    # mtxT, distT = sb.load_coefficients('F:/2.Calibration Files/22-05-12/calibration_chessboard.yml')

    dirTop = str(dirRoot + "/T/*")
    dirBot = str(dirRoot + "/B/*")
    chars = len(os.listdir(str(dirTop)[:-1])[0])

    if chars > 12:
        oj.renameFiles(str(dirTop)[:-1])
        oj.renameFiles(str(dirBot)[:-1])
        print("Files Renamed")
    else:
        pass

    FileListTop = sorted(glob.glob(dirTop))
    FileListBot = sorted(glob.glob(dirBot))
    # Define cropping size
    n = 55

    number = list(range(0, len(FileListBot) - 2))


def process_image(number):
    top = cv2.imread(FileListTop[number])
    dstTop = cv2.undistort(top, mtx, dist, None, None)[:-n, :]
    bottom = cv2.imread(FileListBot[number+2])
    dstBottom = cv2.undistort(bottom, mtx, dist, None, None)[n:, :] 
    merged = cv2.vconcat([dstTop, dstBottom]) #[top,bottom])
    numPad = str(number)
    numPad = numPad.zfill(5)
    cv2.imwrite(str(dirRoot + f"/M/Image_{numPad}.tiff"), merged)
    if short == 1:
        if number % 60 == 0:
            cv2.imwrite(str(dirRoot + f'/Short/{str(int(numPad/60))}.tiff'), merged)
        else:
            pass
    else:
        pass
    print(f"done     file: {number}")


if __name__ == "__main__":
    load()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_image, number)


def renameFiles(dir):
    """
    loads .tiff images from a directory and changes their name to '00001.tiff' The number is detected by looking for a dash in the filename

    INPUT:
        dir         : Directory of files to open, must end in *. e.g. \Images\*

    """
    listFiles = sorted(os.listdir(dir))
    length = len(listFiles)

    for i in range(0, length):  # length
        fileOld = os.path.join(dir, listFiles[i])
        Position = int(str(listFiles[i]).rfind("-")) + 1
        Number = str(listFiles[i])[Position:-5]
        NumPad = Number.zfill(5)
        FnNew = str(NumPad + ".tiff")
        fileNew = os.path.join(dir, FnNew)
        os.rename(fileOld, fileNew)


def save_coefficients(mtx, dist, path):
    """Save the camera matrix and the distortion coefficients to given path/file."""
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write("K", mtx)
    cv_file.write("D", dist)
    # note you *release* you don't close() a FileStorage object
    cv_file.release()


def load_coefficients(path):
    """Loads camera matrix and distortion coefficients."""
    # FILE_STORAGE_READ
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]


def sum_kinetic_energy(u, v):
    V = np.sqrt((abs(u))**2 + (abs(v))**2)
    kinetic_energy = np.square(V)
    sum_kinetic_energy = np.sum(kinetic_energy, axis=(1,2))
    # print(sum_kinetic_energy.shape)
    return kinetic_energy, sum_kinetic_energy


def frames_to_seconds(u, v, FPS = 60, ):
    """for plotting in seconds"""
    data_length = u.shape[0]   # 10 seconds of data at 60Hz
    sample_rate = 60   # FPS

    # calculate the time step
    time_step = 1/sample_rate

    # create the time series
    time = np.arange(0, data_length*time_step, time_step)
    return time


def animate_cube_quiver( 
    u, v, interval=16.7, cmap="bwr", save=0, output="15.mp4", fps=60, scale = 1, fsize = (10, 8)
):

    """
    animates a numpy 3D Array for quick visualisation (specific to quiver plot).

    INPUT:
        cube_array  : name of 3D numpy array that needs to be animated.
        interval    : no. of ms between each frame.
        cmap        : colormap. Default='bwr'

    OUTPUT:
        animated window going through the cube.

    """

    x, y = np.meshgrid(np.arange(0, 119, 1), np.arange(0, 74, 1))
    V = np.sqrt((abs(u**2) + abs(v**2)))

    fig, ax = plt.subplots(figsize=fsize)
    vmin = -np.max(np.abs(V))
    vmax = np.max(np.abs(V))
    def animate(i):
        ax.clear()
        ax.contourf(u[i, :, :], cmap=cmap, levels = np.linspace(scale*vmin,scale*vmax,20))
        # u = [i,:,:]
        # v = [i,:,:]
        ax.quiver(x, y, u[i,:,:], v[i,:,:], pivot="middle")
        ax.set_title("%03d" % (i))

    ani = animation.FuncAnimation(
        fig, animate, frames=V.shape[0], interval=interval, blit=False
    )

    # plt.colorbar()
    if save == 0:
        plt.show()
    # else:
    # ani.save(output, writer="ffmpeg", fps=fps, dpi=160)


def sum_Vorticity(
    u, v, l = 0
):
    vorticity, vorticity_gauss = calculate_vorticity(u, v)
    sumVorticity = np.zeros((u.shape[0]))


    if l == 0:
        l = vorticity.shape[0]
    elif l > vorticity.shape[0]:
        l = vorticity.shape[0]

    for i in range(l):
        vortTemp = vorticity[i, :, :]
        sumVorticity[i] = np.sum(abs(vorticity[i, :, :]))
    return sumVorticity


def sum_Enstrophy(
    u, v, l = 0        
):
    vorticity, vorticity_gauss = calculate_vorticity(u, v)
    sumEnstrophy = np.zeros((u.shape[0]))


    if l == 0:
        l = vorticity.shape[0]
    elif l > vorticity.shape[0]:
        l = vorticity.shape[0]

    for i in range(l):
        vortTemp = vorticity[i, :, :]
        sumEnstrophy[i] = np.sum((vorticity[i, :, :]**2))
    return sumEnstrophy






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