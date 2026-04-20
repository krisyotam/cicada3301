## OEIS

Download and unzip the OEIS [stripped.gz][oeis]. Rename the file to `oeis_orig.txt`. Run `trim_orig_oeis()` in `solver.py`, which will generate the `oeis.txt`.

[oeis]: https://oeis.org/stripped.gz


## InterruptDB

- `db_indices` : Just each index of each rune for all chapters
- `db_high` : Find IoC combinations that are as high as possible
- `db_norm` : Find IoC combinations that are close to normal english (1.7737)



### Secondary Solutions

`db_{high|norm}_secondary`

This looks at the best scoring solutions according to a threshold (high: 1.4, norm: 0.55). If an IoC score is greater than the threshold (but lower than the best solution found in the original db), we calculate and store the IoC values and interrupts for all non-optimal solutions. This calculation is performed on both IoC caclulation methods, high and norm.

_Note:_ The secondary dbs do not include the solutions from the original db.



### Pattern Analysis

#### Pattern: Modulo

`db_{high|norm}_mod_{a|b}_{mod}.{group}`

The format of a db file is `db_high_mod_a_2.0`, where `high` is the type of IoC calculation (see above), `a` is the modulo variant (see below), `2` is the modulo divisor (in this case `x % 2`), and `0` is the modulo subgroup (here: where `x % 2 == 0`). Mod 2 has two subgroups (0, 1) and mod 3 has three subgroups (0, 1, 2).

This analysis answers the question if there is an alternation of different alphabets. For example, the first alphabet could be of length 3 (ABC) and the second alphabet of length 4 (DEFG). Such an alternation between different alphabets would only repeat after 24 runes (ADBECFAGBDCEAFBGCDAEBFCG). So, a simple modulo could break simple frequency analysis with fixed key length.

Variant `a` is also called “first-interrupt-then-mod”. This method will try all 2^20 interrupt combinations, remove all interrupts in a possible candidate, and then divide the data into modulo parts. On each part we calculate the IoC and store the IoC in a separate db. This means that mod-group 0 and 1 can have different interrupts for the same key length. So, you wont be able to find a solution that fits both, but none of the solutions have a particular high IoC either...

Variant `b` is called “first-mod-then-interrupt”. In this case we first divide the data into equal parts and look for interrupts in each part separately. This will look at more data than the first method because we consider 2^20 interrupts per mod-group.

Both cases are different interpretations on how an interrupt might be handled. The first assumes that an interrupt will pause the alternation of the alphabet-sets: A1(0), interrupt, A2(0), A1(1). The second assumes that an interrupt will pause the key rotation within an alphabet-set, but still alternate the alphabet: A1(0), interrupt, A1(1), A2(0).



#### Pattern: Shift

`db_{high|norm}_pattern_shift_{keylen}.{offset}`

The format of a db file is `db_high_pattern_shift_5.0`, where `high` is the type of IoC calculation (see above), `5` is the key length, and `0` the offset of the pattern. This db misuses the key length column within the db-file to store the pattern shift variant (see below).

A pattern extends a short key to a longer one. For example, `ABCDE` (key length: 5) can be one of four possible shift variants:

- Shift by 1: `ABCDE BCDEA CDEAB DEABC EABCD`
- Shift by 2: `ABCDE CDEAB EABCD BCDEA DEABC`
- Shift by 3: `ABCDE DEABC BCDEA EABCD CDEAB`
- Shift by 4: `ABCDE EABCD DEABC CDEAB BCDEA`

(all patterns loop indefinitely)

So, since every key length `n` can have `n - 1` shift variants, a single db-file holds all shift variants for a single key length. Thus, the file gets larger the longer the key length gets. Just don't confuse the key lengh column of the db with the actual key length which is stored in the filename instead.

_Note:_ In the example above, a shift of `4` is equivalent to a shift of `-1`.

The offset `0` indicates where the pattern starts. Or simplified, how many letters are dropped from the sequence. For example, an offset of two will start with `CDE...` in the example. So, only offsets smaller than the key length make sense here. Because shifting it by the key length will yield the same pattern (letters will be different but the alphabets splits are the same).

_Note:_ All A's are in one alphabet and all B's are in another, etc.

Why is it relevant? With this technique we can check for key lengths that are far greater than we could confidently detect otherwise. Because the key, even though it changes, still uses the same alphabets. And thus, we can check key lengths that are `n^2` the length of the original key.



#### Pattern: Mirror

`db_{high|norm}_pattern_mirror_{a|b}.{offset}`

This pattern is similar to the shift pattern. Here we have two variants. Variant `a` creates the pattern `ABCDEEDCBA`. Variant `b` creates the same pattern but without double letters: `ABCDEDCB`. Again, both repeat indefinitely and the offset drops the first n letters.



#### Pattern: Autokey

`db_high_autokey_{+|-}{p|i}{_inv}`

A very brief test on reusing the previously decrypted result similar to autokey. Though autokey would use a key word with key length, here we simply use a single letter. The current rune will only be influenced by the decrypted value of the previous rune. `+`/`-` denote the operation of decryption and `p`/`i` what value was used, either the runes prime value or its index. The db has `_inv` appended if the input text was inverted prior.

As the whole text will be used, we can lower our interrupt limit to 16 without sacrificing reliability. This makes the calculations faster. But still, all variations are as uniform as the LP itself (IoC between 1.0 and 1.15). The vast majority is below 1.1 though.

Just two notable exceptions: p0-2 with `-i` and p3-7 with `-i_inv` produce higher than average IoCs consistently on all initialization letters (all of them are above 1.1).
