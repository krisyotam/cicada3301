#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
from InterruptSearch import InterruptSearch
from InterruptIndices import InterruptIndices
from Probability import Probability
from RuneText import RuneTextFile
from LPath import FILES_ALL, FILES_UNSOLVED, LPath
from KeySearch import GuessPattern


#########################################
#  InterruptDB  :  Perform heuristic search on best possible interrupts.
#########################################

class InterruptDB(object):
    def __init__(self, data, interrupt, irp_stops=None):
        self.irp = interrupt
        self.iguess = InterruptSearch(data, irp=interrupt, irp_stops=irp_stops)
        self.irp_count = len(self.iguess.stops)

    def find_best_solution(self, fn_score, keylen):
        if keylen == 0:  # without interrupts
            score, skips = fn_score(self.iguess.join(), 1), [[]]
        else:
            score, skips = self.iguess.all(keylen, fn_score)
        for i, interrupts in enumerate(skips):
            skips[i] = self.iguess.to_occurrence_index(interrupts)
        return score, skips

    def write(self, dbname, desc, score, keylen, nums):
        with open(LPath.db(dbname), 'a') as f:
            for solution in nums:
                solution = ','.join(map(str, solution))
                f.write('{}|{}|{:.5f}|{}|{}|{}\n'.format(
                    desc, self.irp_count, score, self.irp, keylen, solution))

    @staticmethod
    def load(dbname):
        if not os.path.isfile(LPath.db(dbname)):
            return {}
        ret = {}
        with open(LPath.db(dbname), 'r') as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue
                line = line.rstrip()
                name, irpc, score, irp, kl, nums = [x for x in line.split('|')]
                val = [int(irpc), float(score), int(irp), int(kl)]
                val.append([int(x) for x in nums.split(',')] if nums else [])
                try:
                    ret[name].append(val)
                except KeyError:
                    ret[name] = [val]
        return ret

    @staticmethod
    def load_scores(dbname):
        scores = {}  # {fname: [irp0_[kl0, kl1, ...], irp1_[...]]}
        for name, entries in InterruptDB.load(dbname).items():
            for irpc, score, irp, kl, nums in entries:
                if name not in scores:
                    scores[name] = {}
                pointer = scores[name]
                if irp not in pointer:
                    pointer[irp] = {}
                pointer = pointer[irp]
                if kl not in pointer:
                    pointer[kl] = (0, 0)
                oldc = pointer[kl][1]
                if irpc > oldc or (irpc == oldc and score > pointer[kl][0]):
                    pointer[kl] = (score, irpc)
        return scores


#########################################
#  helper functions
#########################################


def get_db(fname, irp, max_irp):
    stops, Z = InterruptIndices().consider(fname, irp, max_irp)
    data = RuneTextFile(LPath.page(fname)).index_no_white[:Z]
    return InterruptDB(data, irp, irp_stops=stops)


def get_db_invert(fname, irp, max_irp):
    stops, Z = InterruptIndices().consider(fname, 28 - irp, max_irp)
    data = RuneTextFile(LPath.page(fname))
    data.invert()
    data = data.index_no_white[:Z]
    return InterruptDB(data, irp, irp_stops=stops)


def enum_db_irps(dbname, fn_score, max_irp=20, irpset=[0, 28],
                 klset=range(1, 33), files=FILES_UNSOLVED, fn_load_db=get_db):
    oldValues = {k: set((a, b, c) for a, _, b, c, _ in v)
                 for k, v in InterruptDB.load(dbname).items()}
    for irp in irpset:  # interrupt rune index
        for fname in files:
            db = fn_load_db(fname, irp, max_irp)
            print('load:', fname, 'interrupt:', irp, 'count:', db.irp_count)
            for keylen in klset:  # key length
                if (db.irp_count, irp, keylen) in oldValues.get(fname, []):
                    print(f'{keylen}: skipped.')
                    continue
                score, skips = db.find_best_solution(fn_score, keylen)
                yield db, fname, score, keylen, skips


def create_primary(dbname, fn_score):
    for db, fname, score, kl, skips in enum_db_irps(dbname, fn_score,
                                                    irpset=range(29),
                                                    files=FILES_ALL):
        db.write(dbname, fname, score, kl, skips)
        print(f'{kl}: {score:.4f}, solutions: {len(skips)}')


def create_secondary(db_in, db_out, fn_score, threshold=0.75, max_irp=20):
    search_set = set()
    for fname, arr in InterruptDB.load(db_in).items():
        if fname in FILES_UNSOLVED:
            for irpc, score, irp, kl, nums in arr:
                if score > threshold and kl > 3 and kl < 26:
                    search_set.add((fname, irp, kl))
    print('searching through', len(search_set), 'candidates.')
    for fname, irp, kl in search_set:
        print('load:', fname, 'interrupt:', irp, 'keylen:', kl)
        scores = []

        def fn_keep_scores(x, kl):
            score = fn_score(x, kl)
            if score >= threshold:
                scores.append(score)  # hacky but gets the job done
                return 1
            return -1

        db = get_db(fname, irp, max_irp)
        _, skips = db.find_best_solution(fn_keep_scores, kl)
        ret = list(zip(scores, skips))
        bestscore = max(ret)[0]
        # exclude best results, as they are already present in the main db
        filtered = [x for x in ret if x[0] < bestscore]
        for score, nums in filtered:
            db.write(db_out, fname, score, kl, [nums])
        print('found', len(filtered), 'additional solutions')


