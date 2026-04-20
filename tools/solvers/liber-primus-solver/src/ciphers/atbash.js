import {RunesAlphabet} from '../core/runesAlphabet'

export class Atbash {
    constructor() {
        if (!!Atbash.instance) {
            return Atbash.instance
        }

        Atbash.instance = this

        this.runesTranslator = new RunesAlphabet()

        return this
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

        const {decimal} = this.runesTranslator.runes.get(text)

        const newDecimal = 28 - decimal

        const newRune = this.runesTranslator.runeAlphabet[newDecimal]

        return this.runesTranslator.runes.get(newRune).rune
    }
}