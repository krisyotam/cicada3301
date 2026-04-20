#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import math


def is_prime(num):
    if isinstance(num, str):
        num = int(num)
    if num in [2, 3, 5]:
        return True
    if num & 1 and num % 5 > 0:
        for i in range(2, math.floor(math.sqrt(num)) + 1):
            if i & 1 and (num % i) == 0:
                return False
        return True
    return False


def rev(num):  # or int(str(num)[::-1])
    if isinstance(num, str):
        num = int(num)
    revs = 0
    while (num > 0):
        remainder = num % 10
        revs = (revs * 10) + remainder
        num = num // 10
    return revs


def is_emirp(num):
    return is_prime(rev(num))


def power(x, y, p):
    res = 1
    x %= p
    while (y > 0):
        if (y & 1):
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p
    return res


def sqrtNormal(n, p):
    n %= p
    for x in range(2, p):
        if ((x * x) % p == n):
            return x
    return None


# Assumption: p is of the form 3*i + 4 where i >= 1
def sqrtFast(n, p):
    if (p % 4 != 3):
        # raise ValueError('Invalid Input')
        return sqrtNormal(n, p)
    # Try "+(n ^ ((p + 1)/4))"
    n = n % p
    x = power(n, (p + 1) // 4, p)
    if ((x * x) % p == n):
        return x
    # Try "-(n ^ ((p + 1)/4))"
    x = p - x
    if ((x * x) % p == n):
        return x
    return None


def elliptic_curve(x, a, b, r):
    y2 = (x ** 3 + a * x + b) % r
    y = sqrtFast(y2, r) if y2 > 0 else 0
    if y is None:
        return None, None
    return y, -y % r


AFFINE_INV = None


def affine_inverse(s, n=29):
    def fn(s, n):
        g = [n, s]
        u = [1, 0]
        v = [0, 1]
        y = [None]
        i = 1
        while g[i] != 0:
            y.append(g[i - 1] // g[i])
            g.append(g[i - 1] - y[i] * g[i])
            u.append(u[i - 1] - y[i] * u[i])
            v.append(v[i - 1] - y[i] * v[i])
            i += 1
        return v[-2] % n

    global AFFINE_INV
    if AFFINE_INV is None:
        AFFINE_INV = [fn(x, n) for x in range(n)]
    return AFFINE_INV[s]


def affine_decrypt(x, key, n=29):  # key: (s, t)
    return ((x - key[1]) * affine_inverse(key[0], n)) % n


def autokey_reverse(data, keylen, pos, search_term):
    ret = [29] * keylen
    for o in range(len(search_term)):
        plain = search_term[o]
        i = pos + o
        while i >= 0:
            plain = (data[i] - plain) % 29
            i -= keylen
        ret[i + keylen] = plain
    return ret


if __name__ == '__main__':
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cipher = 'YDIDWYASDDJVAPJMMBIASDTJVAMD'
    indices = [affine_decrypt(alphabet.index(x), (5, 9), 26) for x in cipher]
    print(''.join(alphabet[x] for x in indices))
