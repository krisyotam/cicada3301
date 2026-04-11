# Liber Primus — The Unsolved Book

**Released**: May 2, 2014
**Pages**: 58 image files of Elder Futhark runes
**Solved**: ~17 pages
**Unsolved**: ~41 pages

## What Is It

Liber Primus ("First Book" in Latin) is a 58-page document rendered entirely in Elder Futhark runes using the Gematria Primus cipher system. It was released as the culmination of the 2014 Cicada 3301 puzzle and represents the primary unsolved challenge.

## Where to Get the Pages

- **Internet Archive**: [archive.org/details/liber-primus](https://archive.org/details/liber-primus)
- **Dropbox archive**: [dropbox.com/sh/lkta4q921vliyuw](https://www.dropbox.com/sh/lkta4q921vliyuw/AADmZ1YUHXWSjSizlMGZHXVMa?dl=0)
- **GitHub**: [cicada-solvers/The-Complete-Cicada3301-Archive](https://github.com/cicada-solvers/The-Complete-Cicada3301-Archive)
- **Pastebin (rune prime values for all 58 pages)**: [pastebin.com/vGMK330j](https://pastebin.com/vGMK330j)
- **Google Sheets (rune reference)**: [docs.google.com/spreadsheets/d/1QsoYQ-NkJcwEuyOgMrD6DkHU2AUktwsfnQGnTURf1bU](https://docs.google.com/spreadsheets/d/1QsoYQ-NkJcwEuyOgMrD6DkHU2AUktwsfnQGnTURf1bU/edit#gid=480300769)

## Decoded Content

The solved pages reveal philosophical and esoteric text. Example from the opening:

> WELCOME, PILGRIM, TO THE GREAT JOURNEY TOWARD THE END OF ALL THINGS. IT IS NOT AN EASY TRIP, BUT FOR THOSE WHO FIND THEIR WAY HERE IT IS A NECESSARY ONE. ALONG THE WAY YOU WILL FIND AN END TO ALL STRUGGLE AND SUFFERING, YOUR INNOCENCE, YOUR ILLUSIONS, YOUR CERTAINTY, AND YOUR REALITY. ULTIMATELY YOU WILL DISCOVER AN END TO SELF.

Another decoded passage:

> SOME WISDOM: THE PRIMES ARE SACRED. THE TOTIENT FUNCTION IS SACRED. ALL THINGS SHOULD BE ENCRYPTED. KNOW THIS...

## Decryption Methods Used on Solved Pages

The ~17 decoded pages used combinations of:

1. **Gematria Primus transliteration** — direct rune-to-letter mapping
2. **Vigenère cipher** with prime-based keys
3. **Euler's totient function**: `decimal[i] = (decimal[i] - (primes[i] - 1)) % 29`
4. **Atbash cipher** variants (reversed alphabet substitution)

The last two pages (56.jpg and 57.jpg) were among the first solved.

## Why It's Hard

The unsolved pages appear to require a breakthrough in approach. The community has exhausted straightforward applications of the known cipher methods. Leading theories for the remaining pages include:

- Multi-layered encryption combining several methods
- Keys derived from content not yet identified
- Steganographic data hidden in the page images themselves (not just the rune text)
- A fundamentally different cipher system for the remaining sections

## Solving Tools

See [tools/](tools/) for community-built Liber Primus analysis tools.

Key repositories:
- [cicada-solvers/LiberPrTools-Web](https://github.com/cicada-solvers/LiberPrTools-Web) — web-based deciphering tools
- [cicada-solvers/idkfa](https://github.com/cicada-solvers/idkfa) — rtkd's toolset
- [r4nd0mD3v3l0p3r/LiberPrimusSolver](https://github.com/r4nd0mD3v3l0p3r/LiberPrimusSolver) — automated solving attempts
- [relikd/LiberPrayground](https://github.com/relikd/LiberPrayground) — solving playground

## References

- [Uncovering Cicada Wiki — Liber Primus](https://uncovering-cicada.fandom.com/wiki/Liber_Primus)
- [How the solved pages were solved](https://uncovering-cicada.fandom.com/wiki/How_the_solved_pages_of_the_Liber_Primus_were_solved)
- [Unsolved pages](https://uncovering-cicada.fandom.com/wiki/Liber_Primus_Unsolved_Pages)
- [What Happened Liber Primus (Post 2014)](https://uncovering-cicada.fandom.com/wiki/What_Happened_Liber_Primus_(Post_2014))
