"""
    Hashing script for the deepweb hash using the Gematria library(./lib/)

    - Takes in a file input with '\n' separated values
    to be hashed by the various hash funtions and compared to the deepweb hash
"""

from __future__ import annotations
import logging, coloredlogs
import sys
import lib as gematria

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

def main() -> int:
    """Hashing entry point"""
    
    # Parse args
    logger.info("PARSING ARGS")
    ap = gematria.ArgParser()
    parsed_args = ap.parse()

    message = parsed_args[0]
    file_input = parsed_args[1]

    if file_input is None:
        logger.critical("MUST PROVIDE A FILE CONTAINING STRINGS TO HASH(--input file.txt)")
        return -1

    # Writer with title of the file we are hashing contents
    title = gematria.utils.get_file_name(file_input)
    writer = gematria.Writer(message=title)

    # Read all file content
    content = gematria.utils.file_into_array(file_input)
    
    # Hash all
    hash_all(content, writer)

    return 0

def hash_all(content: List, writer: gematria.Writer) -> None:
    """Hash compares every line in content"""
    
    for string_hash in content:
        # Create new hashing and writer object
        hasher = gematria.Hashing(message=string_hash, writer=writer)

        # Hash against all
        hasher.str_check()

if __name__ == "__main__":
    sys.exit(main())
