import os
import json
import matplotlib

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def priotize_chars(high_priority, low_priority, char2centers):
  if high_priority in char2centers.keys() and low_priority in char2centers.keys():
    # read higher priority image and extract character size
    img = cv.imread(os.path.join('cropped vocabulary', high_priority + '.png'), 0)
    height, width = img.shape
    remove = []
    for y, x in char2centers[high_priority]:
      for j, i in char2centers[low_priority]:
        # if characters overlap, collect lower priority character index
        if i < x + width/2 and i > x - width/2 and \
           j < y + height/2 and j > y - height/2:
           remove.append((j, i))
      # remove targeted low priority characters
      for y, x in remove:
        char2centers[low_priority].remove((y, x))
      remove = []
  return char2centers


def find_blob(indices, x, y, x_sum, y_sum):
  # recursively find centroid of connected hit pixels
  if (x, y) in indices:
    x_sum += x
    y_sum += y
    indices.remove((x, y))
    indices, x_sum, y_sum = find_blob(indices, x + 1, y, x_sum, y_sum)
    indices, x_sum, y_sum = find_blob(indices, x, y + 1, x_sum, y_sum)
    indices, x_sum, y_sum = find_blob(indices, x - 1, y, x_sum, y_sum)
    indices, x_sum, y_sum = find_blob(indices, x, y - 1, x_sum, y_sum)
  return indices, x_sum, y_sum


def dbscan(points, eps, min_pts):
  cluster = 0
  labels = np.empty_like(points)
  labels[:] = np.nan
  for idx, point in np.ndenumerate(points):
    if not np.isnan(labels[idx]):
      continue
    neighbors = get_neighbors(points, eps, point)
    if len(neighbors) < min_pts:
      labels[idx] = np.inf
      continue
    labels[idx] = cluster
    for neighbor in neighbors:
      if np.isinf(labels[neighbor]):
        labels[neighbor] = cluster
      if not np.isnan(labels[neighbor]):
        continue
      labels[neighbor] = cluster
      new_neighbors = get_neighbors(points, eps, points[neighbor])
      if len(neighbors) >= min_pts:
        neighbors.extend(new_neighbors)
    cluster += 1
  return labels

def get_neighbors(points, eps, point):
  dists = np.abs(points - np.repeat(point, points.shape[0]))
  neighbors = np.argwhere(dists < eps)
  return neighbors.tolist()


# define kernels to use for hit-or-miss filter
kernel_3 = np.ones((3, 3), np.uint8)
diamond = [[0, 0, 1, 0, 0],
           [0, 1, 1, 1, 0],
           [1, 1, 1, 1, 1],
           [0, 1, 1, 1, 0],
           [0, 0, 1, 0, 0]]
kernel_5_d = np.array(diamond, np.uint8)
kernel_5 = np.ones((5, 5), np.uint8)
kernel_7 = np.ones((7, 7), np.uint8)

# define character hit custom dtype
dtype = [('y', int), ('x', int), ('char', object)]

