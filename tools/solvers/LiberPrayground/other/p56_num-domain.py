#!/usr/bin/env python3
from hashlib import sha512, blake2b
import sys

search = '36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618dee09a8425893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4'


def enc(hash_string):
    x = hash_string.encode()
    return blake2b(x).hexdigest(), sha512(x).hexdigest()


for i in range(6452 * 1000000, 100000000000):
    addr = '{}'.format(i)
    for x in [addr, addr + '.com']:
        hahs = enc(x)
        if search in hahs:
            print('FOUND: ' + x)
            exit()
    if i % 1000000 == 0:
        sys.stdout.write('.')
        sys.stdout.flush()
print('done.')
