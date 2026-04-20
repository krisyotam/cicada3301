# Gematria Primus

The Gematria Primus is the primary cipher system used by Cicada 3301, introduced in the 2013 puzzle. It maps 29 Anglo-Saxon (Futhorc) runes to the first 29 prime numbers.

## The Cipher Table

| # | Prime | Rune | Unicode | Letter(s) | Name |
|---|-------|------|---------|-----------|------|
| 0 | 2 | ᚠ | U+16A0 | F | Feoh |
| 1 | 3 | ᚢ | U+16A2 | U/V | Ur |
| 2 | 5 | ᚦ | U+16A6 | TH | Thorn |
| 3 | 7 | ᚩ | U+16A9 | O | Os |
| 4 | 11 | ᚱ | U+16B1 | R | Rad |
| 5 | 13 | ᚳ | U+16B3 | C/K | Cen |
| 6 | 17 | ᚷ | U+16B7 | G | Gyfu |
| 7 | 19 | ᚹ | U+16B9 | W | Wynn |
| 8 | 23 | ᚻ | U+16BB | H | Haegl |
| 9 | 29 | ᚾ | U+16BE | N | Nyd |
| 10 | 31 | ᛁ | U+16C1 | I/J | Is |
| 11 | 37 | ᛄ | U+16C4 | IO/IA | Ior |
| 12 | 41 | ᛇ | U+16C7 | EO | Eolhx |
| 13 | 43 | ᛈ | U+16C8 | P | Peorth |
| 14 | 47 | ᛉ | U+16C9 | X | Eolh |
| 15 | 53 | ᛋ | U+16CB | S/Z | Sigel |
| 16 | 59 | ᛏ | U+16CF | T | Tir |
| 17 | 61 | ᛒ | U+16D2 | B | Beorc |
| 18 | 67 | ᛖ | U+16D6 | E | Eh |
| 19 | 71 | ᛗ | U+16D7 | M | Mann |
| 20 | 73 | ᛚ | U+16DA | L | Lagu |
| 21 | 79 | ᛝ | U+16DD | NG/ING | Ing |
| 22 | 83 | ᛟ | U+16DF | OE | Ethel |
| 23 | 89 | ᛞ | U+16DE | D | Daeg |
| 24 | 97 | ᚪ | U+16AA | A | Ac |
| 25 | 101 | ᚫ | U+16AB | AE | Aesc |
| 26 | 103 | ᚣ | U+16A3 | Y | Yr |
| 27 | 107 | ᛡ | U+16E1 | EA | Ear |
| 28 | 109 | ᛠ | U+16E0 | Q (rare) | Cweorth |

## Word Separator

The bullet/dot `•` (U+2022) separates words in runic text.

## Versions

### Gematria Primus 2013
The original version published in the 2013 puzzle as a chart image (see `puzzles/2013/images/gematria-primus.jpg`).

### Gematria Primus 2014
A variation used in Liber Primus where the alphabet is reversed (Atbash-style). The community reconstructed this from solved pages:

> "From Gematria Primus 13, take the left block of three columns and stack it on top of the right block of three columns. Then, find the letter you wish to decode. Find the position of that letter in the vertical list, beginning at the top. Take that number and find the character that many characters into the list, from the bottom up."

## Cipher Methods Applied

### Direct Substitution
Simple rune-to-letter replacement using the table above. Used on the first solved pages.

### Vigenere with Prime Keys
A Vigenere cipher where the key is derived from prime numbers or prime-indexed rune values. Applied to several middle-section pages.

### Totient Shift
Uses Euler's totient function:
```
plaintext[i] = (ciphertext[i] - (prime[i] - 1)) mod 29
```
Where `prime[i]` is the i-th prime number. Used on pages 56-57 ("SOME WISDOM" section).

### Atbash (Reversed Alphabet)
Standard Atbash substitution where position `n` maps to position `28 - n` in the 29-character alphabet. Variant of the 2014 reversed Gematria.

### Combined / Multi-Layer
The unsolved pages likely require combinations of the above methods, possibly with keys derived from content not yet identified.

## Key Properties

- The alphabet has exactly **29** characters (29 is prime, the 10th prime)
- All mapped values are the first 29 primes (2 through 109)
- The sum of all 29 primes is **1,720**
- Modular arithmetic is performed mod 29
- The system is designed so that mathematical operations on prime values yield meaningful transformations

## References

- [Uncovering Cicada Wiki — Gematria Primus](https://uncovering-cicada.fandom.com/wiki/Gematria_Primus)
- [Pastebin: Rune prime values for all 58 pages](https://pastebin.com/vGMK330j)
- [Google Sheets: Rune reference](https://docs.google.com/spreadsheets/d/1QsoYQ-NkJcwEuyOgMrD6DkHU2AUktwsfnQGnTURf1bU/)
