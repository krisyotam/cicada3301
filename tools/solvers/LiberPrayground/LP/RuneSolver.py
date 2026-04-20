#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from RuneText import Rune, RuneText
from utils import affine_decrypt


#########################################
#  RuneSolver  :  Generic parent class handles interrupts and text highlight
#########################################

class RuneSolver(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.INTERRUPT = 'ᚠ'
        self.INTERRUPT_POS = []  # '1' for first occurrence of INTERRUPT

    def highlight_interrupt(self):
        return self.highlight_rune(self.INTERRUPT, self.INTERRUPT_POS)

    def substitute_supports_keylen(self):
        return False

    def substitute_get(self, pos, keylen, search_term, found_term, all_data):
        return found_term.zip_sub(search_term).description(count=True)

    def enum_data(self, data):
        irp_i = 0
        r_pos = -1
        for i, obj in enumerate(data):
            skip = obj.index == 29
            if not skip:
                r_pos += 1
                is_interrupt = obj.rune == self.INTERRUPT
                if is_interrupt:
                    irp_i += 1
                skip = is_interrupt and irp_i in self.INTERRUPT_POS
            yield obj, i, r_pos, skip

    def run(self, data):
        raise NotImplementedError('must subclass')
        # return RuneText(), [(start-highlight, end-highlight), ...]

    def __str__(self):
        return f'interrupt: {self.INTERRUPT}, jumps: {self.INTERRUPT_POS}'


#########################################
#  SequenceSolver  :  Decrypt runes with sequential function
#########################################

class SequenceSolver(RuneSolver):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        super().reset()
        self.FN = None

    def run(self, data):
        assert(self.FN)
        seq_i = 0
        ret = []
        for rune, i, ri, skip in self.enum_data(data):
            if not skip:
                rune = self.FN(seq_i, rune)
                seq_i += 1
            ret.append(rune)
        return RuneText(ret), []

    def __str__(self):
        return super().__str__() + f'\nf(x): {self.FN}'


#########################################
#  RunningKeySolver  :  Decrypt runes with key; handles shift, rotation, etc.
#########################################

class RunningKeySolver(RuneSolver):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        super().reset()
        self.KEY_DATA = []  # the key material
        self.KEY_SHIFT = 0  # ABCD -> DABC
        self.KEY_ROTATE = 0  # ABCD -> ZABC
        self.KEY_OFFSET = 0  # ABCD -> __ABCD
        self.KEY_POST_PAD = 0  # ABCD -> ABCD__

    def run(self, data):
        k_len = len(self.KEY_DATA)
        if k_len <= 0:
            return data, []
        k_full_len = self.KEY_OFFSET + k_len + self.KEY_POST_PAD
        k_current_pos = 0
        ret = []
        highlight = [[0, 0]]
        for rune, i, ri, skip in self.enum_data(data):
            if not skip:
                u = k_current_pos - self.KEY_OFFSET
                if u < 0 or u >= k_len or self.KEY_DATA[u] == 29:
                    self.unmodified_callback(rune)
                else:
                    key_i = (u + self.KEY_SHIFT) % k_len
                    decrypted = self.decrypt(rune.index, key_i)
                    rune = Rune(i=(decrypted - self.KEY_ROTATE) % 29)
                    if i == highlight[-1][1]:
                        highlight[-1][1] = i + 1
                    else:
                        highlight.append([i, i + 1])
                # rotate_key
                if k_full_len > 0:  # e.g., for key invert without a key
                    k_current_pos = (k_current_pos + 1) % k_full_len
            ret.append(rune)
        if highlight[0][1] == 0:
            highlight = highlight[1:]
        return RuneText(ret), highlight

    def decrypt(self, rune_index, key_index):
        raise NotImplementedError('must subclass')

    def unmodified_callback(self, rune_index):
        pass  # subclass if needed

    def key__str__(self):  # you should override this
        return RuneText(self.KEY_DATA).description(indexWhitespace=True)

    def __str__(self):
        txt = super().__str__()
        txt += f'\nkey: {self.key__str__()}'
        txt += f'\nkey offset: {self.KEY_OFFSET} runes'
        txt += f'\nkey post pad: {self.KEY_POST_PAD} runes'
        txt += f'\nkey shift: {self.KEY_SHIFT} indices'
        txt += f'\nkey rotate: {self.KEY_ROTATE} indices'
        return txt


#########################################
#  VigenereSolver  :  Decrypt runes with an array of indices
#########################################

class VigenereSolver(RunningKeySolver):
    def decrypt(self, rune_index, key_index):
        return rune_index - self.KEY_DATA[key_index]

    def substitute_supports_keylen(self):
        return True

    def substitute_get(self, pos, keylen, search_term, found_term, all_data):
        ret = [Rune(r='⁚')] * keylen
        for i, r in enumerate(found_term.zip_sub(search_term)):
            ret[(pos + i) % keylen] = r
        return RuneText(ret).description(count=True, index=False)


#########################################
#  AffineSolver  :  Decrypt runes with an array of (s, t) affine keys
#########################################

class AffineSolver(RunningKeySolver):
    def decrypt(self, rune_index, key_index):
        return affine_decrypt(rune_index, self.KEY_DATA[key_index])

    def key__str__(self):
        return self.KEY_DATA


#########################################
#  AutokeySolver  :  Decrypts runes by using previously decrypted ones as input
#########################################

class AutokeySolver(RunningKeySolver):
    def run(self, data):
        key = self.KEY_DATA[self.KEY_SHIFT:] + self.KEY_DATA[:self.KEY_SHIFT]
        key = [29] * self.KEY_OFFSET + key + [29] * self.KEY_POST_PAD
        self.running_key = key
        return super().run(data)

    def decrypt(self, rune_index, key_index):
        rune_index = (rune_index - self.running_key.pop(0)) % 29
        self.running_key.append(rune_index)
        return rune_index

    def unmodified_callback(self, rune_index):
        self.running_key.pop(0)
        self.running_key.append(rune_index)

    def substitute_supports_keylen(self):
        return True

    def substitute_get(self, pos, keylen, search_term, found_term, all_data):
        data = all_data.index_no_white
        ret = [Rune(r='⁚')] * keylen
        for o in range(len(search_term)):
            plain = search_term[o].index
            i = pos + o
            while i >= 0:
                plain = (data[i] - plain) % 29
                i -= keylen
            ret[i + keylen] = Rune(i=plain)
        return RuneText(ret).description(count=True, index=False)


if __name__ == '__main__':
    slvr = VigenereSolver()
    slvr.KEY_DATA = [1]
    print(slvr)
    txt = RuneText('hi there')
    sol = slvr.run(txt)
    print(sol[0].text)
    sol, mark = slvr.run(txt)
    print(sol.text)
    slvr.KEY_DATA = [-1]
    print(slvr.run(sol)[0].text)
    print(mark)
