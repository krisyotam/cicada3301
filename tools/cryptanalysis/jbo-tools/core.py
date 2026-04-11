import inspect
import string

class RuneUtils(object):
    """
        Utilities for rune handling.
    """

    # Runes latin etc.
    _RUNES = [ 'ᚠ', 'ᚢ', 'ᚦ', 'ᚩ', 'ᚱ', 'ᚳ', 'ᚷ', 'ᚹ', 'ᚻ', 'ᚾ', 'ᛁ', 'ᛄ', 'ᛇ', 'ᛈ', 'ᛉ', 'ᛋ', 'ᛏ', 'ᛒ', 'ᛖ', 'ᛗ', 'ᛚ', 'ᛝ', 'ᛟ', 'ᛞ', 'ᚪ', 'ᚫ', 'ᚣ', 'ᛡ', 'ᛠ' ]
    _LATIN = [ 'F', 'V', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA' ]
    _PUNCT = { '-': ' ', '.': '. ' }
    _GP_PRIMES = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109 ]

    @classmethod
    def size(cls):
        """
            Get the size of alphabet.
        """

        # Return size
        return len(cls._RUNES)

    @classmethod
    def iter_runes(cls):
        """
            Iterate all runes.
        """

        # Iterate runes
        return iter(cls._RUNES)

    @classmethod
    def rune_at(cls, index):
        """
            Returns the rune at a specific index.
        """

        # Return the rune
        return cls._RUNES[index % cls.size()]

    @classmethod
    def latin_at(cls, index):
        """
            Returns the Latin at a specific index.
        """

        # Returns the Latin
        return cls._LATIN[index % cls.size()]

    @classmethod
    def gp_at(cls, index):
        """
            Return the GP prime at a specific index.
        """

        # Returns the GP prime
        return cls._GP_PRIMES[index % cls.size()]

    @classmethod
    def is_rune(cls, rune):
        """
            Indicates if the given input is a rune or not.
        """

        # Indicate
        return rune in cls._RUNES

    @classmethod
    def is_punct(cls, candidate):
        """
            Indicates if the given input is a recognized punctuation.
        """

        # Indicate
        return candidate in cls._PUNCT

    @classmethod
    def get_rune_index(cls, rune):
        """
            Gets the given rune's index.
        """

        # Validations
        assert cls.is_rune(rune), Exception(f'Invalid rune: {rune}')
        return cls._RUNES.index(rune)

    @classmethod
    def runes_to_gp_sum(cls, runes):
        """
            Translates runes to a GP-sum, ignoring non-runes.
        """

        # Only take runes and translate
        return sum([ cls._GP_PRIMES[cls._RUNES.index(rune)] for rune in runes if rune in cls._RUNES ])

    @classmethod
    def runes_to_latin(cls, runes):
        """
            Turns runes to Latin.
        """

        # Only take runes into account and preserve spaces etc.
        return ProcessedText(rune_text=runes).to_latin()

    @classmethod
    def english_to_runes(cls, english):
        """
            Turns English ("true" English) to runes.
        """

        # Only take letters and turn everything uppercase
        s = ''.join([ i.upper() for i in english if i in string.ascii_letters ])

        # Certain Cicada3301 quirks
        s = s.replace('ING', 'NG')      # "BENG"
        s = s.replace('IO', 'IA')       # "INSTRVCTIAN"
        s = s.replace('QU', 'CW')       # "CWESTION"
        s = s.replace('K', 'C')         # "BOOC"
        s = s.replace('U', 'V')         # "OVR"
        s = s.replace('Z', 'S')         # Hypothesis
        s = s.replace('Q', 'C')         # Hypothesis

        # Try to minimize the number of runes by prioritizing runes that translate to two-letter latin
        for i in range(len(cls._RUNES)):
            if len(cls._LATIN[i]) == 1:
                continue
            s = s.replace(cls._LATIN[i], cls._RUNES[i])

        # Translate all the rest
        for i in range(cls.size()):
            s = s.replace(cls._LATIN[i], cls._RUNES[i])

        # Return result
        return s

    @classmethod
    def translate_punct(cls, c):
        """
            Translates punctuation.
        """

        # Return the translation or an empty string
        return cls._PUNCT.get(c, '')

