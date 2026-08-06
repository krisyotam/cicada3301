#!/usr/bin/env python3
import os
import wave
import struct


TRACK_LEN = 146.468
SAMPLE_LEN = 6459264  # hard coded so we dont need to load the file
SAMPLING = 8  # take every x-th frame
SMOOTH_WINDOW = 2  # gaussian window size X +- window
END_TIMES = [
    10.639, 15.914, 28.937, 32.239, 33.590, 38.875, 42.408,
    45.919, 49.475, 54.763, 72.301, 74.172, 81.219, 82.339,
    92.900, 99.753, 100.654, 105.919, 114.771, 146.468]


def flip_bits(bits):
    return bits.replace('1', '_').replace('0', '1').replace('_', '0')


def bin_to_hex(binary_str):
    ret = ''
    for i in range(0, len(binary_str), 8):
        ret += '{:02X}'.format(int(binary_str[i:i + 8], 2))
    return ret


def bin_to_text(binary_str):
    ret = ''
    for i in range(0, len(binary_str), 8):
        ret += chr(int(binary_str[i:i + 8], 2))
    return ret


def oneChannel(fname, chanIdx, maxread=None):
    f = wave.open(fname, 'rb')
    c_chn = f.getnchannels()
    c_frm = f.getnframes()
    if maxread:
        c_frm = min(maxread, c_frm)
    assert f.getsampwidth() == 2
    s = f.readframes(c_frm)
    f.close()
    unpstr = '<{0}h'.format(c_frm * c_chn)
    x = list(struct.unpack(unpstr, s))
    return x[chanIdx::c_chn]


def find_db_peaks(wav_filename, threshold, write_to=None):
    res = oneChannel(wav_filename, 1)  # 100000
    if len(res) != SAMPLE_LEN:
        print('WARN: file sample rate mismatch with SAMPLE_LEN')
    with open(write_to, 'wb') as fo:
        # apply a rough gaussian smoothing
        ftlr_rng = range(-SMOOTH_WINDOW, SMOOTH_WINDOW + 1)
        for i in range(SMOOTH_WINDOW, len(res) - SMOOTH_WINDOW, SAMPLING):
            z = [res[i + x] * (1 / (abs(x) + 1)) for x in ftlr_rng]
            z = sum(z)
            f = abs(z) > 400  # threshold
            fo.write(b'\xFF' if f else b'\x00')


def fill_gaps(fname, window_size, min_count, threshold=128, write_to=None):
    window = [0] * window_size
    with open(write_to, 'wb') as fo:
        with open(fname, 'rb') as fi:
            for x in fi.read():
                window.pop(0)
                window.append(1 if x > threshold else 0)
                f = sum(window) > min_count
                fo.write(b'\xFF' if f else b'\x00')


def find_db_change(fname, threshold=128, write_to=None):
    res = [(0, False)]
    prev = False
    with open(fname, 'rb') as fi:
        for i, x in enumerate(fi.read()):
            f = x > threshold
            if f != prev:
                prev = f
                res.append((i, f))
    with open(write_to, 'w') as fo:
        for x in res:
            fo.write('{}: {}\n'.format(*x))
        # fo.write('\n'.join(['{}: {}'.format(*x) for x in res]))


def find_signal_midpoints(fname):
    res = []  # (pos, width, dist_to_prev)
    prev = 0
    with open(fname, 'r') as fi:
        lines = fi.readlines()
        for x, y in zip(lines[1::2], lines[2::2]):
            x = int(x.split(':')[0])
            y = int(y.split(':')[0])
            w = y - x
            x += int(w / 2)  # center point
            res.append((x, w, x - prev))
            prev = x
    return res


