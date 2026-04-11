#!/usr/bin/env python3
import sys
if True:
    sys.path.append('..')
import lib as LIB
try:
    from PIL import Image, ImageDraw
    IMG_OUT = True
except ModuleNotFoundError:
    IMG_OUT = False

ALL_OF_THEM = []
OFFSET = 0
SEPERATORS = []
PRIMES_RED = False


def write_image(dots, name, h, sz=0, width=None):
    if width is None:
        width = h
    image = Image.new('RGB', (width, h))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, h), fill='white')
    for x, p1, p2, pr in dots:
        z1 = h - 1 - p1
        z2 = h - 1 - p2
        color = 'red' if PRIMES_RED and pr else 'black'
        draw.rectangle((x - sz, z1 - sz, x + sz, z1 + sz), fill=color)
        draw.rectangle((x - sz, z2 - sz, x + sz, z2 + sz), fill=color)
    for x in SEPERATORS:
        draw.rectangle((x, 0, x + 1, h), fill='gray')
    image.save(name, 'PNG')


def draw_curve(a, b, r):
    global ALL_OF_THEM, OFFSET, SEPERATORS
    # print(f'generate curve: a={a}, b={b}, r={r}')
    img_dots = []
    txt = ''
    for x in range(r):
        p1, p2 = LIB.elliptic_curve(x, a, b, r)
        if p1 is not None:
            # print(x, p1, p2)
            txt += f'{x} {p1} {p2}\n'
            # img_dots.append((x + OFFSET, p1, p2, LIB.is_prime(x)))
            if LIB.is_prime(x):
                img_dots.append((x + OFFSET, p1, p2, True))

    # with open(f'ec-a{a}-b{b}-r{r}.txt', 'w') as f:
    #     f.write(txt)

    ALL_OF_THEM.append(((a, b, r), img_dots))
    OFFSET += len(img_dots) + 10
    SEPERATORS.append(OFFSET - 6)
    # if IMG_OUT:
    #     print(f'writing image output (a={a}, b={b}, r={r})')
    #     write_image(img_dots, f'ec-a{a}-b{b}-r{r}-pp.png', r)
    #     write_image(img_dots, f'ec-a{a}-b{b}-r{r}-lg.png', r, sz=2)
    # print()


r = 3299
t = [2, 3, 5, 7, 13, 23, 43, 79, 149, 263, 463, 829, 1481, 2593]
# t = [2, 3]
for x in t:
    ALL_OF_THEM = []
    SEPERATORS = []
    OFFSET = 0
    for y in t:
        draw_curve(a=x, b=y, r=r)

    print(f'writing image output ({x}@{t[0]}-{t[-1]} r={r}) {OFFSET}x{r}')
    just_all = [z for x, y in ALL_OF_THEM for z in y]
    write_image(just_all, f'ec-{x}-r{r}.png', r, sz=3, width=OFFSET)
