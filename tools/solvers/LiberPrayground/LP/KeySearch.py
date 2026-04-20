#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils import affine_decrypt


#########################################
#  GuessVigenere  :  Shift values around with a given keylength
#########################################

class GuessVigenere(object):
    def __init__(self, nums):
        self.nums = nums

    def guess(self, keylength, score_fn):  # minimize score_fn
        found = []
        avg_score = 0
        for offset in range(keylength):
            bi = -1
            bs = 9999999
            for i in range(29):
                shifted = [(x - i) % 29 for x in self.nums[offset::keylength]]
                score = score_fn(shifted)
                if score < bs:
                    bs = score
                    bi = i
            avg_score += bs
            found.append(bi)
        return avg_score / keylength, found


#########################################
#  GuessAffine  :  Find greatest common affine key
#########################################

class GuessAffine(object):
    def __init__(self, nums):
        self.nums = nums

    def guess(self, keylength, score_fn):  # minimize score_fn
        found = []
        avg_score = 0
        for offset in range(keylength):
            candidate = (None, None)
            best = 9999999
            for s in range(29):
                for t in range(29):
                    shifted = [affine_decrypt(x, (s, t))
                               for x in self.nums[offset::keylength]]
                    score = score_fn(shifted)
                    if score < best:
                        best = score
                        candidate = (s, t)
            avg_score += best
            found.append(candidate)
        return avg_score / keylength, found


#########################################
#  GuessPattern  :  Find a key that is rotated ABC BCA CAB, or ABC CAB BCA
#########################################

class GuessPattern(object):
    @staticmethod
    def groups(nums, keylen, generator, offset=0):
        for _ in range(offset):
            next(generator)
        ret = [[] for _ in range(keylen)]
        for idx, value in zip(generator, nums):
            ret[idx].append(value)
        return ret

    def shift_pattern(kl, shift=1):  # shift by (more than) one, 012201120
        for i in range(10000):
            p = (i * shift) % kl
            yield from range(p, kl)
            yield from range(p)

    def mirror_pattern_a(kl):  # mirrored, 012210012210
        for i in range(10000):
            yield from range(kl)
            yield from range(kl - 1, -1, -1)

    def mirror_pattern_b(kl):  # mirrored, 012101210
        for i in range(10000):
            yield from range(kl)
            yield from range(kl - 2, 0, -1)

    @staticmethod
    def zip(nums, key, keylen, shift=1, offset=0):
        gen = GuessPattern.shift_pattern(keylen, shift)
        for _ in range(offset):
            next(gen)
        return [(n - key[k]) % 29 for n, k in zip(nums, gen)]

    @staticmethod
    def guess(parts, score_fn):  # minimize score_fn
        found = []
        avg_score = 0
        for nums in parts:
            best = 9999999
            candidate = 0
            for i in range(29):
                score = score_fn([(x - i) % 29 for x in nums])
                if score < best:
                    best = score
                    candidate = i
            avg_score += best
            found.append(candidate)
        return avg_score / len(parts), found


if __name__ == '__main__':
    print(list(GuessPattern.shift_pattern(4, 3))[:20])