def analyze_midpoints(midpoints_list, min_frames):
    res = []  # (frame-no, time, dist-to-prev, type 'S-M-E')
    typ = 'E'  # marks first as [S]tart
    for x, width, dist in midpoints_list:
        if width < min_frames:
            continue
        typ = 'S' if typ == 'E' else 'M'
        x *= SAMPLING
        at_time = x / SAMPLE_LEN * TRACK_LEN
        dist *= SAMPLING
        for i, end_time in enumerate(END_TIMES):
            if abs(end_time - at_time) < 0.100:  # accurate within 100 ms
                typ = 'E'
                del END_TIMES[i]  # keeps count if all are used up
                break
        res.append((x, at_time, dist, typ))
    if len(END_TIMES) > 0:
        if END_TIMES[0] > res[-1][1]:
            for x in END_TIMES:
                fn = round(x / TRACK_LEN * SAMPLE_LEN)
                res.append((fn, x, fn - res[-1][0], 'E'))
        else:
            print('These endpoints were not found:')
            print(END_TIMES)  # double check
    return res


def find_common_frame_dist(arr):
    arr = [x[2] for x in arr if x[3] != 'S']
    min_dist = min(arr)
    print('Smallest common divisor: {}'.format(min_dist))
    best_match = min_dist
    best_sum = 999999
    for tx in range(min_dist - 200, min_dist + 200 + 1):
        subsum = 0
        for x in arr:
            x /= tx
            x -= round(x)
            subsum += x * x  # least square distance
        if subsum < best_sum:
            best_sum = subsum
            best_match = tx
    print('Best matching frame dist: {}'.format(best_match))
    return best_match


def analyze_db_peaks(wav_file, force=False):
    print('761')
    print('===')
    print('Track length:', TRACK_LEN)
    print('Total frames:', SAMPLE_LEN)
    if not os.path.isdir('tmp'):
        os.mkdir('tmp')
    tmp1 = 'tmp/wav-peak-analysis_1.dat'
    tmp2 = 'tmp/wav-peak-analysis_2.dat'
    tmp3 = 'tmp/wav-peak-analysis_3.txt'

    if force or not os.path.isfile(tmp1):
        find_db_peaks(wav_file, 400, write_to=tmp1)

    if force or not os.path.isfile(tmp2):
        fill_gaps(tmp1, window_size=80, min_count=20, write_to=tmp2)

    # force = True
    if force or not os.path.isfile(tmp3):
        find_db_change(tmp2, write_to=tmp3)

    points = find_signal_midpoints(tmp3)
    points = analyze_midpoints(points, min_frames=10)
    freq = find_common_frame_dist(points)
    # if times between 96.68-96.79 and 70.10-70.21 are sampled differently
    # freq /= 2  # use *2 or /2 to decrease or increase sampling frequency

    print('''
The columns are as follows:
Type  Time(s)  Time(frame)  dist-to-prev

- Type is one of [S]tart point, [M]id-point, or [E]nd point
- dist-to-prev is frame distance to previous signal divided by frame-dist
''')

    bits = ['']
    nums = [[]]
    t_between = []
    t_lengths = []
    since_start = 0

    for x, at, dist, typ in points:
        def time_diff_tpl(diff):
            return (round(diff / freq), diff / SAMPLE_LEN * TRACK_LEN)

        in_samples = round(dist / freq)
        print('{} {:.2f} {} {}'.format(typ, at, x, in_samples))
        if typ == 'S':
            # bits[-1] += '0' * (in_samples - 1)  # consider space between
            bits[-1] += '1'
            t_between.append(time_diff_tpl(dist))
            since_start = 0
        elif typ == 'E':
            bits[-1] += '0' * (in_samples - 1)
            bits[-1] += '0'  # or 1?
            missing_bits = 8 - len(bits[-1]) % 8
            if missing_bits != 8:
                # bits[-1] = '0' * missing_bits + bits[-1]
                bits[-1] += '0' * missing_bits

            since_start += dist
            t_lengths.append(time_diff_tpl(since_start))
            bits.append('')
            nums[-1].append(in_samples)
            nums.append([])
        else:
            since_start += dist
            bits[-1] += '0' * (in_samples - 1)
            bits[-1] += '1'
            nums[-1].append(in_samples)
    if bits[-1] == '':
        del bits[-1]
    if not nums[-1]:
        del nums[-1]
    print()

    print('Distance between transmissions:')
    print(', '.join(['{} ({:.2f}s)'.format(x, y) for x, y in t_between]))
    print()

    print('Lengths of transmission:')
    print(', '.join(['{} ({:.2f}s)'.format(x, y) for x, y in t_lengths]))
    print()

    print('Individual signals:')
    for i, x in enumerate(nums):
        print(' {:2}: {}'.format(i, x))
    print()

    print('Individual signals (total time):')
    for i, x in enumerate(nums):
        r = [0]
        for n in x:
            r.append(r[-1] + n)
        print(' {:2}: {}'.format(i, r[1:]))
    print()

    print('''
The following assumes that each transmission:
- begins with a 1 bit
- end is always a 0 bit
- midpoints are '0' * (dist-to-prev - 1) + '1'
- no counting in-between transmissions

Here is a representation of the individual transmissions,
as well as the full string at the end. Results are:

(0): signals are 1 bit, read left-to-right
(1): reverse bit order (aka. read right-to-left)
(2): as (0) but with inverted bits
(3): reversed and inverted

Interpreting individual transmissions:
''')

    def print_arr_w_alternates(bits, fn):
        print('0\n{}'.format([fn(x) for x in bits]))
        print('1\n{}'.format([fn(x[::-1]) for x in bits]))
        print('2\n{}'.format([fn(flip_bits(x)) for x in bits]))
        print('3\n{}'.format([fn(flip_bits(x)[::-1]) for x in bits]))
        print()

    def print_str_w_alternates(bits, fn):
        not_bits = flip_bits(bits)
        print('0: {}'.format(fn(bits)))
        print('1: {}'.format(fn(bits[::-1])))
        print('2: {}'.format(fn(not_bits)))
        print('3: {}'.format(fn(not_bits[::-1])))
        print()

    # print('As numbers:')
    # print_arr_w_alternates(bits, lambda x: int(x, 2))
    # print('As binary:')
    # print_arr_w_alternates(bits, lambda x: x)
    # print('As hex:')
    # print_arr_w_alternates(bits, lambda x: bin_to_hex(x))
    print('As text:')
    print_arr_w_alternates(bits, lambda x: bin_to_text(x))

    print('Interpreting as a whole:')
    print()
    concat = ''.join([x for x in bits])
    # print('As numbers:')
    # print_str_w_alternates(concat, lambda x: int(x, 2))
    # print('As binary:')
    # print_str_w_alternates(concat, lambda x: x)
    # print('As hex:')
    # print_str_w_alternates(concat, lambda x: bin_to_hex(x))
    print('As text:')
    print_str_w_alternates(concat, lambda x: bin_to_text(x))


