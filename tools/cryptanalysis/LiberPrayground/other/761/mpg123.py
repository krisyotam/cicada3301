from mpg123 import Mpg123
# import wave
# import struct
# https://github.com/20tab/mpg123-python


def bin_to_text(binary_str):
    ret = ''
    for i in range(0, len(binary_str), 8):
        ret += chr(int(binary_str[i:i + 8], 2))
    return ret


mp3 = Mpg123('761.MP3')
# rate, channels, encoding = mp3.get_format()
# wav = wave.open('761.wav', 'wb')
# wav.setnchannels(channels)
# wav.setframerate(rate)
# wav.setsampwidth(mp3.get_width_by_encoding(encoding))
# # fill the wave file
# for frame in mp3.iter_frames():
#     wav.writeframes(frame)
# wav.close()


txt = [''] * 8
for i, frame in enumerate(mp3.iter_frames()):
    # bytes = struct.unpack('H' * (len(frame) // 2), frame)
    for u in range(1):
        for b in range(0, len(frame), 167):
            txt[u] += '1' if frame[b] & (1 << 0) else '0'
    # for x in bytes:
    #     txt += '1' if x & 1 else '0'
    # if i > 5:
    #     break

for t in txt:
    print(bin_to_text(t))
