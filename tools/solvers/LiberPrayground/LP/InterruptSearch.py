#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import itertools  # product, compress, combinations
import bisect  # bisect_left, insort


#########################################
#  InterruptSearch  :  Hill climbing algorithm for interrupt detection
#########################################

class InterruptSearch(object):
    def __init__(self, arr, irp, irp_stops=None):  # remove whitespace in arr
        self.single_result = False  # if False, return list of equal likelihood
        self.full = arr
        if irp_stops is None:
            self.stops = [i for i, n in enumerate(arr) if n == irp]
        else:
            self.stops = irp_stops

    def to_occurrence_index(self, interrupts):
        return [self.stops.index(x) + 1 for x in interrupts]

    def from_occurrence_index(self, interrupts):
        return [self.stops[x - 1] for x in interrupts]

    def join(self, interrupts=[]):  # rune positions, not occurrence index
        ret = []
        i = -1
        for x in interrupts:
            ret += self.full[i + 1:x]
            i = x
        return ret + self.full[i + 1:]

    # Just enumerate all possibilities.
    # If you need to limit the options, trim the data before computation
    def all(self, keylen, score_fn):
        best_s = -8
        found = []  # [match, match, ...]
        for x in itertools.product([False, True], repeat=len(self.stops)):
            part = list(itertools.compress(self.stops, x))
            score = score_fn(self.join(part), keylen)
            if score >= best_s:
                if score > best_s or self.single_result:
                    best_s = score
                    found = [part]
                else:
                    found.append(part)
        return best_s, found

    # Go over the full string but only look at the first {maxdepth} interrupts.
    # Enumerate all possibilities and choose the one with the highest score.
    # If first interrupt is set, add it to the resulting set. If not, ignore it
    # Every iteration will add a single interrupt only, not the full set.
    def sequential(self, keylen, score_fn, startAt=0, maxdepth=9):
        found = [[]]

        def best_in_one(i, depth, prefix=[]):
            best_s = -8
            best_p = []  # [match, match, ...]
            irp = self.stops[i:i + depth]
            for x in itertools.product([False, True], repeat=depth):
                part = list(itertools.compress(irp, x))
                score = score_fn(self.join(prefix + part), keylen)
                if score >= best_s:
                    if score > best_s or self.single_result:
                        best_s = score
                        best_p = [part]
                    else:
                        best_p.append(part)
            return best_p, best_s

        def best_in_all(i, depth):
            best_s = -8
            best_p = []  # [(prefix, [match, match, ...]), ...]
            for pre in found:
                parts, score = best_in_one(i, depth, prefix=pre)
                if score >= best_s:
                    if score > best_s or self.single_result:
                        best_s = score
                        best_p = [(pre, parts)]
                    else:
                        best_p.append((pre, parts))
            return best_p, best_s

        # first step: move maxdepth-sized window over data
        i = startAt - 1  # in case loop isnt called
        for i in range(startAt, len(self.stops) - maxdepth):
            print('.', end='')
            parts, _ = best_in_all(i, maxdepth)
            found = []
            search = self.stops[i]
            for prfx, candidates in parts:
                bitSet = False
                bitNotSet = False
                for x in candidates:
                    if len(x) > 0 and x[0] == search:
                        bitSet = True
                    else:
                        bitNotSet = True
                    if bitSet and bitNotSet:
                        break
                if bitSet:
                    found.append(prfx + [search])
                if bitNotSet:
                    found.append(prfx)
        print('.')
        # last step: all permutations for the remaining (< maxdepth) bits
        i += 1
        remaining, score = best_in_all(i, min(maxdepth, len(self.stops) - i))
        found = [x + z for x, y in remaining for z in y]
        return score, found

    # Flip upto {maxdepth} bits anywhere in the full string.
    # Choose the bitset with the highest score and repeat.
    # If no better score found, increment number of testing bits and repeat.
    # Either start with all interrupts set (topDown) or none set.
    def genetic(self, keylen, score_fn, topDown=False, maxdepth=3):
        current = self.stops if topDown else []

        def evolve(lvl):
            if lvl > 0:
                yield from evolve(lvl - 1)
            for x in itertools.combinations(self.stops, lvl + 1):
                tmp = current[:]
                for y in x:
                    if y in current:
                        tmp.pop(bisect.bisect_left(tmp, y))
                    else:
                        bisect.insort(tmp, y)
                yield tmp, score_fn(self.join(tmp), keylen)

        best = score_fn(self.join(), keylen)
        level = 0  # or start directly with maxdepth - 1
        while level < maxdepth:
            print('.', end='')
            update = None
            for interrupts, score in evolve(level):
                if score > best:
                    best = score
                    update = interrupts
            if update:
                level = 0  # restart with 1-bit again
                current = update
                continue  # did optimize, so retry with same level
            level += 1
        print('.')
        # find equally likely candidates
        if self.single_result:
            return best, [current]
        all_of_them = [x for x, score in evolve(2) if score == best]
        all_of_them.append(current)
        return best, all_of_them


if __name__ == '__main__':
    a = InterruptSearch([2, 0, 1, 0, 14, 15, 0, 13, 24, 25, 25, 25], irp=0)
    print(a.sequential(1, lambda x, k: (1.2 if len(x) == 11 else 0.1)))
    print(a.sequential(1, lambda x, k: (1.1 if len(x) == 10 else 0.1)))
    print(a.sequential(1, lambda x, k: (1.3 if len(x) == 9 else 0.1)))
    print(a.genetic(1, lambda x, k: (1.5 if len(x) == 10 else 0.1)))
    print(a.all(1, lambda x, k: (1.4 if len(x) == 11 else 0.1)))
