# Cicada 3301 — The Definitive Research Archive

Comprehensive archive of all known Cicada 3301 materials: three puzzle rounds (2012–2014, 2016), the complete Liber Primus, all PGP-signed communications, Cicada OS contents, community solver tools, primary sources, and ongoing analysis. 5,157 files across 37 directories.

Last known authentic communication: April 2017. Liber Primus remains largely unsolved.

---

## Directory Structure

```
cicada3301/
├── puzzles/                    Puzzle rounds with walkthroughs, assets, and original images
│   ├── 2012/                   Round 1 — 4chan post through physical posters, Caesar/book ciphers
│   ├── 2013/                   Round 2 — Gematria Primus introduction, Cicada OS, 761.mp3
│   ├── 2014/                   Round 3 — 11-stage puzzle, Liber Primus release (stages 1–11 assets)
│   └── 2016/                   Unofficial/disputed round — single image (4gq25.jpg)
│
├── liber-primus/               The Sacred Book — complete in all known forms
│   ├── pages/                  75 original page images (JPG) as released from onion7
│   ├── enhanced/               High-contrast and processed versions for analysis
│   ├── original-onion7/        Raw files pulled directly from the onion7 hidden service (61 files)
│   ├── sacred-book-edition/    Community-assembled edition with English text overlays
│   ├── decoded/                Solved pages as plaintext with cipher method notes
│   ├── gifs/                   Animated GIF comparisons and steganographic analyses
│   ├── analysis/               Research notes, hints never used, map images, cipher hypotheses
│   └── tools/                  LP-specific solving utilities
│
├── pgp/                        All PGP-signed communications and the Cicada public key
│   ├── key/                    cicada-3301-public-key.asc (key ID: 7A35090F)
│   └── messages/               22 signed messages, 2012–2017 (chronologically named .asc files)
│
├── tools/                      Cryptanalysis and verification tools
│   ├── cryptanalysis/
│   │   ├── gematria/           Gematria Primus hash/analysis scripts (Python)
│   │   └── gematria-tool/      Extended gematria toolset (cloned repo)
│   ├── solvers/                Community solver projects (cloned repos)
│   │   ├── iddqd/              iddqd's master archive — LP images, transcriptions, translations, keys
│   │   ├── LiberPrayground/    Web-based LP solving environment with DB and page tools
│   │   ├── jbo-tools/          jbo's Liber Primus analysis tools
│   │   ├── idkfa/              idkfa solver library
│   │   ├── ibotpeaches/        ibotpeaches archive — ISO, keys, liber_primus, onions, scripts
│   │   ├── aadishgoel/         aadishgoel's solver collection
│   │   ├── ralphatobe/         ralphatobe's documented analysis tools
│   │   ├── liber-primus-solver Java-based LP solver with test resources
│   │   ├── liber-pr-tools-web  Web tools for LP analysis
│   │   ├── archive-tool/       General Cicada archive utility
│   │   └── complete-archive/   Comprehensive community archive (2012–2017 + extra wiki pages)
│   └── verification/
│       └── isitcicada/         PGP signature verification tool and assets
│
├── archives/                   Raw archival sources
│   ├── cijhho/                 cijhho's archive (2012–2017, Archive/, EXTRA WIKI PAGES/)
│   ├── scream314/              scream314's archive with thumbnails and assets
│   ├── wiki/                   129 wiki pages (community knowledge base)
│   └── irc-logs/               IRC chat logs from solving sessions (13 files)
│       media-coverage/
│       ├── Mainstream media/   Press coverage (Wired, NPR, BBC, etc.)
│       ├── media articles/     Full article archives as HTML/PDF
│       ├── reddit front page posts/  Reddit thread archives
│       ├── cicada3301.boards.net/    Forum archives
│       └── non text coverage/  Video/audio press coverage
│
├── papers/                     126 PDFs — research papers, reference docs, press articles,
│                               Wikipedia snapshots, and technical references used in solving
│
├── media/                      Audio and video primary sources
│   ├── audio/                  761.mp3 (Cicada OS audio), stage audio files, interconnectedness track
│   └── video/                  Phone call recording, Cicada OS boot sequence, Seoul poster hunt
│                               footage (11 MTS files), xaxanon videos, media coverage recordings
│
├── philosophy/                 Symbolism and esoteric source analysis
│   ├── onion-image-symbolism/  Analysis of imagery used in puzzle onion pages
│   └── README.md               Overview of philosophical frameworks (Blake, Gnostic, Thelemic)
│       The Wm. Blake Page - The Marriage of Heaven and Hell.pdf
│
├── community/                  Community resources index and links
│   ├── README.md               Overview of active solving communities
│   └── LINKS.md                Curated links to tools, forums, active projects
│
└── timeline/
    └── TIMELINE.md             Complete chronology of all Cicada 3301 events (2012–2023)
```

