#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from LPath import FILES_ALL, LPath
from RuneText import RuneTextFile


#########################################
#  InterruptIndices  :  Read chapters and extract indices (cluster by runes)
#########################################

class InterruptIndices(object):
    def __init__(self):
        self.pos = InterruptIndices.load()

    def consider(self, name, irp, limit):
        nums = self.pos[name]['pos'][irp]
        total = self.pos[name]['total'] if len(nums) <= limit else nums[limit]
        return nums[:limit], total

    def consider_mod_b(self, name, irp, limit, mod):
        sets = [[] for _ in range(mod)]
        for x in self.pos[name]['pos'][irp]:
            mm = x % mod
            sets[mm].append((x - mm) // mod)
        tot = self.pos[name]['total']
        totals = [(tot // mod)] * mod
        for i, x in enumerate(sets):
            if len(x) > limit:
                totals[i] = x[limit]
            elif i < tot % mod:
                totals[i] += 1
        return [x[:limit] for x in sets], totals

    def total(self, name):
        return self.pos[name]['total']

    # def longest_no_interrupt(self, name, irp, irpmax=0):
    #     irpmax += 1
    #     nums = self.pos[name]['pos'][irp] + [self.pos[name]['total']] * irpmax
    #     ret = [(y - x, x) for x, y in zip(nums, nums[irpmax:])]
    #     return sorted(ret, reverse=True)

    @staticmethod
    def write(dbname='db_indices'):
        with open(LPath.db(dbname), 'w') as f:
            f.write('# file | total runes in file | interrupt | indices\n')
            for name in FILES_ALL:
                data = RuneTextFile(LPath.page(name)).index_no_white
                total = len(data)
                nums = [[] for x in range(29)]
                for idx, rune in enumerate(data):
                    nums[rune].append(idx)
                for irp, pos in enumerate(nums):
                    f.write('{}|{}|{}|{}\n'.format(
                        name, total, irp, ','.join(map(str, pos))))

    @staticmethod
    def load(dbname='db_indices'):
        with open(LPath.db(dbname), 'r') as f:
            ret = {}
            for line in f.readlines():
                if line.startswith('#'):
                    continue
                line = line.strip()
                name, total, irp, nums = line.split('|')
                if name not in ret:
                    ret[name] = {'total': int(total),
                                 'pos': [[] for _ in range(29)]}
                pos = ret[name]['pos']
                pos[int(irp)] = list(map(int, nums.split(','))) if nums else []
            return ret


if __name__ == '__main__':
    # InterruptIndices.write()
    for name, val in InterruptIndices.load().items():
        print(name, 'total:', val['total'])
        print(' ', [len(x) for x in val['pos']])
    print()
    for mod in range(1, 4):
        print(f'file: p0-2, maxirp: 20, mod: {mod}')
        pos, limit = InterruptIndices().consider_mod_b('p0-2', 0, 20, mod)
        for i in range(mod):
            print(' ', limit[i], pos[i])
