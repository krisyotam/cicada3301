"""
    GEMATRIA Cryptography tool to aid in decyphering fo LP(Liber Primus)

    by lipeeeee
"""

import sys
import logging
import coloredlogs
from arg_parser import ArgParser
from analyse import Analyse
from writer import Writer

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

def main() -> int:
    """GEMATRIA Entry Point"""
    
    # Parse args
    logger.info("PARSING ARGS")
    ap = ArgParser()
    parsed_args = ap.parse()
    
    message = parsed_args[0]
    input_ = parsed_args[1]

    # File Writer
    writer = Writer(message)

    # Analyze
    logger.info("STARTING TO ANALYSE")
    a = Analyse(message, writer)
    a.analyse()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

