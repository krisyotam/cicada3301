import os
import json

import matplotlib.pyplot as plt

from collections import Counter
from utils import splitter, variant_joiner


CHAPTERS = [[0, 1, 2], [3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14], [15, 16, 17, 18, 19, 20, 21, 22], [23, 24, 25, 26], [27, 28, 29, 30, 31, 32], [33, 34, 35, 36, 37, 38, 39], [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55], [56], [57]]


for chapter in CHAPTERS:
  unigrams = Counter()
  for page in chapter:
    print("processing page", page)
    chars = []
    with open(os.path.join('transcripts', str(page) + '.json')) as f:
      data = json.load(f)
      # # individual english character language stats
      # for char in data:
      #   if char not in [' ', '.', ';']:
      #     chars.extend(set(char) - set('-'))
        
      # cipher character set stats
      chars = [char for char in data if char not in [' ', '.', ';']]

    unigrams.update(chars)
  alphabet, alphabet_counts = zip(*unigrams.most_common())
  
  plt.bar(range(len(alphabet_counts)), alphabet_counts)
  plt.xticks(range(len(alphabet)), alphabet)
  plt.show()
  