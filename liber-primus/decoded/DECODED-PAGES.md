# Liber Primus — Decoded Pages Reference

The Liber Primus ("First Book") is a 75-page runic manuscript published by Cicada 3301 in two parts. LP1 (pages 00-16, 17 pages total) was released first. LP2 (pages 17-74, 58 pages) followed. File names in the archive use two different numbering schemes: the sequential scheme (00.jpg through 74.jpg used here) and an internal LP2 scheme (0.jpg through 57.jpg). Where both appear, the sequential number is primary.

The writing system is the Runic alphabet Futhorc, decoded via Gematria Primus — a cipher table mapping runes to Latin letters developed specifically for the Cicada 3301 puzzle. Two versions of Gematria Primus exist (2013 and 2014); the 2014 version is used for most decoding.

---

## Summary Table

| Page | File | Title / Description | Status | Cipher Method |
|------|------|---------------------|--------|---------------|
| 00 | 00.jpg | Title page: "Liber Primus" | Solved | Cleartext (English); OutGuess steganographic payload present |
| 01 | 01.jpg | "A Warning" (Runes page) | Solved | Reversed Gematria substitution (Gematria Primus 2014) |
| 02 | 02.jpg | Chapter heading: "Chapter I / Intus" | Solved | Cleartext |
| 03 | 03.jpg | Welcome / Pilgrim text (part 1) | Solved | Vigenere cipher, key DIVINITY (6,19,28,19,20,19,13,3); shift up forward Gematria |
| 04 | 04.jpg | Welcome / Pilgrim text (part 2) + Wisdom | Solved | Vigenere cipher, key DIVINITY (continuation) |
| 05 | 05.jpg | "Some Wisdom" + Magic Square | Solved | Direct Gematria substitution (default) |
| 06 | 06.jpg | Koan: "A Man Decided..." (part 1) | Solved | Shift 3 down reversed Gematria |
| 07 | 07.jpg | Koan (part 2) | Solved | Shift 3 down reversed Gematria (continuation) |
| 08 | 08.jpg | Koan (part 3) | Solved | Shift 3 down reversed Gematria; OutGuess contains a separate message |
| 09 | 09.jpg | "An Instruction: Do Four Unreasonable Things" | Solved | Shift 3 down reversed Gematria |
| 10 | 10.jpg | "The Loss of Divinity" — Consumption section | Solved | Direct Gematria substitution (default) |
| 11 | 11.jpg | Consumption / Preservation sections | Solved | Direct Gematria substitution (default) |
| 12 | 12.jpg | Preservation / Adherence sections | Solved | Direct Gematria substitution (default) |
| 13 | 13.jpg | Adherence conclusion + Some Wisdom + An Instruction | Solved | Direct Gematria substitution (default) |
| 14 | 14.jpg | Koan: "The I" (part 1) | Solved | Vigenere cipher, key FIRFUMFERENFE (13-char key) |
| 15 | 15.jpg | Koan: "The I" (part 2) | Solved | Vigenere cipher, key FIRFUMFERENFE (continuation) |
| 16 | 16.jpg | "An Instruction: Question All Things" + Magic Square | Solved | Direct Gematria substitution (default) |
| 17 | 17.jpg | LP2 begins — Section heading | Unsolved | Unknown cipher |
| 18 | 18.jpg | LP2 content | Unsolved | Unknown cipher |
| 19 | 19.jpg | LP2 content | Unsolved | Unknown cipher |
| 20 | 20.jpg | LP2 content (two sections) | Unsolved | Unknown cipher |
| 21 | 21.jpg | LP2 content | Unsolved | Unknown cipher |
| 22 | 22.jpg | LP2 content | Unsolved | Unknown cipher |
| 23 | 23.jpg | LP2 content | Unsolved | Unknown cipher |
| 24 | 24.jpg | LP2 content | Unsolved | Unknown cipher |
| 25-31 | 25.jpg-31.jpg | LP2 extended section | Unsolved | Unknown cipher |
| 32 | 32.jpg | Contains a 4x4 number grid | Unsolved | Unknown cipher; grid may be a magic square |
| 33-39 | 33.jpg-39.jpg | LP2 extended section | Unsolved | Unknown cipher |
| 40-43 | 40.jpg-43.jpg | LP2 section | Unsolved | Unknown cipher |
| 44-74 | 44.jpg-74.jpg | LP2 remaining pages | Unsolved | Unknown cipher |

