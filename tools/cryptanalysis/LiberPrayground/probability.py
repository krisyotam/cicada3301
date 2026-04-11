#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import LP

INVERT = False
KEY_MAX_SCORE = 0.05
AFF_MAX_SCORE = 0.04
session_files = []

db_i = LP.InterruptIndices()
if True:
    db = LP.InterruptDB.load('db_norm')
    IOC_MIN_SCORE = 0.55
else:
    db = LP.InterruptDB.load('db_high')
    IOC_MIN_SCORE = 1.35


#########################################
#  Perform heuristic search on the keylength, interrupts, and key
#########################################

def break_cipher(fname, candidates, solver, key_fn):
    slvr = solver()
    io = LP.IOWriter()
    io.QUIET = True
    inpt = LP.RuneTextFile(LP.path.page(fname))
    if INVERT:
        inpt.invert()
    data = inpt.index_no_white

    if key_fn.__name__ == 'GuessAffine':
        key_max_score = AFF_MAX_SCORE
    else:
        key_max_score = KEY_MAX_SCORE

    def fn_similarity(x):
        return LP.Probability(x).similarity()

    outfmt = 'IoC: {}, interrupt: {}, count: {}, solver: {}'
    for irp_count, score, irp, kl, skips in candidates:
        stops, upto = db_i.consider(fname, 28 - irp if INVERT else irp, irp_count)
        print(outfmt.format(score, LP.RUNES[irp], len(stops), key_fn.__name__))
        testcase = data[:upto]
        for x in reversed(skips):
            testcase.pop(stops[x - 1])
        key_score, key = key_fn(testcase).guess(kl, fn_similarity)
        if key_score > key_max_score:
            continue
        prio = (1 - key_score) * max(0, score)
        print(f'  key_score: {prio:.4f}, {key}')
        print(f'  skip: {skips}')
        txtname = f'{fname}_{prio:.4f}.{key_fn.__name__}.{irp}_{kl}'
        if INVERT:
            txtname += '.inv'
        while txtname in session_files:
            txtname += '.'
        session_files.append(txtname)
        outfile = LP.path.tmp(txtname)
        with open(outfile, 'w') as f:
            f.write(
                f'{irp}, {kl}, {score:.4f}, {key_score:.4f}, {key}, {skips}\n')
        io.file_output = outfile
        slvr.INTERRUPT = LP.RUNES[irp]
        slvr.INTERRUPT_POS = skips
        slvr.KEY_DATA = key
        io.run(slvr.run(inpt)[0])


