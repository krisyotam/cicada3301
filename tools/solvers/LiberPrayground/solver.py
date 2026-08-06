#!/usr/bin/env python3
import LP
import sys


def load_sequence_file(fname):
    with open(LP.path.data(fname), 'r') as f:
        return [int(x) for x in f.readlines()]


PRIMES = load_sequence_file('seq_primes_1000')
PRIMES_3301 = load_sequence_file('seq_primes_3301')
NOT_PRIMES = load_sequence_file('seq_not_primes')
FIBONACCI = load_sequence_file('seq_fibonacci')
LUCAS = load_sequence_file('seq_lucas_numbers')
MOEBIUS = load_sequence_file('seq_moebius')


def print_all_solved():
    def plain(slvr, inpt):
        pass

    def invert(slvr, inpt):
        inpt.invert()

    def solution_welcome(slvr, inpt):
        slvr.KEY_DATA = [23, 10, 1, 10, 9, 10, 16, 26]  # DIVINITY
        slvr.INTERRUPT = 'ᚠ'
        slvr.INTERRUPT_POS = [4, 5, 6, 7, 10, 11, 14, 18, 20, 21, 25]

    def solution_koan_1(slvr, inpt):
        slvr.KEY_DATA = [26]  # Y
        inpt.invert()

    def solution_jpg107_167(slvr, inpt):  # FIRFUMFERENFE
        slvr.KEY_DATA = [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]
        slvr.INTERRUPT = 'ᚠ'
        slvr.INTERRUPT_POS = [2, 3]

    def solution_p56_end(slvr, inpt):
        slvr.FN = lambda i, r: r - (PRIMES[i] - 1)
        slvr.INTERRUPT = 'ᚠ'
        slvr.INTERRUPT_POS = [4]

    def solve(fname, fn_solution, solver=LP.VigenereSolver):
        slvr = solver()
        inpt = LP.RuneTextFile(LP.path.page(fname))
        fn_solution(slvr, inpt)
        print(f'pages/{fname}.txt')
        print()
        io = LP.IOWriter()
        # io.QUIET = True  # or use -v/-q while calling
        io.run(slvr.run(inpt)[0])
        print()

    solve('0_warning', invert)
    solve('0_welcome', solution_welcome)
    solve('0_wisdom', plain)
    solve('0_koan_1', solution_koan_1)
    solve('0_loss_of_divinity', plain)
    solve('jpg107-167', solution_jpg107_167)
    solve('jpg229', plain)
    solve('p56_an_end', solution_p56_end, solver=LP.SequenceSolver)
    solve('p57_parable', plain)


def play_around():
    vowels = [LP.RUNES.index(x) for x in 'ᚢᚩᛁᛇᛖᛟᚪᚫᛡᛠ']
    for uuu in LP.FILES_UNSOLVED:
        inpt = LP.RuneTextFile(LP.path.page(uuu))
        print(uuu)
        print('word count:', sum(1 for _ in inpt.enum_words()))
        a = [1 if x in vowels else 0 for x in inpt.index_no_white]
        b = [a[i:i + 5] for i in range(0, len(a), 5)]
        c = [int(''.join(str(y) for y in x), 2) for x in b]
        # print('-'.join(str(x) for x in c))
        # print(LP.RuneText(c).text)
        # print(''.join('ABCDEFGHIJKLMNOPQRSTUVWXYZ___...'[x] for x in c))


def try_totient_on_unsolved():
    slvr = LP.SequenceSolver()
    # slvr.INTERRUPT = 'ᛝ'
    # slvr.INTERRUPT_POS = [1]
    # for uuu in ['15-22']:
    for uuu in LP.FILES_UNSOLVED:
        print()
        print(uuu)
        inpt = LP.RuneTextFile(LP.path.page(uuu), limit=25).data_clean
        # alldata = [x for x in inpt if x.index != 29] + [LP.Rune(i=29)] * 1

        def ec(r, i):
            p1, p2 = LP.utils.elliptic_curve(i, 149, 263, 3299)
            if p1 is None:
                return r.index
            return r.index + p1 % 29

        for z in range(29):
            # slvr.FN = lambda i, r: r - PRIMES[i] + z
            # slvr.FN = lambda i, r: LP.Rune(i=((r.prime + alldata[i + 1].prime) + z) % 60 // 2)
            # slvr.FN = lambda i, r: LP.Rune(i=(r.prime - PRIMES[FIBONACCI[i]] + z) % 29)
            # slvr.FN = lambda i, r: LP.Rune(i=(r.prime ** i + z) % 29)
            slvr.FN = lambda i, r: LP.Rune(i=(ec(r, i) + z) % 29)
            print(slvr.run(inpt)[0].text)


if '-s' in sys.argv:  # print [s]olved
    print_all_solved()
else:
    play_around()
    # try_totient_on_unsolved()
