"""
    Hashing Script
"""

import sys
import hashlib
import logging
import whirlpool
import blake512 # https://github.com/tweqx/python-blake512
import skein # https://pythonhosted.org/pyskein/skein.html
from writer import Writer
from utils import hamming_distance

logger = logging.getLogger(__name__)

# Constaants
DEEPWEB_HASH = "36367763ab73783c7af284446c59466b4cd653239a311cb71\
16d4618dee09a8425893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4"
BYTE_DEEPWEB_HASH = DEEPWEB_HASH.encode('UTF-8')

class Hashing:
    """Hashing class that will handle all hashing of a specified string"""

    # String to be hased
    message: str
    b_message: bytes # bytes message

    # Custom file writer
    writer: Writer

    def __init__(self, message: str, writer: Writer) -> None:
        self.message = message
        self.b_message = self.message.encode('UTF-8')
        self.writer = writer

    def blake2b(self) -> str:
        """Blake2b Hashing"""
        hash_digest = hashlib.blake2b(digest_size=64)
        hash_digest.update(self.b_message)
        return hash_digest.hexdigest()

    def blake512(self) -> str:
        """Blake1-512 Hashing"""
        hash_digest = blake512.hash(self.message)
        return hash_digest

    def sha512(self) -> str:
        """Sha512 Hashing"""
        hash_digest = hashlib.sha512()
        hash_digest.update(self.b_message)
        return hash_digest.hexdigest()

    def sha3(self) -> str:
        """SHA3 64 digest hashing"""
        hash_digest = hashlib.sha3_512()
        hash_digest.update(self.b_message)
        return hash_digest.hexdigest()

    def whirlpool(self) -> str:
        """Whirlpool hashing"""
        hash_digest = whirlpool.new(self.b_message)
        return hash_digest.hexdigest()

    def skein512(self) -> str:
        """Skein512 Hashing"""
        hash_digest = skein.skein512()
        hash_digest.update(self.b_message)
        return hash_digest.hexdigest()

    def tiger(self) -> str:
        """TigerHash Hashing"""
        #hash_digest = tiger.hash(self.message)
        #return hash_digest
        return "NOT WORKING ATM"

    def assert_hash_fn(self, hash_fn, str_info) -> bool:
        """Assert if a hash function hashes to the DEEPWEB HASH"""
        hash_digest = hash_fn()
        is_deepweb_hash = self.is_byte_deepweb_hash(hash_digest)
        distance = hamming_distance(str(hash_digest), str(DEEPWEB_HASH))

        output_str = f"{str_info} -> {hash_digest} | IS_DEEPWEB_HASH() \
-> {is_deepweb_hash} >> d:{distance}"
        print(output_str)
        self.writer.write(output_str)

        # Deepweb hash alert
        if is_deepweb_hash:
            logger.critical(f"FOUND DEEPWEB HASH IN {self.message} ENCODED IN {str_info}")
            sys.exit(0)

        return is_deepweb_hash

    def str_check(self) -> bool:
        """For every hash function:
            1. Hash string
            2. Compare to DWH
        """
        # Logging
        output_str = f"HASHING \"{self.message}\"..."
        logger.info(output_str)
        self.writer.title(output_str)

        # blake2b
        self.assert_hash_fn(self.blake2b, "BLAKE2B")

        # blake512
        self.assert_hash_fn(self.blake512, "BLAKE512")

        # sha512
        self.assert_hash_fn(self.sha512, "SHA512")

        # sha3
        self.assert_hash_fn(self.sha3, "SHA3")

        # whirlpool
        self.assert_hash_fn(self.whirlpool, "WHIRLPOOL")

        # Skein512
        self.assert_hash_fn(self.skein512, "SKEIN512")

        # Tiger
        # self.assert_hash_fn(self.tiger, "TIGER"

    def is_byte_deepweb_hash(self, b_string: bytes) -> bool:
        """Checks if given byte str is the deepweb hash from LP"""
        if isinstance(b_string, str):
            b_string = b_string.encode('UTF-8')

        return b_string == BYTE_DEEPWEB_HASH