---

## What's In This Repo

### Puzzle Rounds

- **2012** — The original puzzle. Began January 4 on 4chan (/b/), ran through Caesar cipher, book code (The Lady of Shalott), steganography via outguess, a phone number, a dial-up modem tone, physical posters placed in 14 cities worldwide (Warsaw, Sydney, Seoul, Paris, Dallas, Miami, Annapolis, Los Angeles, New Orleans, Seattle, Atlanta, Hawaii, Portland, Seoul). Full image set preserved: cicada-original-4chan.jpg plus all intermediate images (BxVYf, 8D7hN, vjuNp, KXLOP, NHYLD, 1CcV1, m9sYK, cAuUz, XdNGo, sppR9, hkdgl, everywhere, and others). Outguess-extracted text files included alongside each source image. PUZZLE-2012.md is a step-by-step walkthrough.

- **2013** — Began January 4 on 4chan, introduced Gematria Primus (the runic cipher), Liber Primus's predecessor. Contains the Gematria Primus reference image, spectral analysis of 761.mp3, the Cicada OS bootable ISO (reconstructed in `cicada-os/`), and all Twitter/announcement assets. The Cicada OS directory contains: `AUDIO/761.MP3`, `DATA/_560.00`, `DATA/560.13`, `DATA/560.17`, `tmp/folly`, `tmp/wisdom`, `usr_local_bin/cicada`, `usr_local_bin/prime_echo`, and the signed message `message.txt.asc`. PUZZLE-2013.md walkthrough included.

- **2014** — The most complex round. Eleven documented stages, each with a dedicated assets directory containing the original images, outguess-extracted payloads, onion site snapshots, and READMEs. Stage highlights: stage03 (three onion XOR puzzle), stage04 (Gematria Primus matrix decode), stage06 (multi-image sequence), stage07 (magic squares + audio), stage08 (bzip2 compression), stage11 (sexagesimal encoding, 58 LP pages as 0.jpg–57.jpg). The Liber Primus was released at the end of this round (May 2014). PUZZLE-2014.md walkthrough included.

- **2016** — A single image (4gq25.jpg) posted January 5. Disputed authenticity. Outguess payload preserved.

### Liber Primus

The primary unsolved artifact. A 75-page text written in Gematria Primus runes, released May 2014.

