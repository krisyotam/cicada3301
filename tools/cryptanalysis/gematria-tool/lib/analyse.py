"""
    Main "Analysing" script
"""

from __future__ import annotations
import logging
import gematria as gematria
from hashing import Hashing
from writer import Writer
import utils

logger = logging.getLogger(__name__)

class Analyse:
    """Class that will take a message and do processing on the string"""

    # String to be processed
    message: str

    # Custom file writer
    writer: Writer

    def __init__(self, message: str, writer: Writer) -> None:
        self.message = message
        self.writer = writer
        self.hasher = Hashing(self.message, self.writer)

    def analyse(self) -> None:
        """Main analyze function"""
        # Hash and compare string into all implemented hash fn's
        self.hasher.str_check()

        # Gematria related processing
        self.gematria()
	
    def process_gematria_message(self, runic_message: Cipher) -> None:
        """
            Gematria Processing of prime sums
                1. Message
                2. Words
                3. Lines
                4. TODO .to_numbers()
        """
        # 1. Message
        message_sum = runic_message.gematria_sum()
        message_prime, message_emirp = utils.get_prime_and_emirp(message_sum)
        self.print_sum_prime_status(runic_message.text, message_sum, message_prime, message_emirp)

        # Divisor between 1. Message and 2. Words
        divisor_str = f"PROCESSING EACH WORD IN \"{runic_message.text}\""
        logger.info(divisor_str)
        self.writer.title(divisor_str)

        # 2. Words
        words_list = runic_message.get_words()
        words_sum = runic_message.gematria_sum_words()
        for i in range(len(words_list)):
            words_prime, words_emirp = utils.get_prime_and_emirp(words_sum[i])
            self.print_sum_prime_status(words_list[i], words_sum[i], words_prime, words_emirp)

        # Divisor between 2. Words and 3. Lines
        divisor_str = f"PROCESSING EACH LINE IN \"{runic_message.text}\""
        logger.info(divisor_str)
        self.writer.title(divisor_str)

        # 3. Lines
        lines_list = runic_message.get_lines()
        lines_sum = runic_message.gematria_sum_lines()
        for i in range(len(lines_list)):
            lines_prime, lines_emirp = utils.get_prime_and_emirp(lines_sum[i])
            self.print_sum_prime_status(lines_list[i], lines_sum[i], lines_prime, lines_emirp)

    def gematria(self) -> None:
        """Gematria Related Processing
            1. Process Untouched Message
            2. Process Atbash Message	
        """
        # 1. Process Untouched Message
        # Logging
        runic_version = gematria.Runes(self.message).to_runes()
        latin_version = gematria.Runes(self.message).to_latin()
        title_str = "GEMATRIA PROCESSING...\n\tRUNIC: " + str(runic_version) + "\n\tLATIN: " + str(latin_version)
        logger.info(title_str)
        self.writer.title(title_str)
        print("") # Separtor from title to specific processing

        # Gematria sum & Prime
        self.process_gematria_message(runic_version)

        # 2. Process Atbash Message
        # Logging
        runic_version = runic_version.atbash()
        latin_version = latin_version.atbash()
        title_str = "ATBASH >> GEMATRIA PROCESSING...\n\tRUNIC: " + str(runic_version) + "\n\tLATIN: " + str(latin_version)
        logger.info(title_str)
        self.writer.title(title_str)
        print("") # Separator from title to specific processing

        # Gematria sum & Prime
        self.process_gematria_message(runic_version)

    def print_sum_prime_status(self, target: str, gem_sum: int, prime: bool, emirp: bool) -> None:
        """Helper function to print prime status"""
        # output_str = f"{target} >>>\n"
        output_str = f"{target}\n"
        output_str += "-" * (len(target) + 4) + "\n"
        output_str += f"\tGEMATIRA SUM: {gem_sum}\n"
        output_str += f"\tIS_PRIME() = {prime} >>> IS_EMIRP() = {emirp}\n"

        self.writer.write_and_print(output_str, print_time=False)
