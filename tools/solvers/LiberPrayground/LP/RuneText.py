#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from Alphabet import white_rune, white_text, rune_map, text_map
from Rune import Rune


#########################################
#  RuneText  :  Stores multiple Rune objects. Allows arithmetic operations
#########################################

class RuneText(object):
    def __init__(self, anything):
        self._rune_sum = None
        if not anything:
            self._data = []
        elif isinstance(anything, list):
            if len(anything) > 0 and isinstance(anything[0], Rune):
                self._data = anything
            else:
                self._data = [Rune(i=x) for x in anything]
        else:
            txt = anything.strip()
            if not txt:
                self._data = []
            elif txt[0] in rune_map or txt[0] in white_rune:
                self._data = [Rune(r=x) for x in txt]
            else:
                try:
                    self._data = [
                        Rune(i=int(x)) for x in txt.strip('[]').split(',')
                    ]
                except ValueError:
                    self._data = self.from_text(txt)

        self._data_len = len(self._data)

    @classmethod
    def from_text(self, text):
        res = []
        text = text.strip().upper().replace('QU', 'CW')
        tlen = len(text)
        skip = 0
        for i in range(tlen):
            if skip:
                skip -= 1
                continue
            char = text[i]
            rune = None
            wspace = white_text.get(char, None)
            if wspace is not None:
                rune = wspace
            elif char in '\"\'\n\r\t1234567890':
                rune = char
            else:
                if char in 'TINEOA' and i + 1 < tlen:
                    bichar = char + text[i + 1]
                    rune = text_map.get(bichar, None)
                    if rune is not None:
                        char = bichar
                        skip = 1
                    elif char == 'I' and i + 2 < tlen:
                        trichar = bichar + text[i + 2]
                        rune = text_map.get(trichar, None)
                        if rune:
                            char = trichar
                            skip = 2
                if not rune:
                    rune = text_map.get(char, None)
            if not rune:
                raise ValueError(f'Unkn0n char: {i} "{char}"')
            res.append(Rune(r=rune, t=char))
        return res

    def __len__(self):
        return self._data_len

    def __getitem__(self, key):
        if isinstance(key, str):
            return [getattr(x, key) for x in self._data]
        else:
            return self._data[key]

    # def __setitem__(self, key, value):
    #     self._data[key] = value

    def __add__(self, other):
        return RuneText([x + other for x in self._data])

    def __sub__(self, other):
        return RuneText([x - other for x in self._data])

    def __invert__(self):
        return RuneText([~x for x in self._data])

    def __repr__(self):
        return f'RuneText<{len(self)}>'

    @property
    def text(self):
        return ''.join(x.text for x in self._data)

    @property
    def rune(self):
        return ''.join(x.rune for x in self._data)

    @property
    def index_no_newline(self):
        return [x.index for x in self._data if x.kind != 'l']

    @property
    def index_no_white(self):
        return [x.index for x in self._data if x.index != 29]

    @property
    def prime(self):
        return [x.prime for x in self._data]

    @property
    def prime_sum(self):
        if self._rune_sum is None:
            self._rune_sum = sum(self.prime)
        return self._rune_sum

    @property
    def data_clean(self):
        return [x if x.kind == 'r' else Rune(i=29)
                for x in self._data if x.kind != 'l']

    def description(self, count=False, index=True, indexWhitespace=False):
        return None if len(self) == 0 else \
            self.rune + (f' ({len(self)})' if count else '') + ' - ' + \
            self.text + (f' ({len(self.text)})' if count else '') + \
            (' - {}'.format(self.index_no_newline if indexWhitespace else
                            self.index_no_white)
             if index else '')

    def trim(self, maxlen):
        if self._data_len > maxlen:
            if self._rune_sum and self._rune_sum > 0:
                self._rune_sum -= sum(x.prime for x in self._data[maxlen:])
            self._data = self._data[:maxlen]
            self._data_len = maxlen

    def zip_sub(self, other):
        if len(self) != len(other):
            raise IndexError('RuneText length mismatch')
        return RuneText([x - y for x, y in zip(self._data, other._data)])

    # def equal(self, other):
    #     if len(self) != len(other):
    #         return False
    #     return all(x.index == y.index for x, y in zip(self, other))

    def enum_words(self, reverse=False):  # [(start, end, len), ...]
        start = 0
        r_pos = 0
        word = []
        for i, x in enumerate(reversed(self._data) if reverse else self._data):
            if x.kind == 'r':
                r_pos += 1
                word.append(x)
            elif x.kind == 'l':
                continue
            else:
                if len(word) > 0:  # RuneText may include \n and \r
                    yield start, i, r_pos - len(word), RuneText(word)
                    word = []
                start = i + 1


class RuneTextFile(RuneText):
    def __init__(self, file, limit=None):
        with open(file, 'r') as f:
            super().__init__(f.read()[:limit])
        self.inverted = False
        self.loaded_file = file

    def reopen(self, limit=None):
        ret = RuneTextFile(self.loaded_file, limit)
        if self.inverted:
            ret.invert()
        return ret

    def invert(self):
        self.inverted = not self.inverted
        self._rune_sum = None
        self._data = [~x for x in self._data]

    def __str__(self):
        return '@file: {} ({} bytes), inverted: {}'.format(
            self.loaded_file, len(self._data), self.inverted)


if __name__ == '__main__':
    x = RuneText('Hi there. And welc\nome, to my "world";')
    for a, z, r_pos, word in x.enum_words():
        print((a, z), r_pos, word.text)

    y = RuneTextFile(file='../_input.txt')
    print(y.loaded_file)
    print(y.prime_sum)
    print(y)
