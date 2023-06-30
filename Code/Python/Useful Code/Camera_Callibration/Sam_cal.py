import numpy as np
import os
import sys
import mat73
import glob
import cv2 as cv

#####Import Ollie Tools
dirPath = "C:/Coding"
sys.path.insert(0, dirPath)
import OllieTools as oj
print(dirPath)

# Parameters
IMAGES_DIR = 'G:/Testing/Calibration files/Callibration_images'
IMAGES_FORMAT = 'tiff'
SQUARE_SIZE = 1
WIDTH = 13
HEIGHT = 9

# Calibrate 
ret, mtx, dist, rvecs, tvecs = oj.calibrate_chessboard2(
    IMAGES_DIR, 
    IMAGES_FORMAT, 
    SQUARE_SIZE, 
    WIDTH, 
    HEIGHT
)
print("cal complete")

# Save coefficients into a file
# oj.save_coefficients(mtx, dist, str(IMAGES_DIR+"calibration_chessboard.yml"))
oj.save_coefficients(mtx, dist, "G:/Testing/Calibration files/Callibration_images/calibration_chessboard.yml")
print("saving complete")