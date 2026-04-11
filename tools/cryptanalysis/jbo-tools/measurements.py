from research_utils import ResearchUtils
import screen

from abc import ABC
from abc import abstractmethod
import logging

# Maps function names to measurements
_MEASUREMENTS_CACHE = {}

def measurement(measurement_instance):
    """
        Acts as a decorator that could be used for experiments.
    """

    def wrapper(func):
        """
            The decorator wrapper.
        """

        # Save the measurement to the function
        if func.__func__.__name__ not in _MEASUREMENTS_CACHE:
            _MEASUREMENTS_CACHE[func.__func__.__name__] = []
        _MEASUREMENTS_CACHE[func.__func__.__name__].append(measurement_instance)
        return func

    # Return the decorator wrapper function
    return wrapper

def get_measurements_for_function(func_name):
    """
        Get the set of measurements for a given function.
    """

    # Return from cache
    return _MEASUREMENTS_CACHE.get(func_name, [])

class MeasurementBase(ABC):
    """
        Base class for measurements.
    """

    def __init__(self, threshold, greater_than=True):
        """
            Creates an instance.
        """

        # Saves threshold condition and the threshold itself
        self._threshold = threshold
        if greater_than:
            self._cond = lambda measurement:measurement >= threshold
        else:
            self._cond = lambda measurement:measurement <= threshold

    @abstractmethod
    def run_measurement(self, processed_text):
        """
            Runs a mesaurement on a processed text and returns a result.
        """
        pass

    def measure(self, processed_text, **kwds):
        """
            Runs a measurement and presents the processed text if measurement passes.
        """

        # Run and check
        measurement = self.run_measurement(processed_text)
        if not self._cond(measurement):
            return False

        # Print data and log it
        logger = logging.getLogger(__name__)
        logger.info(f'{self.__class__.__name__}: {measurement}\n')
        screen.print_yellow(self.__class__.__name__, end='')
        print(f': {measurement}\n')
        for kwd in kwds:
            logger.info(f'{kwd}: {kwds[kwd]}')
            screen.print_yellow(f'{kwd}:', end='')
            print(f' {kwds[kwd]}')
        if processed_text.section is None:
            screen.print_solved_text(processed_text.to_latin())
        else:
            ResearchUtils.print_section_data(processed_text.section, processed_text)
        return True

class IocMeasurement(MeasurementBase):
    """
        Measures 1-gram IoC.
    """

    def __init__(self, threshold):
        """
            Creates an instance.
        """

        # Calls super
        super().__init__(threshold=threshold)

    def run_measurement(self, processed_text):
        """
            Runs a mesaurement on a processed text and returns a result.
        """

        # Returns the Runic IoC
        return processed_text.get_rune_ioc()

class PrefixWordsMeasurement(MeasurementBase):
    """
        Measures the number of words that match a dictionary.
    """

    def __init__(self, threshold):
        """
            Creates an instance.
        """

        # Calls super
        super().__init__(threshold=threshold)

        # Save the wordlist
        self._wordlist = ResearchUtils.get_english_dictionary_words(as_runes=True)

    def run_measurement(self, processed_text):
        """
            Runs a mesaurement on a processed text and returns a result.
        """

        # Returns the number of matched words
        return processed_text.get_first_non_wordlist_word_index(self._wordlist)

class AllWordsMeasurement(MeasurementBase):
    """
        A Boolean measurement that indicates all words are in a dictionary.
    """

    def __init__(self):
        """
            Creates an instance.
        """

        # Call super
        super().__init__(threshold=0)

        # Save the wordlist
        self._wordlist = ResearchUtils.get_english_dictionary_words(as_runes=True)

    def run_measurement(self, processed_text):
        """
            Runs a mesaurement on a processed text and returns a result.
        """

        # Indicates success or failure which will be matched against the "threshold" of zero
        if processed_text.get_first_non_wordlist_word_index(self._wordlist) >= len(processed_text.get_rune_words()):
            return 1
        else:
            return -1

