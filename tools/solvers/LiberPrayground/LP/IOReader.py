#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#########################################
#  find the longest chunk in a list of indices, which does not include an irp
#########################################

def longest_no_interrupt(data, interrupt, irpmax=0):
    def add(i):
        nonlocal ret, prev
        idx = prev.pop(0)
        if idx == 0:
            ret = []
        ret.append((i - idx, idx))

    prev = [0] * (irpmax + 1)
    ret = []
    for i, x in enumerate(data):
        if x == interrupt:
            prev.append(i + 1)
            add(i)
    add(i + 1)
    length, pos = max(ret)
    return pos, length