def pattern_solver(fname, irp=0):
    orig = LP.RuneTextFile(LP.path.page(fname))
    # orig = LP.RuneText('ᛄᚹᚻᛗᛋᚪ-ᛋᛁᚫᛇ-ᛋᛠᚾᛞ-ᛇᛞ-ᛞᚾᚣᚹᛗ.ᛞᛈ-ᛝᛚᚳᚾᛗᚾᚣ-ᛖᛝᛖᚦᚣᚢ-ᚱᚻᛁᚠ-ᛟᛝ-ᛚᛖᚫᛋᛚᚳᛋᛇ.ᚣᚾᚻᛄᚾᚳᛡ-ᚷᚳᛝ-ᛈᛝ-ᛡᚷᚦᚷᛖ.ᚻᛠᚣ-ᛄᛞᚹᛒ-ᛇᛄᛝᚩᛟ.ᛗᛠᚣᛋᛖᛚᚠ-ᚾᚫᛁ-ᛄᚹᚻᚻᛚᛈᚹᚠ-ᚫᚩᛡᚫᛟ-ᚷᛠ-ᚪᛡᚠᛄᚱᛏᚢᛈ.ᛏᛈ-ᛇᛞ-ᛟᛗᛇᛒᛄᚳᛈ.ᛉᛟ-ᛒᚻᚱᛄᚣ-ᚾᚱ-ᚾᛡᛈᛈ-ᛚᛉᛗᛞ-ᛟᛝ-ᚷᛁᚱᚩᚹᛗ-ᚠᛇᚣ-ᚣᛝᛒ-ᛁ-ᚠᚾᚹᚢ-ᛠᚾᛈᚠᚻ.ᚫᛋᛄᚪᚻ-ᛒᛖᛋᚻᛠ-ᛄᛗ-ᛟᛡᚹᚪᛡ-ᛄᛋᛖᚢᛗ-ᛏᛖᛉᚪ-ᛞᛟᛉᚾᚠ-ᚱᛡᛒᛚᚩᛈᛝ-ᛋᛄᛚᛗ-ᛞᚱᛗᛗ-ᛒᛈ-ᛁᛉᚱᛄᛝ.ᛋᛇᚪ-ᛗᚠᚻᚣᚹᛉᛞ-ᛡᛁᚷᚪ-ᚩᚱ-ᚪᚾᚹᛇᛋᛞᛄᚷ-ᛡ-ᛖᚫᛄ-ᛞᛟᛁᚻᚹᛝ-ᛠᛈᛏ-ᚪᛗᛗᛚᛚᚪᛞ.ᛁᛠᛈᚷᛞ-ᛗᚣᛄᚳᚹᛚ-ᚻᛋᛟᛗ-ᚣᚫᛝᛚ-ᛠᛁᛝᛝᚪ-ᚳᛗ-ᚢᚫᛋ-ᛉᛠᚱ-ᛇᛡᛄᚻᛗᚾ-ᚻᛗᛝᛚ-ᛇᛞ-ᛟᚢᚣᚪᚷᚱ-ᛡᚷ-ᚷᛠ-ᛚᚻᛒ.ᛡᛒ-ᚩᛁᛄ-ᛗᛟᛉᚩᚣ-ᛞᚩ-ᚳᛗ-ᚾᛗᚩ-ᚷᛠ-ᛚᚱᚠᚷ-ᛁᚫᛗᛉ-ᛁᛠᚹᛚ-ᛖᛝᚾᛟᛗᚾ-ᛄᚾ-ᚾᚳᛚᛝ-ᛡ-ᚷᛞᛗᚱᚻᚩ-ᛗᛞᛠᚫᛞ-ᛞᚱᛗᛗ-ᚣᚪ-ᛗᛉᚢᛞᛇᚹ-ᛟᚱᛏᚱᛟᚢᛉᛗᛚᛈᛉᛝ.ᛏᛖ-ᛗᛋᚣ-ᚹᛁ-ᚹᛝ-ᛋᛇᛄᚳᛁᛋᛝ.ᛄᛚᚹ-ᚷᚠᛝ-ᚫᚷᛚᛡᛁᛡ.ᛖᚠᚣ-ᛉᛝᚻᛄᚾᛈᚠ-ᛉᚣ-ᛚᛄᛞᛝᛞᚪ-ᚩᛈ-ᚻᛟ-ᛖᚻᚱᚹ-ᛚᚷᚳ-ᛒᛈᛏᚻ-ᚠᛋᛠᚣᛋᚠ-ᛏᚷᛈᚪᛒ.')
    # orig = LP.RuneText('ᛇᚦ-ᛒᛏᚣᚳ-ᛇᛚᛉ-ᛄᛚᚦᚪ-ᛋᚱᛉᚦ-ᚦᛄᚻ-ᛉᛗ-ᛏᛞᛋ-ᚣᚾ-ᚣᛟᛇᛈᛟᛚ-ᛈᚹᛚᚪᛗ-ᚪᛉᛁᛇᛝᚢᚱᛉ.ᛞᛄ-ᚻᛠᚪᛚ.ᚠᛚ-ᚩᛋᚾ-ᚫᛞᛋᛁᛞᚹᚾᚪᚪ-ᚱᛟᚻ-ᛚᚠᛚᚳᛟᚱ-ᚣᛏ-ᚹᛏᛝᚣ-ᚳᚩ-ᛄᚷᛟ-ᛖ-ᚫᚻᚦᛠ-ᛒᛠᛁ-ᛁᚩᛡ-ᛗᛉᚠᚷᛁ-ᚣᚣᛋᛇᛗᛠᚹ.ᛇᚪ-ᛇᛉᛡ-ᛄᚾᛇᛁᛇᚫ-ᛋᚱᚹ-ᛝᚣᚦ-ᛠᛁᛄᛚᚢᛄ-ᚻᛇᛚᛟ-ᛒᛠᛒᛚ-ᚩᛈᛈ-ᚢᚻᛚ-ᛡᚾᛚ-ᛒᚦᚱᚠᚦᚫ-ᛞᚳ-ᛄᚳᚷ-ᚹᚫ-ᚱᛉᚣᛖᚱ.ᛒᛝᚹ-ᛟᚳᚫᚹᛈᚢ-ᚱᛋᛒ-ᚷᚦᚳᛏᛏᛠᚹ-ᚱᚣᛞ-ᚣᛠᛄ-ᛋ-qᚪᛚᚾᛖᛄᚪ-ᛇᚻᛖ-ᛏᛠᛈ-ᛝᛉᚾᚳ-ᛋᚾᚹᚦᚾ-ᚣᛞᛝᚣ-ᛠᛠᛡ-ᛉᛁᛚᚢᚩ.ᛗᛉᚦ-ᛒᛝᛇᛠᛟ-ᛁᛟᛏ-ᛠᛏᛄ-ᚫᚳᛉᛝᛖᚠ-ᛇᚠ.ᛄᛄᛝᛟᛡᛟ-ᛠᛖᚫ-ᚦᛏᛠᛗ-ᛁᛏᚩᛒᛡ-ᛝᛟ-ᛉᚠᛇᚷᛗᛠ-ᚠᛖ-ᚳᛖᛖᚾᛠᛁᚪᛟ-ᛉᚣ-ᚢᛁ.ᛒᛏ.ᛒᛠ-ᛠᛁᚢᛗ-ᛞᛟᛋᛠᚷᚠᛇᚫ-ᛏᚪ-ᛇᚦ-ᛒᚪᛟᚩᛗ.ᛟᚳᛇ-ᛞᛞ-ᛋᚱᛁᛋᚦ-ᛇᛒ-ᚳᛒᛟ-ᚳᛟᚳᚷᛇ.ᛗᛉᚦ-ᛞᚦᛉᛈᛚᛈᛚᛁᚢ-ᚳᛞᛡᛝᚻᚷ-ᛞᚪ-ᚳᛟᚳᛁᛟᛞ-')
    data = orig.index_no_newline
    if False:  # longest uninterrupted text
        pos, lg = LP.longest_no_interrupt(data, interrupt=0, irpmax=0)
        data = data[pos:pos + lg]
    else:  # from the beginning
        data = data[:970]

    whitespace_i = [i for i, x in enumerate(data) if x == 29]
    data = [x for x in data if x != 29]

    def fn_similarity(x):
        return LP.Probability(x).similarity()

    prnt_fmt = 'kl: {}, pattern-n: {}, IoC: {:.3f}, dist: {:.4f}, offset: {}, key: {}'
    print(fname)
    # gr = LP.GuessPattern(data)
    for kl in range(3, 19):
        for kl_shift in range(1, kl):
            # Find proper pattern
            res = []
            for offset in range(kl):  # up to keylen offset
                parts = LP.GuessPattern.groups(data, kl, kl_shift, offset)
                score = sum(LP.Probability(x).IC() for x in parts) / kl
                if score > 1.6 and score < 2.1:
                    res.append((score, parts, offset))

            # Find best matching key for pattern
            for score, parts, off in res:
                sc, key = LP.GuessPattern.guess(parts, fn_similarity)
                if sc < 0.1:
                    print(prnt_fmt.format(kl, kl_shift, score, sc, off,
                                          LP.RuneText(key).text))
                    solved = LP.GuessPattern.zip(data, key, kl, kl_shift, off)
                    for i in whitespace_i:
                        solved.insert(i, 29)
                    print(' ', LP.RuneText(solved).text)