# Least Significant Bit Analysis
# https://medium.com/analytics-vidhya/get-secret-message-from-audio-file-8769421205c3
def analyze_lsb(wav_filename):
    obj = wave.open(wav_filename, 'rb')
    # print(obj.getparams())
    fcount = obj.getnframes()
    fcount = 1000
    bytes = bytearray(list(obj.readframes(fcount)))
    obj.close()
    bytes = struct.unpack('H' * (len(bytes) // 2), bytes)
    # if not os.path.isdir('tmp'):
    #     os.mkdir('tmp')

    # Every frame LSB
    for z in range(1, 2):
        for u in range(z):
            txt = ''
            for i in range(u, len(bytes), z):
                f = bytes[i] & (1 << 0)
                txt += '1' if f else '0'
                # txt += chr(bytes[i])
            # print(txt)
            print(bin_to_text(txt))

    # Alternating frame LSB
    # left = bytes[::2]
    # right = bytes[1::2]
    # for z in range(1, 2):
    #     for u in range(z):
    #         txt = ''
    #         for i in range(u, len(left), 2):
    #             if i % 2 == 0:
    #                 txt += str(left[i] & 1)
    #                 # txt += chr(left[i])
    #             else:
    #                 txt += str(right[i] & 1)
    #                 # txt += chr(right[i])
    #         # print(txt)
    #         print(bin_to_text(txt))


analyze_db_peaks('audio_files/761_convergePitch_2.wav', force=False)
# analyze_lsb('audio_files/761.wav')
