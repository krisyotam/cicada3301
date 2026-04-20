import {RunesAlphabet} from '../core/runesAlphabet'
import {CircularArray} from '../core/circularArray'

export class Vigenere {
    constructor(key) {
        this.runesTranslator = new RunesAlphabet()
        this.key = new CircularArray(key.split(''))
    }

    apply = text => {
        let result = ''

        for (const char of text) {
            result = result.concat(this.decrypt(char))
        }

        return result
    }

    decrypt = text => {
        if (!this.runesTranslator.isRune(text))
            return text

        const keyRune = this.key.next()
        const {decimal} = this.runesTranslator.runes.get(text)
        const {decimal: keyDecimal} = this.runesTranslator.runes.get(keyRune)
        const newDecimal = (decimal - keyDecimal + this.runesTranslator.runesCount) % this.runesTranslator.runesCount

        const newRune = this.runesTranslator.runeAlphabet[newDecimal]

        return this.runesTranslator.runes.get(newRune).rune
    }
}