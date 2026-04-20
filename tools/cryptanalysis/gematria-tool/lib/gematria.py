"""
    All of GEMATRIA's alphabet logic n latin
"""

import math

class Gematria:
    """Gematria Alphabet"""

    def __init__(self) -> None:
        """https://cdn.discordapp.com/attachments/787683114914545684/787683150418542632/GematrriaPrimus.jpg"""       
        self.gematriaprimus = (
            (" ", " ", 0),
            (u"ᚠ", "f", 2),
            (u"ᚢ", "v", 3),
            (u"ᚢ", "u", 3),
            (u"ᚦ", "T", 5),  # th
            (u"ᚩ", "o", 7),
            (u"ᚱ", "r", 11),
            (u"ᚳ", "k", 13),
            (u"ᚳ", "c", 13),
            (u"ᚷ", "g", 17),
            (u"ᚹ", "w", 19),
            (u"ᚻ", "h", 23),
            (u"ᚾ", "n", 29),
            (u"ᛁ", "i", 31),
            (u"ᛄ", "j", 37),
            (u"ᛇ", "E", 41),  # eo
            (u"ᛈ", "p", 43),
            (u"ᛉ", "x", 47),
            (u"ᛋ", "z", 53),
            (u"ᛋ", "s", 53),
            (u"ᛏ", "t", 59),
            (u"ᛒ", "b", 61),
            (u"ᛖ", "e", 67),
            (u"ᛗ", "m", 71),
            (u"ᛚ", "l", 73),
            (u"ᛝ", "G", 79),  # ing
            (u"ᛝ", "G", 79),  # ng
            (u"ᛟ", "O", 83),  # oe
            (u"ᛞ", "d", 89),
            (u"ᚪ", "a", 97),
            (u"ᚫ", "A", 101),  # ae
            (u"ᚣ", "y", 103),
            (u"ᛡ", "I", 107),  # ia
            (u"ᛡ", "I", 107),  # io
            (u"ᛠ", "X", 109),  # ea
        )

        self.latsimple = (
            ("T", "th"),
            ("E", "eo"),
            ("G", "ing"),
            ("G", "ng"),
            ("O", "oe"),
            ("A", "ae"),
            ("I", "io"),
            ("I", "ia"),
            ("X", "ea"),
        )

    def gem_map(self, x, src, dest):
        """."""
        m = {p[src]: p[dest] for p in self.gematriaprimus}
        return [m[c] if c in m else c for c in x]

    def lat_to_sim(self, x):
        """Get simplified version of latin letter(supports arrays)"""
        x = x.lower().replace("qu", "kw").replace("q", "k")
        for sim in self.latsimple:
            x = x.replace(sim[1], sim[0])
        return x

    def sim_to_lat(self, x):
        """Get latin version of simplified letter(supports arrays)"""
        for sim in self.latsimple:
            x = x.replace(sim[0], sim[1])
        return x

    def run_to_lat(self, x):
        """Get runic equivalent of latin letter"""
        return self.sim_to_lat("".join(self.gem_map(x, 0, 1)))

    def run_to_num(self, x):
        """Get gematria value of rune"""
        return self.gem_map(x, 0, 2)

    def lat_to_run(self, x):
        """Get latin equivalent of rune"""
        return "".join(self.gem_map(self.lat_to_sim(x), 1, 0))

    def lat_to_num(self, x):
        """Get gematria value of latin letter"""
        # strip non alpha chars when converting to num
        x = "".join([c for c in x if c.isalpha() or c == " "])
        return self.gem_map(self.lat_to_sim(x), 1, 2)

    def num_to_run(self, x):
        """Given a value, get it's rune in the gematria alphabet"""
        return self.gem_map(x, 2, 0)

    def num_to_lat(self, x):
        """Given a value, get it's latin letter inj the gematria alphabet"""
        return self.sim_to_lat("".join(self.gem_map(x, 2, 1)))

