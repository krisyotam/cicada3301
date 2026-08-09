# Cicada Signed Messages
_Any Cicada 3301 message that is verifiable signed by their key used in the 2012 Puzzle._

* Ordered by year

## Filename notes

Two signed messages previously used Windows-illegal names containing `<`/`>`:

| Old (broken on Windows) | New |
|-------------------------|-----|
| `2013/<space>.asc` | `2013/space.asc` |
| `2014/<data-blob>.asc` | `2014/data-blob.asc` |

- `space.asc` — PGP clearsigned message whose body is empty/whitespace (the original oddity).
- `data-blob.asc` — large (~13MB) PGP clearsigned hex payload from the 2014 archive set.

If an older clone still shows the old paths as deleted, pull latest `main` or rename locally to the new paths above.
