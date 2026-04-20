import os
import json

from nltk.corpus import reuters
from collections import Counter

from utils import splitter, variant_joiner

counts = Counter(reuters.words())
common_words = counts.most_common(n=100)
language_model = Counter()
for word, count in common_words:
  language_model[word] = count

primus = ['F','U','TH','O','R','C-K','G','W','H','N','I','J','EO','P','X','S-Z','T','B','E','M','L','NG-ING','OE','D','A','AE','Y','IA-IO','EA']
split_chars = ['C-K','S-Z','NG-ING','IA-IO']
chapters = [[0, 1, 2], [3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14], [15, 16, 17, 18, 19, 20, 21, 22], [23, 24, 25, 26], [27, 28, 29, 30, 31, 32], [33, 34, 35, 36, 37, 38, 39], [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55], [56], [57]]
CHAR_BY_FREQ = 'ETAOINSRHDLUCMFYWGPBVKXQJZ'

# word_counts = []
# for chapter in chapters:

#   for page in chapter:
#     print("processing page", page)
#     for idx in range(len(primus)):
#       shifted_primus = list(reversed(primus[idx:] + primus[:idx]))
#       mapping = {}
#       for char, new_char in zip(primus, shifted_primus):
#         mapping[char] = new_char
#       words = []
#       with open(os.path.join('transcripts', str(page) + '.json')) as f:
#         data = json.load(f)
#         unsplit = list(splitter(data))
#         # print(data)
#         new_data = []
#         for item in data:
#           if item not in [' ', '.', ';']:
#             new_data.append(mapping[item])
#           else:
#             new_data.append(item)
#         # print(new_data)
#         word_chars = list(splitter(new_data))
#         for char_set in word_chars:
#           word_variants = list(variant_joiner(char_set))
#           words.extend(word_variants)
#       score = 0
#       found_words = []
#       for word in words:
#         if len(word) > 2 and word in language_model:
#           score += language_model[word]
#           found_words.append(word)
#           # print(word, end=" ")
#       # print("\nScore:", score)
#       score_normalized = float(score)/len(unsplit)
#       if score_normalized > 10:
#         print("\nScore:", score)
#         print(words)
#         print(found_words)
#         print(idx)

# # iterate over all pages
# for root, dirs, files in os.walk('transcripts'):
#   for file in files:
#     print(root)
#     print(file)
#     with open(os.path.join(root, file)) as f:
#       data = json.load(f)
#     len_two_words = []
#     for word in splitter(data, [' ', '.', ';']):
#       if len(word) == 2:
#         len_two_words.append(word)
#     print(len_two_words)

#     chapter = chapter_mapping[int(file[:-5])]

with open(os.path.join('transcripts', 'starting_chars.json')) as f:
  data = json.load(f)
print(len(data))

word_counts = []
for chapter in chapters:
  words = Counter()
  for page in chapter:
    print("processing page", page)
    with open(os.path.join('transcripts', str(page) + '.json')) as f:
      data = json.load(f)
      word_chars = list(splitter(data))
      for char_set in word_chars:
        if char_set:
          words.update([''.join(char_set)])
  print(words)


  # char_mapping = {}
  # for key, value in zip(alphabet, list(CHAR_BY_FREQ)):
  #   char_mapping[key] = value
    # new_words = []
    # for word in words:
    #   new_word = []
    #   for char in word:
    #     new_word.append(char_mapping[char])
    #   new_words.append(''.join(new_word))
    # print(new_words)