class ProcessedText(object):

    # Save the runes
    _RUNES = list(RuneUtils.iter_runes())

    def __init__(self, rune_text=None, section=None):
        """
            Creates an instance.
        """

        # Saves the section
        self.section = section

        # Get the text
        if rune_text is None and section is None:
            raise Exception('Must supply either section or rune text')
        self._orig = section.get_all_text() if rune_text is None else rune_text

        # Save processes runes
        self._processed_runes = [ c for c in self._orig if RuneUtils.is_rune(c) ]
        self._orig_runes = self._processed_runes[:]

        # Currently not marked as unsolved
        self._is_unsolved = False

        # Cache for measurements
        self._measurements = None

    def revert(self):
        """
            Reverts all changes.
        """

        # Revert
        self._processed_runes = self._orig_runes[:]
        self._is_unsolved = False

    @staticmethod
    def from_processed_text(other):
        """
            Creates a new instance, "duplicating" the given instance.
        """

        # Duplicate
        pt = ProcessedText(other._orig)
        pt._processed_runes = other._processed_runes[:]
        pt._is_unsolved = other._is_unsolved
        pt.section = other.section
        return pt

    def set_unsolved(self):
        """
            Sets as unsolved.
        """

        # Mark
        self._is_unsolved = True

    def is_unsolved(self):
        """
            Indicate if text is still unsolved.
        """

        # Indicate
        return self._is_unsolved

    def get_runes(self):
        """
            Gets the runes.
        """

        # Returns the processed runes
        return self._processed_runes

    def get_num_of_runes(self):
        """
            Returns the number of runes.
        """

        # Returns the number of runes
        return len(self._processed_runes)

    def set_runes(self, new_runes):
        """
            Save the runes.
        """

        # Save processed runes
        assert len(new_runes) == len(self._processed_runes), Exception(f'Length mismatch between new runes ({len(new_runes)}) and old runes ({len(self._processed_runes)})')
        self._processed_runes = new_runes[:]

    def get_rune_words(self, remove_periods=True):
        """
            Get Runic words.
        """

        # Get the Runic text
        text = self.get_rune_text()
        if remove_periods:
            text = text.replace('.', ' ')
        else:
            text = text.replace('.', ' . ')
        return [ word for word in ''.join([ c for c in text if RuneUtils.is_rune(c) or c in (' ', '.') ]).split(' ') if len(word) > 0 ]

    def split_sentences(self, include_empty=True):
        """
            Split text into sentences.
        """

        # Split
        sentences = [ [ word for word in ProcessedText(sentence).get_rune_words() if len(word) > 0 ] for sentence in self.get_rune_text().split('.') ]
        if not include_empty:
            sentences = [ sentence for sentence in sentences if len(sentence) > 0 ]
        return sentences

    def split_lines(self, include_empty=True):
        """
            Split text into lines.
        """

        # Split
        lines = self.get_rune_text().split('\n')
        if not include_empty:
            lines = [ line for line in lines if len(line.strip()) > 0 ]
        return lines

    def get_gp_sum_of_runes(self):
        """
            Get the GP sums of runes.
        """

        # Return the GP sums of runes
        result = [ RuneUtils.runes_to_gp_sum(rune) for rune in self.get_runes() ]
        return [ val for val in result if val > 0 ]

    def get_gp_sum_of_words(self):
        """
            Get the GP sums of words.
        """

        # Return the GP sums of words
        result = [ RuneUtils.runes_to_gp_sum(word) for word in self.get_rune_words() ]
        return [ val for val in result if val > 0 ]

    def get_gp_sum_of_sentences(self):
        """
            Get the GP sums of sentences.
        """

        # Return the GP sums of sentences
        result = [ RuneUtils.runes_to_gp_sum(''.join(sentence)) for sentence in self.split_sentences() ]
        return [ val for val in result if val > 0 ]

    def get_first_non_wordlist_word_index(self, wordlist):
        """
            Finds the first Runic word that is not in the given wordlist.
        """

        # Iterate all words
        word_index = -1
        for word in self.get_rune_words():
            word_index += 1
            if word not in wordlist:
                return word_index
        
        # Indicate all words are in the wordlist by just returning the number of words plus one
        return word_index + 1

    def get_rune_text(self, punct_translation=True):
        """
            Gets the rune text.
        """

        # Replace runes from the original with the newly processed runes
        result = ''
        rune_index = 0
        for c in self._orig:
            if RuneUtils.is_rune(c):
                result += self._processed_runes[rune_index]
                rune_index += 1
            else:
                if punct_translation and RuneUtils.is_punct(c):
                    result += RuneUtils.translate_punct(c)
                else:
                    result += c

        # Return result
        return result

    def to_latin(self):
        """
            Translates to Latin.
        """
        
        # Translate to Latin
        text = self.get_rune_text()
        result = []
        for c in text:
            if RuneUtils.is_rune(c):
                result.append(RuneUtils.latin_at(RuneUtils.get_rune_index(c)))
            else:
                result.append(c)
        all_text = ''.join(result)

        # Add prefix if unsolved
        if self._is_unsolved:
            all_text = f'<UNSOLVED>\n\n{all_text}'
        return all_text

    @staticmethod
    def _get_ioc(text, alphabet):
        """
            1-gram IoC calculation.
        """

        # Take only alphabet letters
        instance = [ c for c in text if c in alphabet ]

        # Ignore zero-length
        if len(instance) == 0 or len(alphabet) == 0:
            return 0.0

        # Calculate the IoC
        s = sum([ instance.count(letter) * (instance.count(letter) - 1) for letter in alphabet ])
        d = len(instance) * (len(instance) - 1) / len(alphabet)
        return s / d
 
    def get_rune_ioc(self):
        """
            Returns the IoC for the runes.
        """

        # Calculate IoC
        return self.__class__._get_ioc(self._processed_runes, self.__class__._RUNES)
    
    def get_latin_ioc(self):
        """
            Returns the latin IoC.
        """

        return self.__class__._get_ioc(self.to_latin(), string.ascii_uppercase)

    def check_measurements(self, **kwds):
        """
            Checks measurements.
        """

        # We could not import measurements before due to circular dependency
        import measurements

        # Get measurements unless previously acquired
        if self._measurements is None:

            # Inspect frames up
            self._measurements = []
            curr_frame = inspect.currentframe()
            while curr_frame is not None:
                self._measurements += measurements.get_measurements_for_function(curr_frame.f_code.co_name)
                curr_frame = curr_frame.f_back

        # Run all measurements and stop at first success
        for measurement in self._measurements:
            if measurement.measure(self, **kwds):
                return True

        # Indicate failure
        return False