# iterate over all pages
for page_root, dirs, page_files in os.walk('2014onion7'):
  for page_file in page_files:
    # if page_file[-4:] == '.jpg' and int(page_file[:-4]) > 4 and int(page_file[:-4]) < 10:
    if page_file[-4:] == '.jpg':
      num = page_file[:-4]
      print(page_file)
      # read and binarize page
      page = cv.imread(os.path.join(page_root, page_file), 0)
      ret, page = cv.threshold(page, 127, 255, cv.THRESH_BINARY)
      page = 255 - page

      # initialize variables
      # read_page = np.zeros_like(page, dtype='float64')
      all_chars = np.array([], dtype=dtype)

      # page_char = page/4

      # iterate over all characters
      for root, dirs, files in os.walk('cropped vocabulary'):
        for file in files:
          # extract character
          char, _ = file.split('.')
          # read and binarize character
          img = cv.imread(os.path.join(root, file), 0)
          ret, img = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
          img = 255 - img
          
          # erode the character to make sure it matches on the page
          img_erode_1 = cv.erode(img, kernel_3)
          if char == '1_dot':
            # create a character outline for the hit or miss filter
            img_erode_2 = cv.dilate(img, kernel_5) - cv.dilate(img, kernel_3)
            filter_page = page
          elif char == 'D':
            # create a character outline for the hit or miss filter
            img_erode_2 = img - cv.erode(img, kernel_3)
            filter_page = cv.erode(page, kernel_5)
            filter_page = cv.erode(filter_page, kernel_5_d)
          else:
            # create a character outline for the hit or miss filter
            img_erode_2 = img - cv.erode(img, kernel_3)
            filter_page = cv.erode(page, kernel_7)
          # run hit or miss filter
          page_erode_1 = cv.erode(page, img_erode_1, borderValue=0)
          page_erode_2 = cv.erode(255 - filter_page, img_erode_2, borderValue=0)
          page_erode = np.logical_and(page_erode_1, page_erode_2)
          page_erode = page_erode.astype(np.uint8) * 255

          # check if character is present in image
          if sum(sum(page_erode)) > 0:

            # permute kernel to make image look correct
            kernel = np.fliplr(np.flipud(img))

            # create structured array with char and index groups
            char_indices = np.argwhere(page_erode)
            data = []
            for coords in char_indices.tolist():
              coords.append(char)
              data.append(tuple(coords))
            found_chars = np.array(data, dtype=dtype)

            # update character hit variables
            # read_page += cv.dilate(page_erode, kernel)/2
            all_chars = np.concatenate((all_chars, found_chars))

      # create char to index dict without repeats
      char2idx = {}
      for x, y, char in all_chars:
        if char in char2idx.keys():
          char2idx[char].append((x, y))
        else:
          char2idx[char] = [(x, y)]

      # create char to blob center dict
      char2centers = {}
      for char, indices in char2idx.items():
        while indices:
          x, y = indices[0]
          num_idx = len(indices)
          # call find_blob to identify the sum of blobx and y coords
          indices, x_sum, y_sum = find_blob(indices, x, y, 0, 0)
          blob_size = num_idx - len(indices)
          # average blob x and y coords to find center
          x = x_sum / blob_size
          y = y_sum / blob_size
          # add new blob center to blob center dict
          if char in char2centers.keys():
            char2centers[char].append((x, y))
          else:
            char2centers[char] = [(x, y)]

      # omit subcharacter hits
      char2centers = priotize_chars('13_dots', '1_dot', char2centers)
      char2centers = priotize_chars('4_dots', '1_dot', char2centers)
      char2centers = priotize_chars('Y', 'U', char2centers)
      char2centers = priotize_chars('R', 'W', char2centers)
      char2centers = priotize_chars('R', 'L', char2centers)

      # extract prioitized characters back into structured array
      data = []
      keys = []
      x_coords = []
      y_coords = []
      for key, values in char2centers.items():
        for y, x in values:
          data.append((y, x, key))
          keys.append(key)
          x_coords.append((x))
          y_coords.append((y)) 

      # order characters top to bottom, left to right
      ordered_chars = np.array(data, dtype=dtype) 
      idx_transcript = np.sort(ordered_chars, order=['y', 'x'])
      print(idx_transcript)

      # extract character image shape
      y, x = img.shape

      # convert points to arrays
      x_points = np.array(x_coords)
      y_points = np.array(y_coords)

      # find x clusters
      x_labels = dbscan(x_points, x/2, 3)

      # remove x noise
      x_points = x_points[np.logical_not(np.isinf(x_labels))]
      y_points = y_points[np.logical_not(np.isinf(x_labels))]
      keys = [keys[int(i)] for i in np.argwhere(np.isinf(x_labels) == False)]

      # find y clusters
      y_labels = dbscan(y_points, y/2, 3)

      # remove y noise
      x_points = x_points[np.logical_not(np.isinf(y_labels))]
      y_points = y_points[np.logical_not(np.isinf(y_labels))]
      keys = [keys[int(i)] for i in np.argwhere(np.isinf(y_labels) == False)]
      y_labels = y_labels[np.logical_not(np.isinf(y_labels))]

      plt.scatter(y_points, np.zeros_like(y_points), c=y_labels)
      plt.show()

      exit()

      if len(keys) > 0:
        # fix line centroids for each cluster
        for cluster in range(int(np.max(y_labels)) + 1):
          indices = np.argwhere(y_labels == cluster)
          cluster_points = y_points[indices]
          line = np.mean(cluster_points)
          y_points[indices] = line

        # consolidate data
        data = []
        for idx, key in enumerate(keys):
          data.append((y_points[idx], x_points[idx], key))

        # order characters top to bottom, left to right
        ordered_chars = np.array(data, dtype=dtype) 
        idx_transcript = np.sort(ordered_chars, order=['y', 'x'])

        # replace dots with punctuation
        transcript = []
        for y, x, char in idx_transcript:
          if char == '1_dot':
            transcript.append(" ")
          elif char == '4_dots':
            transcript.append(".")
          elif char == '13_dots':
            transcript.append(";")
          else:
            transcript.append(char)

      else:
        transcript = []

      # check for transcript folder
      if not(os.path.exists('transcripts')):
        os.makedirs('transcripts')

      # write out transcript
      filepath = os.path.join('transcripts', page_file[:-4] + '.json')
      with open(filepath, 'w') as f:
        json.dump(transcript, f)
