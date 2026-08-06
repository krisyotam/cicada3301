#!/usr/bin/env python3
from hashlib import sha512, blake2b

search = '36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618dee09a8425893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4'


def enc(hash_string):
    x = hash_string.encode()
    return blake2b(x).hexdigest(), sha512(x).hexdigest()


with open('list-onions.txt', 'r') as f:
    for line in f.readlines():
        addr = line.strip()
        for x in [addr, 'http://' + addr, 'http://' + addr + '/', addr.split('.onion')[0]]:
            hahs = enc(x)
            if search in hahs:
                print('FOUND: ' + x)
                exit()
