import copy


def splitter(transcript, splitters=[' ', ';', '.']):
  # split list of chars by splitters
  # returns a list of lists
  # each sublist is a word's characters
  word = []
  for char in transcript:
    if char in splitters:
      yield word
      word = []
    else:
      word.append(char)


def variant_joiner(chars):
  # generate word variants using - separated options
  # returns a list of strings
  word_variants = [[]]
  for char in chars:
    if '-' in char:
      new_variants = copy.deepcopy(word_variants)
      char_1, char_2 = char.split('-')
      for word_variant in word_variants:
        word_variant.append(char_1)
      for word_variant in new_variants:
        word_variant.append(char_2)
      word_variants.extend(new_variants)
    else:
      for word_variant in word_variants:
        word_variant.append(char)
  for word_variant in word_variants:
    yield ''.join(word_variant)


def create_transcript(page_num, char_mapping=None):  
  # convert a page's list of chars to a transcript with inline variants
  # returns a list of strings
  words = []
  with open(os.path.join('transcripts', str(page_num) + '.json')) as f:
    data = json.load(f)
    if char_mapping:
      for i, char in enumerate(data):
        data[i] = char_mapping[char]
    word_chars = list(splitter(data))
    for char_set in word_chars:
      if char_set:
        word_variants = list(variant_joiner(char_set))
        words.extend(word_variants)
  return words