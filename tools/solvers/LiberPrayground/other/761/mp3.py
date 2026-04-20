#!/usr/bin/env python3
import os
import sys

if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
    INPUT_FILE = sys.argv[1]
else:
    INPUT_FILE = 'audio_files/761.MP3'  # '761.MP3' 'index.mp3'
    # print('File not found.')
    # exit()


class MP3Header(object):
    # https://id3.org/mp3Frame
    # http://mpgedit.org/mpgedit/mpeg_format/MP3Format.html
    # http://www.mpgedit.org/mpgedit/mpeg_format/mpeghdr.htm
    # Starts with 11x 1-byte
    SYNC = ''  # 11 bit
    ID = {  # 2 bit (but reduced to 1 later)
        0b00: 'MPEG Version 2.5',
        0b01: 'reserved',
        0b10: 'MPEG Version 2 (ISO/IEC 13818-3)',
        0b11: 'MPEG Version 1 (ISO/IEC 11172-3)'}
    LAYER = {  # 2 bit (but -1 later)
        0b00: 'reserved',
        0b01: 'Layer III',
        0b10: 'Layer II',
        0b11: 'Layer I'}
    PROTECTION = {  # 1 bit
        0: 'Protected',  # 16bit CRC after header
        1: 'Not Protected'}
    BITRATE = {  # 4 bit
        # MPEG2-Layer3, M2-L2, M2-L1, M1-L3, M1-L2, M1-L1 in kbit/s
        0b0000: [0, 0, 0, 0, 0, 0],  # free
        0b0001: [8000, 32000, 32000, 32000, 32000, 32000],
        0b0010: [16000, 48000, 64000, 40000, 48000, 64000],
        0b0011: [24000, 56000, 96000, 48000, 56000, 96000],
        0b0100: [32000, 64000, 128000, 56000, 64000, 128000],
        0b0101: [64000, 80000, 160000, 64000, 80000, 160000],
        0b0110: [80000, 96000, 192000, 80000, 96000, 192000],
        0b0111: [56000, 112000, 224000, 96000, 112000, 224000],
        0b1000: [64000, 128000, 256000, 112000, 128000, 256000],
        0b1001: [128000, 160000, 288000, 128000, 160000, 288000],
        0b1010: [160000, 192000, 320000, 160000, 192000, 320000],
        0b1011: [112000, 224000, 352000, 192000, 224000, 352000],
        0b1100: [128000, 256000, 384000, 224000, 256000, 384000],
        0b1101: [256000, 320000, 416000, 256000, 320000, 416000],
        0b1110: [320000, 384000, 448000, 320000, 384000, 448000],
        0b1111: [0, 0, 0, 0, 0, 0]}  # bad
    FREQUENCY = {  # 2 bit in Hz
        # MPEG-2, MPEG-1, MPEG-2.5 (not used)
        0b00: [22050, 44100, 11025],
        0b01: [24000, 48000, 12000],
        0b10: [16000, 32000, 8000],
        0b11: [0, 0, 0]}  # reserved
    PADDING = {  # 1 bit
        0: 'Padded',  # +1 byte to frame length
        1: 'Not Padded'}
    PRIVATE = {  # 1 bit
        0: 'free',  # freely used for whatever
        1: 'free'}
    MODE = {  # 2 bit
        0b00: 'Stereo',
        0b01: 'Joint stereo (Stereo)',
        0b10: 'Dual channel (2 mono channels)',
        0b11: 'Single channel (Mono)'}
    MODE_EXTENSION = {  # 2 bit
        #       Layer I & II            Layer III
        #                      Intensity stereo  MS stereo
        # 0b00  bands 4 to 31     off             off
        # 0b01  bands 8 to 31     on              off
        # 0b10  bands 12 to 31    off             on
        # 0b11  bands 16 to 31    on              on
    }
    COPYRIGHT = {  # 1 bit
        0: 'Not Copyrighted',
        1: 'Copyrighted'}
    ORIGINAL = {  # 1 bit
        0: 'Copy of Original',
        1: 'Original'}
    EMPHASIS = {  # 2 bit
        0b00: 'none',
        0b01: '50/15 ms',
        0b10: 'reserved',
        0b11: 'CCIT J.17'}
    MULTIPLY = [144, 144, 12]  # frame length multiplier
    # FRAMESIZE = [0, 1152, 1152, 384]  # in samples
    # SLOTS = [0, 1, 1, 4]  # in bytes

    def init_from_bytes(self, b0, b1, b2, b3):
        self.emphasis = b3 & 0b11
        b3 >>= 2
        self.original = b3 & 1
        b3 >>= 1
        self.copyright = b3 & 1
        b3 >>= 1
        self.mode_extension = b3 & 0b11
        b3 >>= 2
        self.mode = b3 & 0b11

        self.private = b2 & 1
        b2 >>= 1
        self.pad = b2 & 1
        b2 >>= 1
        self.frequency = b2 & 0b11
        if self.frequency == 3:
            raise ValueError('Reserved sample rate')
        b2 >>= 2
        self.bitrate = b2 & 0b1111
        if self.frequency == 0b1111:
            raise ValueError('Invalid bitrate')

        self.protection = b1 & 1
        b1 >>= 1
        self.layer = b1 & 0b11  # Layer I-III
        if self.layer == 0:
            raise ValueError('Reserved MPEG-Layer')
        b1 >>= 2
        self.id = b1 & 0b11
        b1 >>= 2
        self.sync = (b0 << 3) + (b1 & 0b111)
        if self.sync != 0b11111111111:
            raise ValueError('Not a MP3 header')

    def __init__(self, b0, b1, b2, b3):
        self.init_from_bytes(b0, b1, b2, b3)

        i_lyr = self.layer - 1  # because arrays
        i_id = self.id & 1  # because arrays
        br = self.BITRATE[self.bitrate][i_lyr + i_id * 3]
        sr = self.FREQUENCY[self.frequency][i_id]
        self.framelength = self.MULTIPLY[i_lyr] * br / sr
        if self.pad:
            self.framelength += 1
        if i_lyr == 2:  # LAYER-1
            self.framelength *= 4
        # TODO: check whether CRC length must be added
        # if self.protection == 0:
        self.framelength = int(self.framelength)

    def as_bytes(self):
        b = self.sync
        b = b << 2 | self.id
        b = b << 2 | self.layer
        b = b << 1 | self.protection
        b = b << 4 | self.bitrate
        b = b << 2 | self.frequency
        b = b << 1 | self.pad
        b = b << 1 | self.private
        b = b << 2 | self.mode
        b = b << 2 | self.mode_extension
        b = b << 1 | self.copyright
        b = b << 1 | self.original
        b = b << 2 | self.emphasis
        return b.to_bytes(4, 'big')

    def __str__(self):
        f = '{:011b} {:02b} {:02b} {:b} {:04b} {:02b} {:b} {:b} {:02b} {:02b} {:b} {:b} {:02b}'
        return f.format(
            self.sync, self.id, self.layer, self.protection, self.bitrate,
            self.frequency, self.pad, self.private, self.mode,
            self.mode_extension, self.copyright, self.original, self.emphasis)


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


