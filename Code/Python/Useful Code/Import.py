from genericpath import exists
from shutil import copytree, ignore_patterns
import shutil
import os

# The purpose of this file is to copy experimental files from an external hard drive to an internal folder.
# 
# It will not copy image folders of .tiff file types of a any kind to reduce storage size on machine.
#
# WARNING! Will only copy folder internals if the day folder does not exist in the new drive 



source = 'E:/.EXPERIMENTS/Horizontal'
destination = 'C:/Experiments'

files = [file for file in os.listdir(source)] #if os.path.isfile(os.path.join(directorya, file))]
for file in files:
    if not os.path.exists(os.path.join(destination, file)):
        print('Copying...')
        shutil.copytree(os.path.join(source, file), os.path.join(destination, file), ignore = ignore_patterns('*.tif', 'Images*'))
    else:
        pass



print('Copying complete')
