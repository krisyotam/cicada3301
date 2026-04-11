#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
from RuneText import RuneText
import utils


#########################################
#  IOWriter  :  handle std output with highlight etc.
#########################################

class IOWriter(object):
    def __init__(self):
        self.BREAK_MODE = None
        self.VERBOSE = '-v' in sys.argv
        self.QUIET = '-q' in sys.argv
        self.COLORS = True  # sys.stdout.isatty() doesnt matter if no highlight
        self.cur_color = None
        self.file_output = None

    def clear(self):
        self.wordsum = 0
        self.linesum = 0
        self.out_r = ''
        self.out_t = ''
        self.out_p = ''
        self.out_ps = ''

    def mark(self, color=None):
        if self.COLORS:
            m = f'\x1b[{color}' if color else '\x1b[0m'
            self.cur_color = color
            self.out_r += m
            self.out_t += m
            self.out_p += m
            # self.out_ps += m  # No. Because a word may be split-up

    def printwordsum(self):
        if self.wordsum <= 0:
            return
        self.linesum += self.wordsum
        if self.VERBOSE:
            if self.out_ps:
                self.out_ps += ' + '
            self.out_ps += str(self.wordsum)
        if utils.is_prime(self.wordsum):
            if self.VERBOSE:
                self.out_ps += '*'
            elif not self.QUIET:  # and self.wordsum > 109
                self.out_t += '__'
        self.wordsum = 0

    def run(self, data, highlight=None):  # make sure sorted, non-overlapping
        break_on = self.BREAK_MODE  # set by user
        if break_on is None:  # check None specifically, to allow '' as value
            break_on = 'l' if self.VERBOSE else 's'  # dynamically adapt mode

        self.clear()
        if not highlight:
            highlight = []
        highlight.append((len(data), len(data)))

        for i in range(len(data)):
            # Handle color highlight
            if i == highlight[0][0]:
                try:
                    color = highlight[0][2]  # e.g. 1;30m for bold black
                except IndexError:
                    color = '1;31m'  # fallback to bold red
                self.mark(color)
            elif i >= highlight[0][1]:
                self.mark()
                highlight.pop(0)

            cur = data[i]
            eow = i + 1 == len(data) or data[i + 1].kind not in 'rl'

            # Output current rune
            if cur.kind == 'l':
                if cur.kind == break_on:
                    self.write()
                elif eow:
                    self.printwordsum()
                continue  # ignore all \n,\r if not forced explicitly
            self.out_r += cur.rune
            self.out_t += cur.text
            if cur.kind != 'r':
                if self.VERBOSE:
                    self.out_p += ' '
                if cur.kind == break_on:
                    self.write()
                elif eow:
                    self.printwordsum()
                continue

            # Mark prime words
            self.wordsum += cur.prime
            if eow:
                self.printwordsum()

            # Special case when printing numbers.
            # Keep both lines (text + numbers) in sync.
            if self.VERBOSE:
                b = f'{cur.prime}'  # TODO: option for indices instead
                fillup = len(b) - len(cur.text)
                self.out_t += ' ' * fillup
                self.out_p += b
                if not eow:
                    if fillup >= 0:
                        self.out_t += ' '
                    self.out_p += '+'
        self.write()

    def write(self):
        def print_f(x=''):
            if self.file_output:
                with open(self.file_output, 'a') as f:
                    f.write(x + '\n')
            else:
                print(x)

        if not self.out_t:
            return

        if self.wordsum > 0:
            self.printwordsum()

        prev_color = self.cur_color
        if prev_color:
            self.mark()

        sffx = ' = {}'.format(self.linesum)
        if utils.is_prime(self.linesum):
            sffx += '*'
        if utils.is_emirp(self.linesum):
            sffx += '√'

        if not self.QUIET or self.VERBOSE:
            print_f()
        if not self.QUIET:
            print_f(self.out_r)
        if not (self.QUIET or self.VERBOSE):
            self.out_t += sffx
        print_f(self.out_t)
        if self.VERBOSE:
            self.out_ps += sffx
            print_f(self.out_p)
            print_f(self.out_ps)
        self.clear()
        if prev_color:
            self.mark(prev_color)


if __name__ == '__main__':
    txt = RuneText('Hi there. And welc\nome, to my world; "manatee"')
    io = IOWriter()
    io.BREAK_MODE = 's'  # 'l'
    # io.VERBOSE = True
    # io.QUIET = True
    io.run(txt, [(4, 12), (13, 27)])
