#!/usr/bin/env python3
import LP
import itertools

WORDS_MIN_MATCH = 2
TRIM_AFTER = 40
SEQS = []
WORDS = [set()] * 13


def convert_orig_oeis(minlen=15, trim=TRIM_AFTER):
    # download and unzip: https://oeis.org/stripped.gz
    with open(LP.path.db('oeis_orig'), 'r') as f_in:
        with open(LP.path.db('oeis'), 'w') as f_out:
            for line in f_in.readlines():
                if line[0] == '#':
                    continue
                name, *vals = line.split(',')
                vals = [str(int(x) % 29) for x in vals if x.strip()][:trim]
                if len(vals) < minlen:
                    continue
                f_out.write(name + ',' + ','.join(vals) + '\n')


def load_db():  # takes 3 seconds
    print('load OEIS db ...')
    with open(LP.path.db('oeis'), 'r') as f:
        for line in f.readlines():
            vals = line.split(',')
            SEQS.append((vals[0], list(map(int, vals[1:]))))

    print('load dictionary ...')
    WORDS[1] = set(x for x in LP.RUNES)
    for i in range(2, 13):  # since 12 is the longest word
        with open(LP.path.data(f'dictionary_{i}'), 'r') as f:
            WORDS[i] = set(x.strip() for x in f.readlines())


def enum_irp_combinations(irps):
    for i in range(len(irps) + 1):
        for x in itertools.combinations(irps, i):  # 2^3
            if len(x) > 0 and x[0] - len(x) >= TRIM_AFTER:
                continue
            yield x


def get_word_splits(data, irp, reverse=False, reverse_word=False):
    new_data = []
    irps = []
    splits = []
    max_len = TRIM_AFTER  # same as trim above
    for _, _, i, w in data.enum_words(reverse=reverse):
        irp_is = [i + ii for ii, r in enumerate(w) if r.index == irp]
        if (len(w) - len(irp_is)) > max_len:  # include only full words
            break
        max_len = max_len + len(irp_is) - len(w)
        irps += irp_is
        splits.append((i, i + len(w)))
        for r in (reversed(w) if reverse_word else w):
            if r.index != 29:
                new_data.append(r.index)
    return new_data[::-1 if reverse else 1], irps, splits


# invert:         28 - rune.index
# reverse:        start chapter from the end
# reverse_word:   start it word from the end, but keep sentence direction
# allow_fails:    number of words that can be wrong
# fail_threshold: at least one word w/ len x+1 must match, else all must match
def find_oeis(irp=0, offset=0, invert=False, reverse=False, reverse_word=False,
              allow_fails=1, fail_threshold=4):
    print()
    print('irp:', irp, ' offset:', offset, ' invert:', invert,
          ' reverse:', reverse, ' reverse_word:', reverse_word,
          ' allow_fails:', allow_fails, ' fail_threshold:', fail_threshold)
    # for fname in ['p56_an_end']:
    for fname in LP.FILES_UNSOLVED:
        data = LP.RuneTextFile(LP.path.page(fname))
        if invert:
            data.invert()
        data, irps, splits = get_word_splits(data, irp, reverse, reverse_word)
        irps.reverse()  # reverse to start inserting at the end
        min_len = splits[WORDS_MIN_MATCH - 1][1]
        max_len = splits[-1][1]
        data = data[:max_len]

        print()
        print(fname, 'words:', [y - x for x, y in splits])
        for comb in enum_irp_combinations(irps):
            for oeis, vals in SEQS:  # 390k
                vals = vals[offset:]
                if len(vals) < min_len:
                    continue
                for z in comb:
                    vals.insert(z, -1)  # insert interrupts
                shortest = min(max_len, len(vals))
                for s in range(29):
                    failed = 0
                    onematch = False
                    full = []
                    for a, b in splits:
                        if b > shortest:
                            break
                        nums = [x if y == -1 else (x - y - s) % 29
                                for x, y in zip(data[a:b], vals[a:b])]
                        word = ''.join(LP.RUNES[x] for x in nums)
                        if word in WORDS[len(nums)]:
                            if len(nums) > fail_threshold:
                                onematch = True
                        else:
                            failed += 1
                            if failed > allow_fails:
                                break
                        full.append(nums)

                    if failed > allow_fails or failed > 0 and not onematch:
                        continue  # too many failed
                    print(oeis, 'shift:', s, 'irps:', comb)
                    print(' ', ' '.join(LP.RuneText(x).text for x in full))


if __name__ == '__main__':
    # convert_orig_oeis()  # create db if not present already
    load_db()
    for i in range(0, 3):
        find_oeis(irp=0, offset=i, invert=False, reverse=False,
                  reverse_word=False, allow_fails=1, fail_threshold=4)
