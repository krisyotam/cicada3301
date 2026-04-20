export class RunesAlphabet {
    runeAlphabet = ['ᚠ', 'ᚢ', 'ᚦ', 'ᚩ', 'ᚱ', 'ᚳ', 'ᚷ', 'ᚹ', 'ᚻ', 'ᚾ', 'ᛁ', 'ᛄ', 'ᛇ', 'ᛈ', 'ᛉ', 'ᛋ', 'ᛏ', 'ᛒ', 'ᛖ', 'ᛗ', 'ᛚ', 'ᛝ', 'ᛟ', 'ᛞ', 'ᚪ', 'ᚫ', 'ᚣ', 'ᛡ', 'ᛠ']

    runes = new Map([
        ['ᚠ', {rune: 'ᚠ', decimal: 0, letter: 'F', prime: 2}],
        ['ᚢ', {rune: 'ᚢ', decimal: 1, letter: '[V,U]', prime: 3}],
        ['ᚦ', {rune: 'ᚦ', decimal: 2, letter: 'TH', prime: 5}],
        ['ᚩ', {rune: 'ᚩ', decimal: 3, letter: 'O', prime: 7}],
        ['ᚱ', {rune: 'ᚱ', decimal: 4, letter: 'R', prime: 11}],
        ['ᚳ', {rune: 'ᚳ', decimal: 5, letter: '[C,K]', prime: 13}],
        ['ᚷ', {rune: 'ᚷ', decimal: 6, letter: 'G', prime: 17}],
        ['ᚹ', {rune: 'ᚹ', decimal: 7, letter: 'W', prime: 19}],
        ['ᚻ', {rune: 'ᚻ', decimal: 8, letter: 'H', prime: 23}],
        ['ᚾ', {rune: 'ᚾ', decimal: 9, letter: 'N', prime: 29}],
        ['ᛁ', {rune: 'ᛁ', decimal: 10, letter: 'I', prime: 31}],
        ['ᛄ', {rune: 'ᛄ', decimal: 11, letter: 'J', prime: 37}],
        ['ᛇ', {rune: 'ᛇ', decimal: 12, letter: 'EO', prime: 41}],
        ['ᛈ', {rune: 'ᛈ', decimal: 13, letter: 'P', prime: 43}],
        ['ᛉ', {rune: 'ᛉ', decimal: 14, letter: 'X', prime: 47}],
        ['ᛋ', {rune: 'ᛋ', decimal: 15, letter: '[S,Z]', prime: 53}],
        ['ᛏ', {rune: 'ᛏ', decimal: 16, letter: 'T', prime: 59}],
        ['ᛒ', {rune: 'ᛒ', decimal: 17, letter: 'B', prime: 61}],
        ['ᛖ', {rune: 'ᛖ', decimal: 18, letter: 'E', prime: 67}],
        ['ᛗ', {rune: 'ᛗ', decimal: 19, letter: 'M', prime: 71}],
        ['ᛚ', {rune: 'ᛚ', decimal: 20, letter: 'L', prime: 73}],
        ['ᛝ', {rune: 'ᛝ', decimal: 21, letter: '[NG,ING]', prime: 79}],
        ['ᛟ', {rune: 'ᛟ', decimal: 22, letter: 'OE', prime: 83}],
        ['ᛞ', {rune: 'ᛞ', decimal: 23, letter: 'D', prime: 89}],
        ['ᚪ', {rune: 'ᚪ', decimal: 24, letter: 'A', prime: 97}],
        ['ᚫ', {rune: 'ᚫ', decimal: 25, letter: 'AE', prime: 101}],
        ['ᚣ', {rune: 'ᚣ', decimal: 26, letter: 'Y', prime: 103}],
        ['ᛡ', {rune: 'ᛡ', decimal: 27, letter: '[IA,IO]', prime: 107}],
        ['ᛠ', {rune: 'ᛠ', decimal: 28, letter: 'EA', prime: 109}],
    ])

    vowels = new Set(['ᚢ', 'ᚩ', 'ᛁ', 'ᛇ', 'ᛖ', 'ᛝ', 'ᛟ', 'ᚪ', 'ᚫ', 'ᛡ', 'ᛠ'])

    buildRunesByPrimes = () => {
        this.runesByPrimes = new Map()
        this.runesPrimes = []

        for (const rune of this.runes.values()) {
            this.runesByPrimes.set(rune.prime, rune)
            this.runesPrimes.push(rune.prime)
        }
    }

    constructor() {
        if (!!RunesAlphabet.instance) {
            return RunesAlphabet.instance
        }

        RunesAlphabet.instance = this
        this.runesCount = this.runeAlphabet.length
        this.buildRunesByPrimes()

        return this
    }

    isRune = candidate => this.runes.has(candidate)

    isVowel = candidate => this.vowels.has(candidate)

    translate = text => {
        let result = ''

        for (const char of text) {
            result = result.concat(this.isRune(char) ? this.runes.get(char).letter : char)
        }

        return result
    }
}