Note: Pages 56-57 (LP2 internal indices 39-40) are reported by some researchers as solved using the totient function, but no verified plaintext appears in the primary archive sources.

---

## Solved Pages — Full Decoded Text

### Page 00 — Title Page (00.jpg)

**Cipher:** Cleartext English.

```
Liber Primus
```

**OutGuess steganographic payload:** A PGP-signed message is hidden in the image using OutGuess steganography. The payload is a PGP signed block with a SHA1 hash — it contains no readable text body, only a hash and signature. The image was used as a puzzle checkpoint to confirm authenticity.

---

### Page 01 — A Warning (01.jpg)

**Cipher:** Substitution using reversed Gematria Primus 2014. Each rune is first read with Gematria Primus 2013 (yielding intermediate Latin characters), then the 2014 table maps those to the final English letters.

**Decoded plaintext:**

```
A WARNING

BELIEVE NOTHING FROM THIS BOOK
EXCEPT WHAT YOU KNOW TO BE TRUE
TEST THE KNOWLEDGE
FIND YOUR TRUTH
EXPERIENCE YOUR DEATH
DO NOT EDIT OR CHANGE THIS BOOK
OR THE MESSAGE CONTAINED WITHIN
EITHER THE WORDS OR THEIR NUMBERS
FOR ALL IS SACRED
```

**Gematria line sums** (emirps marked with *):

```
BELIEVE NOTHING FROM THIS BOOK      = 757*
EXCEPT WHAT YOU KNOW TO BE TRUE     = 1009*
TEST THE KNOWLEDGE                  = 691
FIND YOUR TRUTH                     = 353*
EXPERIENCE YOUR DEATH               = 769*
DO NOT EDIT OR CHANGE THIS BOOK     = 911
OR THE MESSAGE CONTAINED WITHIN     = 1051
EITHER THE WORDS OR THE NUMBERS     = 859
FOR ALL IS SACRED                   = 677
```

An OutGuess steganographic payload is also present in this image (another PGP signed block, hash only, no plaintext body).

---

### Page 02 — Chapter Heading: Intus (02.jpg)

**Cipher:** Cleartext English.

```
Chapter I

Intus
```

"Intus" is Latin for "within" or "inside." This is the title of Chapter 1. An OutGuess payload is present in the image.

---

### Pages 03-04 — Welcome / The Great Journey (03.jpg, 04.jpg)

**Cipher:** Vigenere cipher using key DIVINITY. Key values: 6, 19, 28, 19, 20, 19, 13, 3. Applied as a shift-up forward Gematria. Every cleartext F in the output corresponds to the rune ᚠ (F) and must be skipped during decoding.

These two pages form a single continuous section. Page 03 contains the first portion; page 04 continues directly.

**Page 03 decoded plaintext:**

```
WELCOME:
WELCOME, PILGRIM TO THE GREAT JOURNEY
TOWARD THE END OF ALL THINGS.
IT IS NOT AN EASY TRIP, BUT FOR THOSE WHO
FIND THEIR WAY HERE IT IS A NECESSARY ONE.
ALONG THE WAY YOU WILL FIND AN END TO ALL
STRUGGLE AND SUFFERING, YOUR INNOCENCE, YOUR
ILLUSIONS, YOUR CERTAINTY, AND YOUR REALITY.
ULTIMATELY, YOU WILL DISCOVER AN END TO SELF.
```

**Page 04 decoded plaintext:**