def create_mod_a_db(dbprefix, fn_score):
    for mod, upto in [(2, 13), (3, 8)]:
        for mo in range(mod):
            # if needed add combined check for all modulo parts
            def xor_split(data, keylen):
                return fn_score(data[mo::mod], keylen)

            dbname = f'db_{dbprefix}_mod_a_{mod}.{mo}'
            for db, fname, score, kl, skips in enum_db_irps(
                    dbname, xor_split, klset=range(1, upto + 1)):
                db.write(dbname, fname, score, kl, skips)
                print(f'mod a {mod}.{mo}, kl: {kl}, score: {score:.4f}')


def create_mod_b_db(dbprefix, fn_score):
    db_i = InterruptIndices()
    for mod, upto in [(2, 18), (3, 18)]:
        for mo in range(mod):
            # custom modulo data load function
            def db_load_mod(fname, irp, max_irp):
                stops, Z = db_i.consider_mod_b(fname, irp, max_irp, mod)
                stops = stops[mo]
                Z = Z[mo]
                data = RuneTextFile(LPath.page(fname)).index_no_white
                data = data[mo::mod][:Z]
                return InterruptDB(data, irp, irp_stops=stops)

            dbname = f'db_{dbprefix}_mod_b_{mod}.{mo}'
            for db, fname, score, kl, skips in enum_db_irps(
                    dbname, fn_score, klset=range(2, upto + 1),
                    fn_load_db=db_load_mod):
                db.write(dbname, fname, score, kl, skips)
                print(f'mod b {mod}.{mo}, kl: {kl}, score: {score:.4f}')


def create_pattern_shift_db(dbprefix, fn_score, offset=0):
    # we misuse the db's keylen column as pattern shift multiply
    for kpl in range(4, 19):  # key pattern length, equiv. to x^2 vigenere
        def fn_pattern_scr(x, kpl_shift):
            gen = GuessPattern.shift_pattern(kpl, kpl_shift)
            parts = GuessPattern.groups(x, kpl, gen, offset)
            return fn_score(parts, kpl)

        dbname = f'db_{dbprefix}_pattern_shift_{kpl}.{offset}'
        for db, fname, score, kl, skips in enum_db_irps(dbname, fn_pattern_scr,
                                                        irpset=[0, 28],
                                                        klset=range(1, kpl)):
            db.write(dbname, fname, score, kl, skips)
            print(f'shift_pattern {kpl}.{offset}'
                  f', shift: {kl}, score: {score:.4f}')


def create_pattern_mirror_db(dbprefix, fn_score, offset=0):
    for typ, generator in [('a', GuessPattern.mirror_pattern_a),
                           ('b', GuessPattern.mirror_pattern_b)]:
        def fn_mirror_scr(x, kl):
            parts = GuessPattern.groups(x, kl, generator(kl), offset)
            return fn_score(parts, kl)

        dbname = f'db_{dbprefix}_pattern_mirror_{typ}.{offset}'
        for db, fname, score, kl, skips in enum_db_irps(dbname, fn_mirror_scr,
                                                        irpset=[0, 28],
                                                        klset=range(4, 19)):
            db.write(dbname, fname, score, kl, skips)
            print(f'mirror_pattern {typ}.{offset}'
                  f', kl: {kl}, score: {score:.4f}')


def create_autokey_db(dbprefix, fn_score):
    # we misuse the db's keylen column as start offset. kl is always 1
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
              59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]

    def fn_autokey_scr(x, kl):
        res = []
        prev = kl
        for y in x:
            z = (y - primes[prev]) % 29  # change here +/- or primes[prev]/prev
            res.append(z)
            prev = z
        return fn_score(res, 1)

    desc = '-p'  # +/- prime, +/- index, '_inv' for invert
    dbname = f'db_{dbprefix}_autokey_{desc}'
    for db, fname, score, kl, skips in enum_db_irps(
            dbname, fn_autokey_scr, max_irp=16, irpset=[0], klset=range(29)):
            # fn_load_db=get_db_invert):  # uncomment to invert, leave irpset=0
        db.write(dbname, fname, score, kl, skips)
        print(f'autokey {desc}, start: {kl}, score: {score:.4f}')


if __name__ == '__main__':
    # create_primary('db_high', Probability.IC_w_keylen)
    # create_primary('db_norm', Probability.target_diff)
    # create_mod_a_db('high', Probability.IC_w_keylen)
    # create_mod_a_db('norm', Probability.target_diff)
    # create_mod_b_db('high', Probability.IC_w_keylen)
    # create_mod_b_db('norm', Probability.target_diff)
    # create_pattern_shift_db('high', Probability.parts_high, offset=0)
    # create_pattern_shift_db('norm', Probability.parts_norm, offset=0)
    # create_pattern_mirror_db('high', Probability.parts_high, offset=0)
    # create_pattern_mirror_db('norm', Probability.parts_norm, offset=0)
    create_autokey_db('high', Probability.IC_w_keylen)
    # create_autokey_db('norm', Probability.target_diff)
    # create_secondary('db_high', 'db_high_secondary',
    #                  Probability.IC_w_keylen, threshold=1.4)
    # create_secondary('db_norm', 'db_norm_secondary',
    #                  Probability.target_diff, threshold=0.55)
