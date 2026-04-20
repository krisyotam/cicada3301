import os
import cv2 as cv
import numpy as np
from scipy.misc import imsave

# make cropped image directory, if none
directory = 'cropped vocabulary'
if not os.path.exists(directory):
  os.makedirs(directory)

# iterate over all characters
for root, dirs, files in os.walk('vocabulary'):
  for file in files:
    # read and binarize character image
    char = cv.imread(os.path.join(root, file), 0)
    ret, char_bw = cv.threshold(char, 127, 255, cv.THRESH_BINARY)
    char_bw = 255 - char_bw

    # locate image bounds
    vals = np.nonzero(char_bw)
    bounds = [np.amin(vals[0]), np.amax(vals[0]), np.amin(vals[1]), np.amax(vals[1])]

    # crop and pad original image
    bounded_char = char[bounds[0]:bounds[1] + 1,bounds[2]:bounds[3] + 1]
    padded_char = np.pad(bounded_char, ((5, 5), (5, 5)), 'constant', 
                         constant_values=((255, 255), (255, 255)))

    # save padded char
    imsave(os.path.join(directory,file), padded_char)