# Cicada 3301 PGP Key

## Key Details

| Field | Value |
|-------|-------|
| Key ID | `7A35090F` |
| Full Fingerprint | `6D854CD7933322A601C3286D181F01E57A35090F` |
| Available on | Public PGP keyservers |

## Importance

Every authentic Cicada 3301 communication has been signed with this key. The April 2017 message explicitly warned: "Beware false paths. Always verify PGP signature from 7A35090F."

Any message claiming to be from Cicada 3301 that is not signed with this key should be considered fraudulent.

## Verification Tool

The community built a web-based verification tool:
- **Is It Cicada?**: [cicada-solvers.github.io/isitcicada](https://cicada-solvers.github.io/isitcicada/about.html)
- **Source**: [github.com/cicada-solvers/isitcicada](https://github.com/cicada-solvers/isitcicada)

## Known PGP-Signed Messages

1. **January 2012** — First message embedded via OutGuess in the original 4chan image
2. **January 2013** — Second puzzle messages
3. **January 2014** — Third puzzle messages
4. **July 27, 2015** — Denial of involvement with Planned Parenthood hack (posted to Pastebin via @1231507051321)
5. **April 2017** — Final known message: "Beware false paths. Always verify PGP signature from 7A35090F."

## PGP Tutorial

The community wiki has a tutorial for verifying signatures:
[Uncovering Cicada Wiki — PGP Tutorial](https://uncovering-cicada.fandom.com/wiki/PGP_TUTORIAL)

## How to Verify

```bash
# Import the key
gpg --keyserver keyserver.ubuntu.com --recv-keys 7A35090F

# Verify a signed message
gpg --verify message.sig message.txt

# Or for clearsigned messages
gpg --verify message.asc
```
