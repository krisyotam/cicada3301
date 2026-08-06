#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

white_rune = {'•': ' ', '⁘': '.', '⁚': ',', '⁖': ';', '⁜': '#'}
white_text = {v: k for k, v in white_rune.items()}
alphabet = [  # Using last value for display. Custom added: V
    (2, 'ᚠ', ['F']), (3, 'ᚢ', ['V', 'U']), (5, 'ᚦ', ['TH']), (7, 'ᚩ', ['O']),
    (11, 'ᚱ', ['R']), (13, 'ᚳ', ['K', 'C']), (17, 'ᚷ', ['G']),
    (19, 'ᚹ', ['W']), (23, 'ᚻ', ['H']), (29, 'ᚾ', ['N']), (31, 'ᛁ', ['I']),
    (37, 'ᛄ', ['J']), (41, 'ᛇ', ['EO']), (43, 'ᛈ', ['P']), (47, 'ᛉ', ['X']),
    (53, 'ᛋ', ['Z', 'S']), (59, 'ᛏ', ['T']), (61, 'ᛒ', ['B']),
    (67, 'ᛖ', ['E']), (71, 'ᛗ', ['M']), (73, 'ᛚ', ['L']),
    (79, 'ᛝ', ['ING', 'NG']), (83, 'ᛟ', ['OE']), (89, 'ᛞ', ['D']),
    (97, 'ᚪ', ['A']), (101, 'ᚫ', ['AE']), (103, 'ᚣ', ['Y']),
    (107, 'ᛡ', ['IO', 'IA']), (109, 'ᛠ', ['EA'])
]
text_map = {t: r for _, r, ta in alphabet for t in ta}
rune_map = {r: t for _, r, ta in alphabet for t in ta}
primes_map = {r: p for p, r, _ in alphabet}
RUNES = [r for _, r, _ in alphabet]  # array already sorted
# del alphabet  # used in playground for GP display
