#!/usr/bin/env python3
from core import *
from transformers import *
from liber_primus import LiberPrimus
import screen

import subprocess
import platform
import os
import shutil

class ResearchUtils(object):
    """
        Research utlities.
    """

    # Cache for English words
    _ENGLISH_WORD_RUNES = None
    _ENGLISH_WORD_ENGLISH = None

    # Cache for unsolved sections
    _UNSOLVED_SECTIONS = None

    @classmethod
    def get_unsolved_sections(cls):
        """
            Gets all unsolved sections.
        """

        # Work on cache
        if cls._UNSOLVED_SECTIONS is None:

            # Try to decrypt all sections
            cls._UNSOVLED_SECTIONS = []
            for section in LiberPrimus.get_all_sections():

                # Process all text
                processed_text = ProcessedText(section.get_all_text())
                for transformer in section.transformers:
                    transformer.transform(processed_text)

                # Add to result if section is unsolved
                if processed_text.is_unsolved():
                    cls._UNSOVLED_SECTIONS.append(section)

        # Return all unsolved sections
        return cls._UNSOVLED_SECTIONS

    @classmethod
    def get_english_dictionary_words(cls, as_runes=True):
        """
            Gets words from an English dictionary.
        """

        # Build cache
        if cls._ENGLISH_WORD_RUNES is None or cls._ENGLISH_WORD_ENGLISH is None:
            cls._ENGLISH_WORD_RUNES = set()
            cls._ENGLISH_WORD_ENGLISH = set()
            with open('english_wordlist.txt', 'r') as fp:
                for word in fp.read().split('\n'):
                    if len(word) == 0:
                        continue
                    cls._ENGLISH_WORD_ENGLISH.add(word)
                    runic = RuneUtils.english_to_runes(word)
                    if len(runic) == 0:
                        continue
                    cls._ENGLISH_WORD_RUNES.add(runic)
        
        # Use cache
        return cls._ENGLISH_WORD_RUNES if as_runes else cls._ENGLISH_WORD_ENGLISH

    @classmethod
    def get_rune_wordlist(cls, use_dictionary=False):
        """
            Get a Runic wordlist from all solved sections dynamically.
            Can also extend to an English wordlist.
        """

        # Try to decrypt all sections
        result = set()
        for section in LiberPrimus.get_all_sections():

            # Process all text
            processed_text = ProcessedText(section.get_all_text())
            for transformer in section.transformers:
                transformer.transform(processed_text)

            # Skip unsolved sections 
            if processed_text.is_unsolved():
                continue

            # Get all words
            for word in processed_text.get_rune_words():
                if len(word) == 0:
                    continue
                result.add(word)

        # Optionally extend to use a wordlist
        if use_dictionary:

           # Use cache
            result = set.union(result, cls.get_english_dictionary_words(as_runes=True))

        # Return wordlist sorted by word length descending
        return sorted(result, key=len)[::-1]

    @staticmethod
    def print_section_data(section, processed_text=None):
        """
            Unified way of printing a section data.
        """

        # Present section contents
        screen.print_yellow('Section:', end='')
        print(f' {section.name}', end='')
        if len(section.title) > 0:
            print(f' ("{section.title}")')
        else:
            print('')
        if processed_text is not None:
            screen.print_yellow('Runic IoC (post):', end='')
            print(f' {processed_text.get_rune_ioc()}')
            screen.print_yellow('Latin IoC:', end='')
            print(f' {processed_text.get_latin_ioc()}')
            screen.print_yellow('Rune count:', end='')
            print(f' {len(processed_text.get_runes())}\n\n')
            screen.print_solved_text(f'{processed_text.to_latin()}\n\n{processed_text.get_rune_text()}\n\n\n')
        
        # Show page numbers if available
        page_numbers_string = ', '.join([ str(number) for number in section.get_page_numbers() ])
        if len(page_numbers_string) > 0:
            screen.print_yellow('\nPages:', end='')
            print(f' {page_numbers_string}')

    @staticmethod
    def launch_path(path):
        """
            Launches the given path.
        """

        # Act differently based on platform
        if platform.system() == 'Darwin':
            subprocess.call(('open', path))
        elif platform.system() == 'Windows':
            os.startfile(path)
        else:
            subprocess.call(('xdg-open', path))

    @staticmethod
    def get_command_path(command):
        """
            Gets the command path, or returns None if not found.
        """

        # Find the path
        path = shutil.which(command)
        if path is not None:
            return path

        # Use the PATH environment variable
        paths = os.environ.get('PATH', None)
        if paths is None:
            return None

        # Use both Windows and *NIX style
        for base_path in paths.replace(':', ';').split(';'):
            path = os.path.join(base_path, command)
            if os.path.isfile(path):
                return path
            if platform.system() == 'Windows':
                path += '.exe'
                if os.path.isfile(path):
                    return path
        
        # Nothing was found
        return None

    @staticmethod
    def iterate_potential_interrupter_indices(processed_text, interrupter_rune='ᚠ'):
        """
            Iterates all the potential interrupter indices.
        """

        # Finds all potential indices
        runes = processed_text.get_runes()
        potential_interrupters = [ i for i in range(len(runes)) if runes[i] == interrupter_rune ]

        # Iterate
        for mask in range(2**len(potential_interrupters)):
            yield [ potential_interrupters[i] for i in range(len(potential_interrupters)) if (mask & (1<<i)) > 0 ]

