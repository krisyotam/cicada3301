"""
    Custom-Made Arg-Parser for
    GEMATRIA
"""

from __future__ import annotations
import argparse

class ArgParser(object):
    """Parser Class for argument execution"""

    # Built-in python arg parser
    parser: argparser.ArgumentParser
    
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="GEMATRIA Liber Primus tool")
        self.define()

    def define(self) -> None:
        """Define Arguments"""
        # Message to be encoded/decoded/analyzed
        self.parser.add_argument("message")
        
        # Input file for hashing
        self.parser.add_argument("--input", action='store', default=None)

    def parse(self) -> Tuple:
        """Parse GEMATRIA args"""
        parsed_namespace = self.parser.parse_args()

        return (parsed_namespace.message, parsed_namespace.input)
