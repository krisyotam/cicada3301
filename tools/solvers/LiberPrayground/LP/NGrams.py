#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import re
from Alphabet import RUNES
from RuneText import RuneText
from LPath import LPath


#########################################
#  NGrams  :  loads and writes ngrams, also: translate english text to runes
#########################################

class NGrams(object):
    @staticmethod
    def translate(infile, outfile, stream=False):  # takes 10s
        with open(infile, 'r') as f:
            src = re.sub('[^A-Z]', '' if stream else ' ', f.read().upper())
            if stream:
                src.replace('\n', '')

        with open(outfile, 'w') as f:
            flag = False
            for r in RuneText.from_text(src):
                if r.kind != 'r':
                    if not flag:
                        f.write('\n')
                        flag = True
                    continue
                f.write(r.rune)
                flag = False

    @staticmethod
    def make(gramsize, infile, outfile):
        with open(infile, 'r') as f:
            data = re.sub('[^' + ''.join(RUNES) + ']', '', f.read())

        res = {x: 0 for x in RUNES} if gramsize == 1 else {}
        for i in range(len(data) - gramsize + 1):
            ngram = data[i:i + gramsize]
            try:
                res[ngram] += 1
            except KeyError:
                res[ngram] = 1

        with open(outfile, 'w') as f:
            for x, y in sorted(res.items(), key=lambda x: -x[1]):
                f.write(f'{x} {y}\n')

    @staticmethod
    def load(ngram=1, prefix=''):
        ret = {}
        with open(LPath.data(f'p{prefix}-{ngram}gram'), 'r') as f:
            for line in f.readlines():
                r, v = line.split()
                ret[r] = int(v)
        return ret


if __name__ == '__main__':
    def make_translation(stream=False):  # if true, ignore spaces / word bounds
        NGrams.translate(LPath.data('baseline-text'),
                         LPath.data('baseline-rune'), stream)

    def make_ngrams(max_ngram=1):
        for i in range(1, max_ngram + 1):
            print(f'generate {i}-gram file')
            NGrams.make(i, infile=LPath.data('baseline-rune-words'),
                        outfile=LPath.data(f'p-{i}gram'))
            NGrams.make(i, infile=LPath.root('_solved.txt'),
                        outfile=LPath.data(f'p-solved-{i}gram'))
            NGrams.make(i, infile=LPath.data('baseline-rune-no-e'),
                        outfile=LPath.data(f'p-no-e-{i}gram'))

    # make_translation(stream=False)
    # make_ngrams(5)
    print(NGrams.load(2))
