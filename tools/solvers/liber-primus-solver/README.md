# LiberPrimusSolver
an attempt at solving Cicada 3301 Liber Primus

This program is Free Software, released under GNU GPL v3

## How to run it

You need both [Node](https://nodejs.org/en/) and 
[Yarn](https://yarnpkg.com/lang/en/)

- Clone the repository
- launch `yarn install`
- use `yarn start` to launch the program
- use `yarn test` to run tests

## How it works

Liber Primus Solver (LPS from now on) can execute various tasks.

## How to configure it

the **data** folder contains various txt files.

aWarning.txt, firstKoan.txt, welcome.txt and unsolved.txt are excerpts from the
Liber Primus. First three files contain the sections that were decrypted, while
unsolved.txt contains all the pages that have yet to be decrypted.
You can add more if you want to test different parts of the Liber Primus.

LPS uses [rtkd transcription of Liber Primus](https://github.com/rtkd/iddqd/tree/master/liber-primus__transcription--master).

output files will be placed into a folder named output, that will be created in
data folder as soon as the program is launched.

## The tasks.txt file

**Tasks.txt** is the file used to program LPS. Each row should be a valid JSON,
and represents a task that LPS will execute.
There is another file, **tasks.examples.txt**. This one contains the tasks that were executed by me against the
unsolved pages, along with some comments and observations.


### Type of tasks available

Each row of the tasks.txt file should contain **taskType**, used to specify which type of task the line is
for. Here's all the available task types:

#### decrypt

This one is used to try and decrypt the Liber Primus text using (and chaining) various cipher methods

The general form of a line is as follows:
```json
{"inputFileName":"firstKoan.txt", "outputFileName": "atbashThenShift","taskType":"decrypt", "pipeline":[{"cipher":"atbash"}, {"cipher":"shift", "by":"3"}]}
```

- **inputFileName** is the file the task will use as input (it must be an excerpt
from Liber Primus that follows the transcription rules mentioned above)
- **outputFileName** is the name of the file that will contain the task outcome.
Two files will be generated, one outputFileName.rune.txt containing the result
in runes, another outputFileName.txt containing plain english. At the moment,
runes with multiple possible translations (eg ᛋ that translates
 both into S and Z) will be written with both values enclosed in square brakets.
 An example from the First Koan: ᚹ-ᚣᛠᚹᛟ will appear as A-[C,K]OAN
 Future version will handle these situations in a better way.
- **pipeline** this contains the list of ciphers that will be applied to the input
file. They should appear in the order you want them to be executed.

#### partitions

This type is used to generate all the partitions of a given number, against the set of prime numbers
that can be deduced from the runic alphabet, i.e. {2,...109}

this task type can be configured using the following variables:
- **outputFileName** the name of the file that will contain the found partitions
- **partitionMaxLength** this specifies the max length allowed for a partition to be stored in the output
file
- **maxRepetitions** this is used to instruct the LPS about how many times a rune can appear in a single
partition
- **minVowels** the min number of vowels that must be present in a partition for it to be saved
- **input** the number used to compute the partitions

task example:

```json
{"outputFileName": "18","taskType":"partitions", "options":{"partitionMaxLength":9,"maxRepetitions":2,"minVowels":1}, "input":18}
```

## Supported ciphers

### direct

it simply translates runes into english.

task example:

```json
{"inputFileName":"someInputFile.txt", "outputFileName": "someOutputFile", "pipeline":[{"cipher":"direct"}]}
```

### Atbash

it decrypts the text using Atbash

task example:

```json
{"inputFileName":"someInputFile.txt", "outputFileName": "someOutputFile", "pipeline":[{"cipher":"atbash"}]}
```

### Caesar cipher (shift cipher)

it decrypts the text using Caesar cipher. You must specify the shift value.

task example:
```json
{"inputFileName":"someInputFile.txt", "outputFileName": "someOutputFile", "pipeline":[{"cipher":"shift", "by":"3"}]}
```

### Vigenere

it decrypts the text using Vigenere cipher. You must specify:

- the key to use (use runic alphabeth)
- how the input text should be splitted. 
Valid values are **word, clause, paragraph, segment, chapter, line, page**.
These names come from [rtkd transcription of Liber Primus](https://github.com/rtkd/iddqd/tree/master/liber-primus__transcription--master).
At the beginning of each chunk, the key index is reset. 
Segment is probably the most useful one.

task example:
```json
{"inputFileName":"welcome.txt","outputFileName": "vigenere", "pipeline":[{"cipher":"vigenere", "key":"ᛞᛁᚢᛁᚾᛁᛏᚣ", "splitBy":"segment"}]}
```

### Hill cipher

it decrypts the text using Hill cipher. You must specify:

- how the input text should be splitted (refer to the same section in Vigenere cipher for details)
- the matrix to use
- whether the provided matrix is the decryption matrix or not; if not, its modular inverse
will be computed and used

task example:
```json
{"inputFileName":"unsolved.txt","outputFileName": "matrix", "pipeline":[{"cipher":"hill", "splitBy":"segment","isDecryptionMatrix":false, "matrix":[[272, 138, 341, 131, 151],[366, 199, 130, 320, 18],[226, 245, 91, 245, 226],[18, 320, 130, 199, 366],[151, 131, 341, 138, 272]]}]}
```

## A final word

It's unlikely, but should LPS help you discovering new things about the Liber Primus, please share the gathered information
with the community.