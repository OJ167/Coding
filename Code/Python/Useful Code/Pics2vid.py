import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import glob
import cv2


import os
import sys

dirPath = os.getcwd()
sys.path.insert(0, dirPath)
import OllieTools as oj

dir = 'F:\Warwick Work/vids for conf/test/*'

def loadImages(dir, n=1, clip=0):
    """
    loads .tiff images from a directory to a returned numpy array. Also applies a CLAHE filter to the images.

    INPUT:
        dir         : Directory of files to open, must end in *. e.g. \Images\*
        n           : Optional. Default value is 1. Reduces number images imported by selecting every nth image.
        clip        : Optional. Default is 0. Will stop importing at the number of images in directory determined by this value.

    OUTPUT:
        Array       : 3D Numpy tensor containing image data as pixel intensity.

    """
    FileList = sorted(glob.glob(dir))
    print( f'{dir} - Images detected {len(FileList)}')

    if clip == 0:
        length = int(np.floor(len(FileList) / n))
    else:
        length = int(np.floor(clip / n))
    Im0 = np.array(cv2.imread(FileList[0], 0))
    Array = np.zeros((Im0.shape[0], Im0.shape[1], length))
    clahe = cv2.createCLAHE(clipLimit=10)  #
    for i in range(0, length):
        Array[:, :, i] = np.array((clahe.apply(cv2.imread(FileList[n * i], 0))))
    return Array

def animate_cube_images(
    cube_array, cut=True, interval=75, cmap="gray", save=0, output="output.mp4", fps=12
):

    """
    animates a numpy 3D Array for quick visualisation (specific to images).

    INPUT:
        cube_array  : name of 3D numpy array that needs to be animated.
        cut         : trims pixels off of the images edge to remove edge detector effects.
                      Default = True as 0 returns empty array.
        interval    : #of ms between each frame.
        cmap        : colormap. Default='gray'

    OUTPUT:
        animated window going through the cube.

    """

    fig = plt.figure(figsize=(10, 8))

    img = plt.imshow(
        cube_array[cut:-cut, cut:-cut, 0], animated=True, cmap=cmap
    )  # vmax=mean+3*std, vmin=mean-3*std,

    def updatefig(i):
        img.set_data(cube_array[cut:-cut, cut:-cut, i])
        return (img,)

    ani = animation.FuncAnimation(
        fig, updatefig, frames=cube_array.shape[2], interval=interval, blit=True
    )
    # plt.colorbar()
    if save == 0:
        plt.show()
    else:
        ani.save(output, writer="ffmpeg", fps=fps, dpi=160)


Array = loadImages(dir)

animate_cube_images(Array)
