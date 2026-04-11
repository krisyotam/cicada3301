#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from Alphabet import rune_map
from RuneText import RuneText
from NGrams import NGrams


#########################################
#  NGramShifter  :  Shift rune-pairs in a fixed-width running window
#########################################

class NGramShifter(object):
    def __init__(self, gramsize=3):  # 3 is the only reasonable value though
        self.gramsize = gramsize
        self.prob = NGrams.load(gramsize)

    def ngram_probability_heatmap(self, data):
        gram_count = len(data) // self.gramsize
        ret = [[] for _ in range(gram_count)]  # ret[x][y] x: parts, y: shifts
        for y in range(29):
            variant = data - y
            for x in range(gram_count):
                i = x * self.gramsize
                gram = ''.join(r.rune for r in variant[i:i + self.gramsize])
                ret[x].append((y, self.prob.get(gram, 0), gram))
        # sort most probable first
        for arr in ret:
            arr.sort(key=lambda x: -x[1])  # (shift, probability)
        return ret

    def guess_single(self, data, interrupt_chr=None):
        data = RuneText(data)
        res = self.ngram_probability_heatmap(data)
        fillup = ' ' * (2 * self.gramsize + 1)
        all_interrupts = []
        if interrupt_chr:
            for i, x in enumerate(data):
                if x.rune == interrupt_chr:
                    all_interrupts.append(i)
        for y in range(29):  # each row in output
            line = ''
            for i, obj in enumerate(res):  # each column per row
                txt = ''
                if obj[y][1] > 0:
                    for u in range(self.gramsize):
                        if (i * self.gramsize + u) in all_interrupts:
                            txt += '|'  # mark with preceding
                        txt += rune_map[obj[y][2][u]]
                line += txt + fillup[len(txt):]
            line = line.rstrip()
            if line:
                print(line)

    def guess(self, data, interrupt_chr=None):
        data = RuneText(data)  # create RuneText once and reuse
        for i in range(self.gramsize):
            print('offset:', i)
            self.guess_single(data[i:], interrupt_chr)
            print()


if __name__ == '__main__':
    NGramShifter().guess('ᛈᚢᛟᚫᛈᚠᛖᚱᛋᛈᛈᚦᛗᚾᚪᚱᛚᚹᛈᛖᚩᛈᚢᛠᛁᛁᚻᛞᛚᛟᛠ', 'ᛟ')
    NGramShifter().guess([1, 2, 4, 5, 7, 9, 0, 12], 'ᛟ')
