import glob
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import concurrent.futures
import cv2
import time
import os
import sys


#### CODE FROM SAM THAT APPPLIES CALLIBRATION TO IMAGES ####


#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

def load():
    global dirRoot, mtx, dist, FileListTop, number
    Port = 'G'
    dirRoot = "G:/Testing/Calibration files/Test_call/1" #### Whatever file contains the images to undistort

    mtx, dist = oj.load_coefficients(f'G:/Testing/Calibration files/Callibration_imagescalibration_chessboard.yml')

    dirTop = str(dirRoot + "/B/*")
    chars = len(os.listdir(str(dirTop)[:-1])[0])

    # if chars > 12:
    #     oj.renameFiles(str(dirTop)[:-1])
    #     print("Files Renamed")
    # else:
    #     pass

    FileListTop = sorted(glob.glob(dirTop))

    number = list(range(0, len(FileListTop)))

def process_image(number):
    Im = cv2.imread(FileListTop[number])
    UndistIm = cv2.undistort(Im, mtx, dist, None, None)
    numPad = str(number)
    numPad = numPad.zfill(5)
    cv2.imwrite(str(dirRoot + f"/M/Image_{numPad}.tiff"), UndistIm)
    print(f"done     file: {number}")

if __name__ == "__main__":
    load()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_image, number)
