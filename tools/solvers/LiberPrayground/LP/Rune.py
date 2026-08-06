#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from Alphabet import RUNES, white_rune, rune_map, primes_map


#########################################
#  Rune  :  Stores a single rune. Incl. text, prime, index, and kind
#########################################

class Rune(object):
    def __init__(self, r=None, t=None, i=None, p=None):
        self._rune = r
        self._text = t
        self._index = i
        self._prime = p
        self._kind = None  # one of: r n s l w

    def __repr__(self):
        return f'<{self._rune}, {self._text}, {self._index}, {self._prime}>'

    @property
    def rune(self):
        if self._rune is None:
            self._rune = RUNES[self._index] if self._index < 29 else '•'
        return self._rune

    @property
    def text(self):
        if self._text is None:
            r = self.rune
            try:
                self._text = rune_map[self.rune]
            except KeyError:
                self._text = white_rune.get(r, r)
        return self._text

    @property
    def index(self):
        if self._index is None:
            r = self._rune
            self._index = RUNES.index(r) if r in RUNES else 29
        return self._index

    @property
    def prime(self):
        if self._prime is None:
            self._prime = primes_map.get(self.rune, 0)
        return self._prime

    @property
    def kind(self):
        if self._kind is None:
            x = self.rune
            if x in rune_map:
                self._kind = 'r'  # rune
            elif x == '⁜':
                self._kind = 's'  # paragraph, but treat as sentence
            elif x == '⁘':
                self._kind = 's'  # sentence
            elif x == '\n' or x == '\r':
                self._kind = 'l'  # line end
            elif x in '1234567890':
                self._kind = 'n'  # number
            else:
                self._kind = 'w'  # whitespace (explicitly not n or s)
        return self._kind

    def __add__(self, o):
        if isinstance(o, Rune):
            o = o.index
        if self.index == 29 or o == 29:
            return self
        return Rune(i=(self.index + o) % 29)

    def __sub__(self, o):
        if isinstance(o, Rune):
            o = o.index
        if self.index == 29 or o == 29:
            return self
        return Rune(i=(self.index - o) % 29)

    def __invert__(self):
        return self if self.index == 29 else Rune(i=28 - self.index)
