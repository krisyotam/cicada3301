# 2012 Puzzle — The First Round

**Posted**: January 4, 2012, on 4chan /x/

## The Image

A black JPEG with white text:

> Hello. We are looking for highly intelligent individuals. To find them, we have devised a test. There is a message hidden in this image. Find it, and it will lead you on the road to finding us. We look forward to meeting the few that will make it all the way through. Good luck. 3301

## Stage 1: Steganography

The image contained a hidden message extractable with **OutGuess** (steganography tool by Niels Provos). The extracted message was PGP-signed with key ID `7A35090F`, establishing the verification chain for all future Cicada communications.

The decoded message contained a URL formed from a Caesar cipher, leading to an image of a duck with the text: "WOOPS. Just decoys this way. Looks like you can't guess how to get the message out."

Closer examination of the duck image revealed another OutGuess-embedded message pointing to a subreddit.

## Stage 2: Reddit & Book Cipher

The subreddit `r/a2e7j6ic78h0j` contained posts with encoded text. The sidebar image (a Mayan numeral) and post titles contained book cipher references.

Two book ciphers were used:
1. References to line/word positions in the **King James Bible**
2. References decoded against an unknown text

These decoded to a phone number.

## Stage 3: Phone Number

Calling the number played a recorded message: "Very good. You have done well. There are three prime numbers associated with the original final.jpg image. 3301 is one of them. You will have to find the other two. Multiply all three of these numbers together and add a .com to find the next step."

The image dimensions were **509 × 503** pixels. Both are prime.
509 × 503 × 3301 = **845,145,127**

## Stage 4: 845145127.com

The website displayed a cicada image and a countdown timer. When the countdown expired, it revealed **14 GPS coordinates** pointing to physical locations worldwide.

## Stage 5: Physical Posters

At each GPS coordinate, white paper posters with cicada stencils and QR codes were found attached to streetlights and poles.

**Known poster locations**:
- Warsaw, Poland
- Paris, France
- Seoul, South Korea
- Sydney, Australia
- Hawaii, USA
- Miami, Florida, USA
- New Orleans, Louisiana, USA
- Seattle, Washington, USA
- And several others

This demonstrated that Cicada 3301 had physical operatives (or at least confederates) across multiple continents.

## Stage 6: QR Codes → Book Cipher → Tor

The QR codes on the posters contained book cipher references to William Gibson's **"Agrippa (A Book of the Dead)"** (1992).

Decoding the book cipher produced **.onion URLs** accessible only through the Tor network.

## Stage 7: The Endpoint

The .onion sites led to a PGP-gated forum. Participants who made it this far were given tasks related to:
- Privacy-preserving technology
- Cryptography implementation
- Censorship-resistant communication tools

## Notable Solver

**Joel Eriksson** (ClevCode), a Swedish cryptosecurity researcher, published the most detailed first-person account of solving the 2012 puzzle. His writeup is at [clevcode.org/cicada-3301/](https://clevcode.org/cicada-3301/).

## Key Tools Used

- **OutGuess** — JPEG steganography extraction
- **stegdetect** — steganography detection
- **GnuPG** — PGP signature verification
- **Tor Browser** — accessing .onion endpoints

## References

- [ClevCode writeup](https://clevcode.org/cicada-3301/)
- [Boxentriq walkthrough](https://www.boxentriq.com/code-breaking/cicada-3301-first-puzzle-walkthrough)
- [Fast Company profile of Eriksson](https://www.fastcompany.com/3025785/meet-the-man-who-solved-the-mysterious-cicada-3301-puzzle)
- [Uncovering Cicada Wiki](https://uncovering-cicada.fandom.com/)
- [Internet Archive: 845145127 files](https://archive.org/details/845145127)