def flip_bits(bits):
    return bits.replace('1', '_').replace('0', '1').replace('_', '0')


# def read_mp3_headers(bytes, to_file):
#     with open(to_file, 'w') as fo:
#         counter = 0
#         offset = 0
#         for byte in bytes:
#             if offset < 6000:  # skip ID3
#                 offset += 8
#                 continue
#             for x in [128, 64, 32, 16, 8, 4, 2, 1]:
#                 offset += 1
#                 z = 1 if byte & x else 0
#                 if z:
#                     counter += 1
#                 else:
#                     if counter >= 13:
#                         fo.write('{}\n'.format(offset))
#                     counter = 0


# def prepare_mp3_headers(bytes, header_file):
#     with open(header_file, 'r') as f:
#         indices = [int(x) for x in f.readlines()]
#     all_of_them = []
#     for i in indices[:10]:
#         i -= 14  # beginning of header, 13 + 1 for prev bit
#         major = i // 8
#         minor = i % 8
#         raw_int = 0
#         for u in range(5):
#             raw_int += bytes[major + u] << (32 - u * 8)
#         bit_str = ''
#         for x in range(7 - minor + 32, 7 - minor, -1):
#             bit_str += '1' if raw_int & (1 << x) else '0'
#         try:
#             all_of_them.append((i, MP3Header(bit_str)))
#         except ValueError:
#             pass
#     return all_of_them


