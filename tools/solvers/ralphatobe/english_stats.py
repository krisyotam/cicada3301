import matplotlib.pyplot as plt

from nltk.corpus import reuters
from collections import Counter


primus = ['F','U','TH','O','R','C-K','G','W','H','N','I','J','EO','P','X','S-Z','T','B','E','M','L','NG-ING','OE','D','A','AE','Y','IA-IO','EA']

# construct a character tree from the gematria primus
char_tree = {}
for cipher_item in primus:
  for cipher_char in cipher_item.split('-'):
    head = cipher_char[0]
    if len(cipher_char) > 1:
      tail = cipher_char[1:]
      if head in char_tree.keys():
        char_tree[head].append(tail)
      else:
        char_tree[head] = [tail]
    else:
      if head not in char_tree.keys():
        char_tree[head] = []

print(char_tree)


# consume reuters dataset to find english distribution of primus chars
cipher_counts = Counter()
for word in reuters.words():
  word = list(word.upper())
  while word:
    head = word.pop(0)
    if head in char_tree.keys():
      # print("valid character:", head)
      tail = ''
      for tail in char_tree[head]:
        if word[:len(tail)] == list(tail):
          # print("valid tail:", tail)
          for char in tail:
            word.pop(0)
          break
        else:
          tail = ''
      cipher_counts.update([head + tail])

print(cipher_counts)


# display bar graph of english primus character distribution
primus_counts = Counter()
for cipher_item in primus:
  count = 0
  for cipher_char in cipher_item.split('-'):
    count += cipher_counts[cipher_char]
  primus_counts[cipher_item] = count
  
primus, primus_counts = zip(*primus_counts.most_common())

plt.bar(range(len(primus_counts)), primus_counts)
plt.xticks(range(len(primus)), primus)
plt.show()
  