```
IT IS THROUGH THIS PILGRIMAGE THAT WE SHAPE
OURSELVES AND OUR REALITIES.
JOURNEY DEEP WITHIN AND YOU WILL ARRIVE OUTSIDE.
LIKE THE INSTAR, IT IS ONLY THROUGH GOING
WITHIN THAT WE MAY EMERGE:

WIDSOM:
YOU ARE A BEING UNTO YOURSELF.
YOU ARE A LAW UNTO YOURSELF.
EACH INTELLIGENCE IS HOLY.
FOR ALL THAT LIVES IS HOLY.

:AN INSTRUCTION: COMMAND YOUR OWN SELF :
```

**Gematria line sums for page 03:**

```
WELCOME                                                          = 317
WELCOME, PILGRIM TO THE GREAT JOURNEY TOWARD THE END OF ALL THINGS
                                                                 = 2113
IT IS NOT AN EASY TRIP, BUT FOR THOSE WHO FIND THEIR WAY HERE IT IS A NECESSARY ONE
                                                                 = 2647
ALONG THE WAY YOU WILL FIND AN END TO ALL STRUGGLE AND SUFFERING, YOUR INNOCENCE, YOUR ILLUSIONS, YOUR CERTAINTY, AND YOUR REALITY.
                                                                 = 4577 (composite)
ULTIMATELY, YOU WILL DISCOVER AN END TO SELF                     = 1791 (composite)
```

OutGuess note: The page 03 OutGuess payload is a JPEG image embedded in the steganographic channel. The OutGuess output from page 04 yields approximately 7.5kB of garbage (no meaningful content).

---

### Page 05 — Some Wisdom / Magic Square (05.jpg)

**Cipher:** Direct substitution using Gematria Primus (default). This page contains text and a 5x5 magic square. Some entries in the square are written as runes, others as Arabic numerals.

**Decoded plaintext:**

```
SOME WISDOM
THE PRIMES ARE SACRED
THE TOTIENT FUNCTION IS SACRED
ALL THINGS SHOULD BE ENCRYPTED

KNOW THIS:

272       138       SHADOWS    131       151
AETHEREAL BUFFERS   VOID       CARNAL    18
226       OBSCURA   FORM       245       MOBIUS
18        ANALOG    VOID       MOURNFUL  AETHEREAL
151       131       CABAL      138       272
```

**Magic square in numeric form** (Gematria Primus values):

```
272     138     341     131     151
366     199     130     320     18
226     245     91      245     226
18      320     130     199     366
151     131     341     138     272
```

This 5x5 matrix matches a matrix found in the Out-of-Band (OOB) data from the third Cicada onion server.

**Gematria line sums** (emirps marked with *):

```
SOME WISDOM                     = 468
THE PRIMES ARE SACRED           = 853
THE TOTIENT FUNCTION IS SACRED  = 1039
ALL THINGS SHOULD BE ENCRYPTED  = 1237*
KNOW THIS                       = 157*
```

No OutGuess payload present.

---

### Pages 06-09 — The Koan: A Man Decided (06.jpg, 07.jpg, 08.jpg, 09.jpg)

**Cipher:** Shift 3 down reversed Gematria (Gematria Primus 2014, reversed, then shifted).

Pages 06 through 09 form a single continuous Zen koan, followed by an instruction. The full decoded text spans all four pages.

**Decoded plaintext (full koan, pages 06-09):**