#########################################
#  main
#########################################
for fname in [
    'p0-2',  # ???
    'p3-7',  # ???
    'p8-14',  # ???
    'p15-22',  # ???
    'p23-26',  # ???
    'p27-32',  # ???
    'p33-39',  # ???
    'p40-53',  # ???
    'p54-55',  # ???
    # '0_warning',  # invert
    # '0_welcome',  # V8
    # '0_wisdom',  # plain
    # '0_koan_1',  # invert + shift
    # '0_loss_of_divinity',  # plain
    # 'jpg107-167',  # V13
    # 'jpg229',  # plain
    # 'p56_an_end',  # totient
    # 'p57_parable',  # plain
]:
    pattern_solver(fname)
    # break
    continue
    # NGramShifter().guess(data, 'ᚠ')
    if fname not in db:
        print(fname, 'not in db.')
        continue
    print()
    print(f'loading: {fname}')
    candidates = [x for x in db[fname] if x[1] >= IOC_MIN_SCORE and x[2] == 0]
    if not candidates:
        maxscore = max(x[1] for x in db[fname])
        print('No candidates. Highest score is only', maxscore)
        continue
    break_cipher(fname, candidates, LP.AffineSolver, LP.GuessAffine)
    break_cipher(fname, candidates, LP.VigenereSolver, LP.GuessVigenere)