- **pages/** — 75 original JPG page scans as distributed via the onion7 hidden service
- **enhanced/** — 6 processed versions (high contrast, sharpened, etc.) for detailed analysis
- **original-onion7/** — 61 raw files pulled directly from the onion7 Tor hidden service, including the source HTML
- **sacred-book-edition/** — Community-assembled edition in two formats: complete English remake and English text overlaid on original pages
- **decoded/** — Plaintext files for all currently solved pages, with cipher method annotations. Approximately 17 pages solved as of the last update; the remainder are either unsolved or partially constrained.
- **gifs/** — Animated comparisons and visual analysis
- **analysis/** — Research notes, `HINTS-NEVER-USED.md` (P.S. number from 2012 end message, wisdom/folly files, missing primes on telnet, trailing space anomalies, onion cookie hashes), map files (Cadaver.jpg, Echo.jpg, Regular_map.jpg, The_map.jpg)
- **GEMATRIA-PRIMUS.md** — Full cipher reference: 29-rune alphabet with numerical values, prime associations, transliteration table
- **runes-text.txt** — Raw rune transcription of the full book

### PGP — Signed Messages & Key

The Cicada 3301 PGP public key (key ID: `7A35090F`, full fingerprint: `6D854CD7933322A601C3286D181F01E57A35090F`) is at `pgp/key/cicada-3301-public-key.asc`.

22 signed messages preserved in `pgp/messages/`, covering:

| Year | Messages |
|------|----------|
| 2012 | key-announcement, key-in-front-of-you, book-code-poem, coordinates, second-chance, end-of-puzzle, final-message |
| 2013 | opening-book-code, rune-table-morse, telnet-hello, cicada-os-message (two versions) |
| 2014 | opening-book-code, onion-welcome, liber-primus-hash-block, onion5-liber-primus, final-message, liber-primus-release (May) |
| 2015 | planned-parenthood-denial |
| 2017 | final-warning, final-message |

No authentic PGP-signed messages are known after April 2017.

### Community Solver Tools

Cloned repos and standalone tools used by the active solving community:

- **iddqd** — The most comprehensive community archive. Contains `liber-primus__images--full/`, `liber-primus__images--unsolved/`, `liber-primus__index/`, `liber-primus__keys/`, `liber-primus__transcription--master/`, `liber-primus__transcription--sentences/`, `liber-primus__translation/`, `lp_outguessed/`, `byte-strings/`, `ttf/` (runic font), and per-year puzzle files (2012–2016).
- **LiberPrayground** — Web-based LP analysis environment with SQLite DB, page image sets, and results tracking.
- **jbo-tools** — jbo's Liber Primus utilities with transcription data.
- **idkfa** — Solver library with data and lib directories.
- **ibotpeaches** — Archive covering ISO, keys, liber_primus, onions, scripts, tool, and wordlists.
- **liber-primus-solver** — Java-based solver with test resources and archived attempts.
- **gematria** (cryptanalysis) — Python scripts for Gematria Primus hashing, frequency analysis, and dictionary attack. Includes `lib/analyse.py`, `lib/arg_parser.py`, `hash.py`, `dictionary.txt`, and prior outputs.
- **isitcicada** — PGP signature verification tool with bundled key assets.
- **ralphatobe** — Documented analysis tools with attached docs.

### Original Archives

- **cijhho** — Organized by year (2012–2017) plus Archive/ and EXTRA WIKI PAGES/. One of the most complete raw community archives.
- **scream314** — Archive with full thumbnail set and assets directory.

### Reference & Research

- **papers/** — 126 PDFs: press articles (NPR, The Star, Wired-era), Wikipedia snapshots (Gematria, cuneiform numbers, Gregorian calendar, base64, Fibonacci-prime spiral, Zeckendorf's theorem, Nebuchadnezzar/Newton Blake prints), technical references (thttpd, htaccess, Exif viewer), community writeups (ClevCode analysis, Marcus Wanner profile, "Meet the Man Who Solved" piece), and 4chan/paranormal board thread archives.
- **archives/wiki/** — 129 wiki pages covering: FAQ, Liber Primus solved pages, Liber Primus ideas and suggestions, origin of the Cicada logo, outguess detection visual analysis, onion ports reference, useful tools, traces of a 1990s crypto group, symbolism of cicadas and Instar, Linode server discovery logs, and the debate over the onion image meaning.
- **archives/irc-logs/** — 13 IRC log files from active solving sessions.
- **philosophy/** — Analysis of Cicada's philosophical sources: William Blake (Marriage of Heaven and Hell, Newton, Nebuchadnezzar prints), Gibson's Agrippa, Gnostic and Thelemic frameworks, and the onion image symbolism.

### Media

- **audio/** — `761.MP3` (the audio file embedded in the Cicada OS, contains spectrogram data), stage audio files (`index.mp3`, `index.3.mp3`, `c.mp3`), `3301 - Interconnectedness.mp3`, and `Cicada 3301 The Great Internet Mystery Solved!.mp3`.
- **video/** — `Voice On Phone - Cicada 3301.mp4` (the recorded phone call), `boot sequence.mp4` and `boot video.mp4` (Cicada OS boot), 11 MTS video files documenting the 2013 Seoul poster search at Yongsan and Banghwa stations (with descriptions and thumbnails), `d92c9999e6e2cc62b4a2025bcc01cf72.mp4` (xaxanon content), `Cicada 3301 Headhunting for CIA MI6 Al-Shabaab.mp4` (media coverage).

---

## Quick Start

### Verify a PGP message

```bash
# Import the Cicada public key
gpg --import pgp/key/cicada-3301-public-key.asc

# Verify any signed message
gpg --verify pgp/messages/2017-04-final-message.asc
```

### Key files by topic

| Goal | File |
|------|------|
| Gematria Primus cipher table | `liber-primus/GEMATRIA-PRIMUS.md` |
| Full LP rune transcription | `liber-primus/runes-text.txt` |
| Solved pages (plaintext) | `liber-primus/decoded/pages/page-NN.txt` |
| Original LP page images | `liber-primus/pages/` |
| Hints never used | `liber-primus/analysis/HINTS-NEVER-USED.md` |
| All PGP-signed messages | `pgp/messages/*.asc` |
| 2012 puzzle walkthrough | `puzzles/2012/PUZZLE-2012.md` |
| 2013 puzzle walkthrough | `puzzles/2013/PUZZLE-2013.md` |
| 2014 puzzle walkthrough | `puzzles/2014/PUZZLE-2014.md` |
| Cicada OS files | `puzzles/2013/cicada-os/` |
| Full event chronology | `timeline/TIMELINE.md` |

---

## Verification

**PGP Key**

```
Key ID:      7A35090F
UID:         Cicada 3301 (845145127)
Fingerprint: 6D854CD7933322A601C3286D181F01E57A35090F
Algorithm:   RSA 4096
Created:     2012-01-03
```

Every authentic Cicada 3301 message is signed with this key. The April 2017 final message is the last known use. Any message claiming to be from Cicada 3301 that cannot be verified against this key should be treated as inauthentic — numerous fakes have circulated since 2012.

---

## Current Status

**Puzzle rounds:** Three confirmed rounds completed (2012, 2013, 2014). Winners were identified each round but have not publicly identified themselves or disclosed what they found.

**2016:** A single image appeared on January 5. Its authenticity is disputed and no further activity followed.

**Liber Primus:** 75 pages. Approximately 17 pages have been decoded using Gematria Primus with various key phrases. The remaining pages are encrypted; candidate key phrases from the solved pages have not unlocked the rest. The book contains philosophical and instructional content drawing heavily on themes of self-sufficiency, privacy, and Gnostic/occult frameworks.

**Last known authentic communication:** April 2017. Two messages were posted: a warning about imposters and a final statement. No further PGP-signed messages have appeared.

**Active community:** Work continues at the Uncovering Cicada wiki, several Discord servers, and via the GitHub repositories archived here.

---

## Sources & Attribution

Materials in this archive come from:

- Cicada 3301 directly (original puzzle posts, signed messages, Liber Primus)
- **cijhho** — extensive year-by-year archive
- **scream314** — early archival work
- **iddqd** — LP transcription and translation master archive
- **ibotpeaches** — ISO and key archive
- **LiberPrayground** — community solving platform
- **jbo**, **idkfa**, **ralphatobe**, **aadishgoel** — solver tools
- Community wiki contributors (129 pages)
- Press sources reproduced for research purposes

This is an archival and educational project. All Cicada 3301 original materials are reproduced for research. Community tools and writeups belong to their respective authors. No copyright claim is made over third-party content.
