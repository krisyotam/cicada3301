import {RunesAlphabet} from '../core/runesAlphabet'

export class AffineCipher {

    constructor(a, b) {
        this.a = a
        this.b = b
        this.runesAlphabet = new RunesAlphabet()
    }

    encryptedRunes = () => {
        const encryptedRunes = new Map()

        for (const rune of this.runesAlphabet.runeAlphabet) {
            const runeToEncrypt = this.runesAlphabet.runes.get(rune)

            const encryptedDecimal = (this.a * runeToEncrypt.decimal + this.b) % this.runesAlphabet.runesCount

            encryptedRunes.set(this.runesAlphabet.runeAlphabet[encryptedDecimal], runeToEncrypt)
        }

        return encryptedRunes
    }

    apply = text => {
        let result = ''
        const encryptedRunes = this.encryptedRunes()

        for (const char of text) {
            result = result.concat(this.decrypt(char, encryptedRunes))
        }

        return result
    }

    decrypt = (text, encryptedRunes) => {
        if (!this.runesAlphabet.isRune(text))
            return text

        return encryptedRunes.get(text).rune
    }
}