```
A KOAN

A MAN DECIDED TO GO AND STUDY WITH A MASTER.
HE WENT TO THE DOOR OF THE MASTER
"WHO ARE YOU WHO WISHES TO STUDY HERE?"
ASKED THE MASTER.
THE STUDENT TOLD THE MASTER HIS NAME.
"THAT IS NOT WHAT YOU ARE THAT IS ONLY WHAT YOU ARE CALLED.
WHO ARE YOU WHO WISHES TO STUDY HERE?" HE ASKED AGAIN.
THE MAN THOUGHT FOR A MOMENT, AND REPLIED
"I AM A PROFESSOR."
"THAT IS WHAT YOU DO, NOT WHAT YOU ARE"
REPLIED THE MASTER. "WHO ARE
YOU WHO WISHES TO STUDY HERE?"
CONFUSED, THE MAN THOUGHT SOME MORE.
FINALLY, HE ANSWERED, "I AM A HUMAN BEING."
"THAT IS ONLY YOUR SPECIES, NOT WHO YOU ARE.
WHO ARE YOU WHO WISHES TO STUDY HERE?"
ASKED THE MASTER AGAIN.
AFTER A MOMENT OF THOUGHT, THE PROFESSOR REPLIED
"I AM A CONSCIOUSNESS INHABITING AN ARBITRARY BODY."
"THAT IS MERELY WHAT YOU ARE NOT WHO YOU ARE"
WHO ARE YOU WHO WISHES TO STUDY HERE?"
THE MAN WAS GETTING IRRITATED. "I AM," HE STARTED,
BUT HE COULD NOT THINK OF ANYTHING ELSE TO SAY,
SO HE TRAILED OFF. AFTER A LONG PAUSE THE MASTER REPLIED
"THEN YOU ARE WELCOME TO COME STUDY."

AN INSTRUCTION

DO FOUR UNREASONABLE THINGS EACH DAY.
```

**OutGuess notes:**
- Pages 06, 07, 09: OutGuess yields garbage output (no meaningful payload).
- Page 08 OutGuess contains a distinct puzzle message:

```
For those who have fallen behind:

TL BE IE OV UT HT RE ID TS EO ST PO SO YR
SL BT II IY T4 DG UQ IM NU 44 2I 15 33 9M

Good luck.

3301
```

---

### Pages 10-13 — The Loss of Divinity (10.jpg, 11.jpg, 12.jpg, 13.jpg)

**Cipher:** Direct substitution using default Gematria Primus. The runes were not additionally encrypted beyond the substitution cipher.

These four pages form a single continuous section. The text on pages 10-12 runs together; page 13 is the conclusion of the section followed by a new "Some Wisdom" and an instruction.

**Page 10 decoded plaintext:**

```
THE LOSS OF DIVINITY: THE CIRCUMFERENCE PRACTICES THREE BEHAVIORS WHICH CAUSE THE LOSS OF DIVINITY.

CONSUMPTION: WE CONSUME TOO MUCH BECAUSE WE BELIEVE THE FOLLOWING TWO ERRORS WITHIN THE DECEPTION.

    1 WE DO NOT HAVE ENOUGH
      OR THERE IS NOT ENOUGH
```

**Page 11 decoded plaintext:**

```
    2 WE HAVE WHAT WE HAVE NOW BY LUCK, AND WE WILL NOT
      BE STRONG ENOUGH LATER TO OBTAIN WHAT WE NEED.

MOST THINGS ARE NOT WORTH CONSUMING:

PRESERVATION: WE PRESERVE THINGS BECAUSE WE BELIEVE WE ARE WEAK.
IF WE LOSE THEM WE WILL NOT BE STRONG ENOUGH TO GAIN THEM AGAIN.
THIS IS THE DECEPTION.
```

**Page 12 decoded plaintext:**

```
MOST THINGS ARE NOT WORTH PRESERVING:

ADHERENCE: WE FOLLOW DOGMA SO THAT WE CAN BELONG AND BE RIGHT.
OR WE FOLLOW REASON SO WE CAN BELONG AND BE RIGHT.

THERE IS NOTHING TO BE RIGHT ABOUT.
TO BELONG IS DEATH.

IT IS THE BEHAVIORS OF CONSUMPTION, PRESERVATION, AND ADHERENCE
```

**Page 13 decoded plaintext:**

```
(CE THAT HAVE US LOSE OUR PRIMALITY AND THUS OUR DIVINITY:)

SOME WISDOM: AMASS GREAT WEALTH. NEVER BECOME ATTACHED TO WHAT YOU OWN. BE
PREPARED TO DESTROY ALL THAT YOU OWN:

AN INSTRUCTION: PROGRAM YOUR MIND. PROGRAM REALITY
```

**OutGuess payloads (pages 10, 11, 12, 13):** Each of these four pages contains a PGP-signed OutGuess message. The text body of each is identical:

```
Create one Tor hidden service that can accept CGI file uploads.

When this hidden service returns and can accept input, post the
three magic squares and the URL to your Tor hidden service here.

Work alone.
```

Each page then presents a different 4x4 border matrix (the "magic squares" requested). Three distinct grids appear across the four pages:

Grid 1 (pages 10 and 13):
```
1111111111111111
110    12    101
1              1
112    14    121
1              1
110    12    101
1111111111111111
```

Grid 2 (page 11):
```
3333333333333333
310    12    103
3              3
312    14    123
3              3
310    12    103
3333333333333333
```

Grid 3 (page 12):
```
0000000000000000
010    12    100
0              0
012    14    120
0              0
010    12    100
0000000000000000
```

---

### Pages 14-15 — The Koan: The I (14.jpg, 15.jpg)

**Cipher:** Vigenere cipher with key FIRFUMFERENFE (13 characters, values: 29, 19, 25, 29, 28, 10, 29, 11, 25, 11, 20, 29, 11). Applied as shift-up forward Gematria. Every cleartext F corresponds to ᚠ and must be skipped.

These two pages form a single continuous koan.

**Page 14 decoded plaintext:**

```
A KOAN: DURING A LESSION: THE MASTER EXPLAINED THE I:
"THE I IS THE VOICE OF THE CIRCUMFERENCE," HE SAID.
WHEN ASKED BY A STUDENT TO EXPLAIN WHAT THAT MEANT,
THE MASTER SAID "IT IS A VOICE INSIDE YOUR HEAD."
"I DON'T HAVE A VOICE IN MY HEAD," THOUGHT THE STUDENT,
AND HE RAISED HIS HAND TO TELL THE MASTER.
THE MASTER STOP
```

**Page 15 decoded plaintext:**

```
PED THE STUDENT, AND SAID "THE VOICE THAT JUST SAID YOU HAVE
NO VOICE IN YOUR HEAD, IS THE I."
AND THE STUDENTS WERE ENLIGHTENED:
```

No OutGuess payloads on pages 14 or 15.

---

### Page 16 — An Instruction: Question All Things (16.jpg)

**Cipher:** Direct substitution using default Gematria Primus. Not encoded beyond the rune substitution.

**Decoded plaintext:**

```
AN INSTRUCTION: QUESTION ALL THINGS.
DISCOVER TRUTH INSIDE YOURSELF.
FOLLOW YOUR TRUTH.
IMPOSE NOTHING ON OTHERS.

KNOW THIS:
434    1311    312    278    966
204    812     934    280    1071
626    620     809    620    626
1071   280     934    812    204
966    278     312    1311   434
```

The 5x5 number grid is a magic square of Gematria values. No OutGuess payload.

---

## Unsolved Pages — LP2 (Pages 17-74)

All pages from 17.jpg through 74.jpg remain unsolved as of the available archive data. Their rune text has been transcribed but no valid cipher key or decryption method has been confirmed.

### What is known about LP2

**Pages 17-19** (LP2 internal: 0.jpg-2.jpg): Three pages of dense rune text. The OutGuess on 17.jpg yields approximately 58.2kB of garbage output. Pages 18-19 have no OutGuess payload.

**Page 20** (LP2 internal: 3.jpg): Two distinct runic sections on the same image. No OutGuess.

**Pages 20-23** (LP2 internal: 3.jpg-6.jpg): Four-page section with dense runic content beginning with a three-rune word "ᛈᛞᚦ". The OutGuess on 21.jpg yields 58.2kB garbage. Pages 20, 22, 23 have no OutGuess.

**Pages 23-24** (LP2 internal: 6.jpg-7.jpg): Two-page section. No OutGuess.

**Pages 25-31** (LP2 internal: 8.jpg-14.jpg): Seven-page section. The longest continuous runic passage in LP2. The runes include an embedded Arabic numeral "7" within the runic text on what appears to be page 31.