# def analyze_mp3_headers(bytes, prepared_obj):
#     txt = ''
#     for i, head in prepared_obj:
#         print('{:06d} {} {}'.format(i, head, head.framelength))
#         # if head == '00':
#         #     txt += head[7]
#     print(txt)
#     print(bin_to_text(txt))

# read_mp3_headers(bytes, to_file='mp3_header_indices.txt')
# anlz = prepare_mp3_headers(bytes, header_file='mp3_header_indices.txt')
# analyze_mp3_headers(bytes, anlz)


def parse_mp3_header(bytes):
    for i, x in enumerate(bytes):
        if x != 0xFF:
            continue
        if bytes[i + 1] >> 5 == 0b111:
            try:
                obj = MP3Header(*bytes[i:i + 4])
                next_at = i + obj.framelength
            except ValueError:
                continue
            try:
                MP3Header(*bytes[next_at:next_at + 4])
                return next_at, obj
            except ValueError:
                continue


def enum_mp3_header(bytes):
    i, header = parse_mp3_header(bytes)
    while header and i < len(bytes):
        header = MP3Header(*bytes[i:i + 4])
        yield i, header
        i += header.framelength


with open(INPUT_FILE, 'rb') as f:
    bytes = f.read()

uniq = [set(), set(), set(), set(), set(),
        set(), set(), set(), set(), set(), set()]
keyz = ['id', 'layer', 'protection', 'frequency', 'pad', 'private',
        'mode_extension', 'copyright', 'original', 'emphasis', 'framelength']
txt_chr = ''
txt_bit = ''
count_header = 0

# # Modify existing new file (a copy)
# last_i = 0
# with open(INPUT_FILE + '.modified.mp3', 'wb') as f:
#     for i, header in enum_mp3_header(bytes):
#         f.write(bytes[last_i:i])
#         header.mode_extension = 3
#         f.write(header.as_bytes())
#         last_i = i + 4

# # Split in chunks
# if not os.path.isdir('tmp'):
#     os.mkdir('tmp')
# if not os.path.isdir('tmp/mp3_frames'):
#     os.mkdir('tmp/mp3_frames')
# last_i = 0
# running_i = 0
# for i, header in enum_mp3_header(bytes):
#     with open('tmp/mp3_frames/{:06d}.mp3'.format(running_i), 'wb') as f:
#         running_i += 1
#         f.write(bytes[last_i:i])
#         last_i = i
# exit()

txt = [''] * 624
# Parse and analyze header info
for i, header in enum_mp3_header(bytes):
    # for x in range(1, 624):
    #     txt[x] += '1' if bytes[i - x] & 7 else '0'
    # print(header)
    count_header += 1
    txt_chr += chr(bytes[i - 1])
    txt_bit += '1' if bytes[i - 1] & 1 else '0'
    for i, k in enumerate(keyz):
        uniq[i].add(getattr(header, k))

for x in range(624):
    if txt[x]:
        print(bin_to_text(txt[x]))
# exit()
print('The unique values per header field:')
print({x: y for x, y in zip(keyz, uniq)})
print()


def print_bits(bits):
    print('\nBinary:')
    print(bits)
    print('\nText (normal):')
    print(bin_to_text(bits))
    print('\nText (reverse):')
    print(bin_to_text(bits[::-1]))
    print('\nText (inverse):')
    print(bin_to_text(flip_bits(bits)))
    print('\nText (reverse, inverse):')
    print(bin_to_text(flip_bits(bits[::-1])))
    print()


print('Last byte per chunk:')
print(txt_chr)
print()
print('Last bit per chunk:')
print_bits(txt_bit)

# find header fields that differ
for i in range(len(uniq) - 1, -1, -1):
    if len(uniq[i]) == 1:
        del uniq[i]
        del keyz[i]
    else:
        uniq[i] = uniq[i].pop()  # good luck if there are three

if not uniq:
    print('Nothing to do. No header changes value')
else:
    txt = [''] * len(uniq)
    # skip_once = True
    for i, header in enum_mp3_header(bytes):
        # if skip_once:
        #     skip_once = False
        #     continue
        for i, k in enumerate(keyz):
            txt[i] += '1' if getattr(header, k) == uniq[i] else '0'
    for i, k in enumerate(keyz):
        print('Header field:', k)
        print_bits(txt[i])

print()
print('Number of headers: {}'.format(count_header))
print()
