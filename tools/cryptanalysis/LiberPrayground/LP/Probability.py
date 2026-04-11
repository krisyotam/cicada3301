#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from NGrams import NGrams
from Alphabet import RUNES


def normalized_probability(int_prob):
    total = sum(int_prob)
    return [x / total for x in int_prob]  # math.log(x / total, 10)


PROB_INT = [0] * 29
for k, v in NGrams.load(1, '').items():  # '-no-e', '-solved'
    PROB_INT[RUNES.index(k)] = v
PROB_NORM = normalized_probability(PROB_INT)
# Target IoC. peace and war: 1.77368517 solved: 1.78021503, no e: 1.82715300
N_total = (sum(PROB_INT) * (sum(PROB_INT) - 1)) / 29
TARGET_IOC = sum(x * (x - 1) for x in PROB_INT) / N_total
# TARGET_IOC = 1.78


#########################################
#  Probability  :  Count runes and do simple frequency analysis
#########################################

class Probability(object):
    def __init__(self, numstream):
        self.prob = [0] * 29
        for r in numstream:
            self.prob[r] += 1
        self.N = sum(self.prob)

    def IC(self):
        X = sum(x * (x - 1) for x in self.prob)
        return X / ((self.N * (self.N - 1)) / 29)

    def IC_norm(self, target_ioc=TARGET_IOC):
        return 1 - abs(self.IC() - target_ioc)

    def similarity(self):
        probs = normalized_probability(self.prob)
        return sum((x - y) ** 2 for x, y in zip(PROB_NORM, probs))

    @staticmethod
    def IC_w_keylen(nums, keylen):
        val = sum(Probability(nums[x::keylen]).IC() for x in range(keylen))
        return val / keylen

    @staticmethod
    def target_diff(nums, keylen, target_ioc=TARGET_IOC):
        val = sum(abs(Probability(nums[x::keylen]).IC() - target_ioc)
                  for x in range(keylen))
        return 1 - (val / keylen)

    @staticmethod
    def parts_high(parts, keylen):
        return sum(Probability(x).IC() for x in parts) / keylen

    @staticmethod
    def parts_norm(parts, keylen, target_ioc=TARGET_IOC):
        val = sum(abs(Probability(x).IC() - target_ioc) for x in parts)
        return 1 - (val / keylen)
