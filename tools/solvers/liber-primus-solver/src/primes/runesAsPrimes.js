import {RunesAlphabet} from '../core/runesAlphabet'
import {Logger} from '../utils/logger'

export class RunesAsPrimes {
    constructor() {
        if (!!RunesAsPrimes.instance) {
            return RunesAsPrimes.instance
        }

        RunesAsPrimes.instance = this
        this.runesAlphabet = new RunesAlphabet()
        this.logger = new Logger()

        return this
    }

    wordAsSumOfPrimes = word => {
        let sum = 0
        let primes = []

        for (const rune of word) {
            const prime = this.runesAlphabet.runes.get(rune).prime
            primes.push(prime)
            sum += prime
        }

        this.logger.log('RunesAsPrimes',`wordAsSumOfPrimes. Word:${word},sum:${sum},primes sequence:${primes}`)

        return sum
    }

    wordAsProductOfPrimes = word => {
        let product = 1

        for (const rune of word) {
            product *= this.runesAlphabet.runes.get(rune).prime
        }

        return product
    }

}