**Page 32** (LP2 internal: 15.jpg): Contains a section heading and a 4x4 numeric grid:
```
3258    3222    3152    3038
3278    3299    3298    2838
3288    3294    3296    2472
4516    1206    708     1820
```
These numbers may represent Gematria sums or function as cipher keys.

**Pages 32-39** (LP2 internal: 15.jpg-22.jpg): Eight-page section. Unsolved.

**Pages 40-43** (LP2 internal: 23.jpg-26.jpg): Four-page section. Unsolved.

**Pages 44-74**: All remaining LP2 pages. Unsolved. The archive does not contain decoded text for any of these pages.

---

## Notable Observations and Meta-Clues

### Trailing spaces encode prime sequences

Several Cicada 3301 messages surrounding the Liber Primus use trailing whitespace characters to encode sequences of prime numbers. This is a meta-cipher applied to outer puzzle messages, not to the book text itself:

- 2012 final message: trailing spaces encode `0, 2, 3, 5, 7, 11, 13, (1, 1, 2), 11, 0, 7, 0, 5, 0, 3, 2`
- 2013 telnet "hello" message: trailing spaces encode `5, 3, 2, 2, 3, 5`
- 2014 message.txt.asc: trailing spaces encode `2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37` (first 11 primes)
- 2015 Planned Parenthood statement: trailing spaces encode `5, 3, 2, 5, 7`

### Gematria Primus and sacred numbers

Page 01 makes this structural: each line of "A Warning," when its letters are summed using Gematria Primus values, produces a prime number. Several lines produce emirps (primes that remain prime when their digits are reversed). This property was intentional — the content and the numeric structure of the content were designed together.

### The totient function

Page 05 states "THE TOTIENT FUNCTION IS SACRED." Euler's totient function φ(n) counts the integers up to n that are coprime to n. Some researchers have reported that pages near the end of LP2 were solved using the totient function as a key derivation step, but no verified plaintext from those pages appears in the primary source material reviewed here.

### The "circumference" concept

The solved pages use "the circumference" as a technical term for the ordinary, socially-conditioned self — the self defined by names, roles, species membership, and material attachments. The koan on pages 06-09 demonstrates that stripping away these layers (name, profession, species, consciousness-in-a-body) until nothing remains is the point. The koan on pages 14-15 identifies "the I" with the voice of the circumference. The three behaviors in pages 10-13 (consumption, preservation, adherence) are framed as what causes "loss of divinity."

### The FIRFUMFERENFE key

The Vigenere key for pages 14-15 is FIRFUMFERENFE — a phonetic corruption of "CIRCUMFERENCE," the central concept throughout Chapter 1. The substitution of "CIRC" with "FIRF" and "ENCE" with "ENFE" mirrors the cipher rule from pages 03-04: the ᚠ (F) rune must be skipped when those ciphers are applied, because F cannot be encrypted with the DIVINITY key. The key for pages 14-15 encodes a self-referential hint to that decoding rule.

### Missing primes in the 2013 telnet shell

The CICADA OS telnet "primes" shell listed primes with a gap: it skipped all primes between 71 and 1229. The two primes that had extra leading spaces were 31 and 3259. This anomaly was noted by researchers but never definitively connected to a specific decryption step in LP2.

### OutGuess in LP2

Several LP2 pages contain OutGuess payloads, but the extracted data yields large blocks of garbage output. This suggests either a different steganographic tool, image modification after initial release, or the OutGuess layer in LP2 requires a passphrase not yet discovered.

---

## Source Files

- Primary source: `/home/krisyotam/dev/cicada3301/archives/scream314/liber_primus.md`
- Cipher table analysis: `/home/krisyotam/dev/cicada3301/archives/scream314/pages_and_ciphers.md`
- Rune transcriptions: `/home/krisyotam/dev/cicada3301/liber-primus/runes-text.txt`
- Hint analysis: `/home/krisyotam/dev/cicada3301/archives/scream314/hints_never_used.md`
- Gematria Primus reference: `/home/krisyotam/dev/cicada3301/liber-primus/GEMATRIA-PRIMUS.md`
