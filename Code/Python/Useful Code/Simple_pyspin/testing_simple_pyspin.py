
from simple_pyspin import Camera
from PIL import Image
import os


frames = 10 #number of frames to be captured

with Camera() as cam: # Initialize Camera
    cam.start() # Start recording
    imgs = [cam.get_array() for n in range(frames)]
    cam.stop() # Stop recording

# Make a directory to save some images
output_dir = 'F:\Testing'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Saving images to: %s" % output_dir)

# Save them
# NOTE: images may be very dark or bright, depending on the camera lens and
#   room conditions!
for n, img in enumerate(imgs):
    Image.fromarray(img).save(os.path.join(output_dir, '%08d.png' % n))