class Cipher:
    """Cipher repr class"""

    def __repr__(self):
        return "<Cipher %s>" % (self.text)

    def __str__(self):
        return self.text

    def __init__(self, text, alpha) -> None:
        self.text = text
        self.alpha = alpha
        self.gm = Gematria()
        self.primes = lambda: (  # generates an infinite number of prime numbers
            n
            for n, _ in enumerate(iter(int, 1))  # for every value of n
            if n % 2 != 0  # but only if n is not even
            and all(
                n % p != 0 for p in range(3, int(math.sqrt(n)) + 1, 2)
            )  # not divisable by 3..sqrt(n)+1, skipping even numbers
            and n
            != 1  # 1 doesn't count as prime (we're not counting 2 specific factors, so this has to be hardcoded)
            or n == 2  # bypass the even number skip for 2.
        )

    def to_runes(self):
        """Latin to runes"""
        return Runes(self.gm.lat_to_run(self.text))

    def to_latin(self):
        """Runes to latin"""
        return Latin(self.gm.run_to_lat(self.text))

    def to_numbers(self):
        """X to Numeric value"""
        return self.gm.run_to_num(self.gm.lat_to_run(self.text))

    def sub(self, plain, cipher):
        """Substitute plain with cipher"""
        self.text = self.text.upper()
        return Cipher(self.text.translate(str.maketrans(plain, cipher)), self.alpha)

    def shift(self, n):
        """Shift Cipher"""
        return self.sub(self.alpha, self.alpha[n:] + self.alpha[:n])

    def atbash(self):
        """Atbash value of X"""
        return self.sub(self.alpha, self.alpha[::-1])

    def gematria_sum(self):
        """Gematria sum of self.text"""
        return sum([n for n in self.to_numbers() if type(n) is int])

    def gematria_sum_words(self):
        """Gematria sum of words in self.text"""
        return [Runes(w).gematria_sum() for w in self.text.split()]

    def gematria_sum_lines(self):
        """Sum of Gematria in self.text lines"""
        return [Runes(w).gematria_sum() for w in self.text.splitlines()]

    def to_index(self):
        """Get index of X in Gematria alphabet"""
        return [self.alpha.index(i.upper()) for i in self.text.upper()]

    def get_lines(self):
        """Gets lines of current text"""
        return self.text.splitlines()

    def get_words(self):
        """Gets words of current text"""
        return self.text.split()	

    def running_shift(self, key, interrupts="", skip_indices=[], decrypt=True):
        """."""
        if not key:
            return self.text

        # handles modulo
        def key_generator(key):
            while True:
                for k in key:
                    yield k

        key = key_generator(key)
        if type(interrupts) == list:
            interrupts = "".join(interrupts)
        o = ""
        i = 0

        for c in self.text:
            if c not in self.alpha or c in interrupts.upper():
                o += c
                continue
            if i in skip_indices:
                o += c
                i += 1
                continue
            c_index = self.alpha.index(c)
            # grab next key value
            shift = next(key)
            if decrypt:
                # invert the shift to decrypt
                shift = -shift
            # shift c by shift, wrap around if shift is longer than alpha
            o += self.alpha[(c_index + shift) % len(self.alpha)]
            i += 1

        return Cipher(o, self.alpha)

    def vigenere(self, key, interrupts=[], decrypt=True):
        """Vigenere cipher"""
        key = [self.alpha.index(k) for k in key.upper() if k in self.alpha]
        return self.running_shift(key, interrupts=interrupts, decrypt=decrypt)

    def totient_stream(self, interrupts="", skip_indices=[], decrypt=True):
        """Totient Encoding"""
        return self.running_shift(
            (p - 1 for p in self.primes()),
            interrupts=interrupts,
            skip_indices=skip_indices,
            decrypt=decrypt,
        )

class Runes(Cipher):
    """Runes alphabet"""
	
    def __init__(self, text) -> None:
        super().__init__(text, "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ")

class Latin(Cipher):
    """Latin Alphabet"""
    
    def __init__(self, text) -> None:
        super().__init__(text.upper(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

class Hex(Cipher):
    """Hex Cipher"""

    def __init__(self, text) -> None:
        super().__init__(text.upper(), "0123456789ABCDEF")

if __name__ == "__main__":
    r = Runes("ᚱ ᛝᚱᚪᛗᚹ ᛄᛁᚻᛖᛁᛡᛁ ᛗᚫᚣᚹ ᛠᚪᚫᚾ")
    print(r)
    print(r.gematria_sum())
    print(r.to_latin().gematria_sum())
    print(r.gematria_sum())
    print("--"*12)
    print(r)
    print(r.to_latin())
    print(r.sub("ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ123").text)
    print(r.atbash().text)
    print(r.to_numbers())
    print(r.gematria_sum())
    print(r.to_latin().gematria_sum())
    print(r.gematria_sum_words())
    print(r.gematria_sum_lines())
    # ᚻᛖᛚᛚᚩ
    h = Latin("Hello").to_runes()
    print(h.text)
    for i in range(4):
        print(h.shift(i).text)
        print(Hex("afe81723").shift(i))
