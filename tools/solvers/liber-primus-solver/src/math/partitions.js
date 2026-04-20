import {RunesAlphabet} from '../core/runesAlphabet'
import {Logger} from '../utils/logger'
import {MultiSet} from 'mnemonist'

export class Partitions {

    buildReferenceSet = () => {
        this.referenceSet = []

        for (const key of this.runesAlphabet.runesByPrimes.keys())
            this.referenceSet.push(key)
    }

    constructor() {
        if (!!Partitions.instance) {
            return Partitions.instance
        }

        Partitions.instance = this
        this.runesAlphabet = new RunesAlphabet()
        this.logger = new Logger()

        this.buildReferenceSet()

        return this
    }

    computePartitions = (number, options = null) => {
        this.logger.log('Partitions', `Started computing partitions for:${number}`)
        let candidate = this.nearestNumberToTheLeft(number)
        let index = this.runesAlphabet.runesPrimes.indexOf(candidate)
        let firstLoop = true
        let partitions = []

        while (index >= 0) {
            if (firstLoop) {
                firstLoop = false
            } else {
                candidate = this.runesAlphabet.runesPrimes[index]
            }

            const candidatePartitions = this.innerPartitions(candidate, index, number - candidate, [candidate], [], options)

            if (candidatePartitions.length > 0)
                candidatePartitions.forEach(x => partitions.push(x))

            index--
        }

        this.logger.log('Partitions', `Done computing partitions for:${number}`)
        return partitions
    }

    innerPartitions = (candidate, currentIndex, remainder, currentPartition, partitions, options) => {
        if (remainder === 0) {
            if (options === null) {
                partitions.push(currentPartition)
            } else {
                if (this.checkPartitionAgainstOptions(currentPartition, options))
                    partitions.push(currentPartition)
            }

            return partitions
        } else if (remainder < 0) {
            return partitions
        }

        while (currentIndex >= 0) {
            const currentCandidate = this.runesAlphabet.runesPrimes[currentIndex]

            if (remainder - currentCandidate >= 0) {
                const newPartition = [...currentPartition]
                newPartition.push(currentCandidate)
                const newRemainder = remainder - currentCandidate

                this.innerPartitions(currentCandidate, currentIndex, newRemainder, newPartition, partitions, options)
            }

            currentIndex--
        }

        return partitions
    }

    checkPartitionAgainstOptions = (partition, options) => {
        const {partitionMaxLength, maxRepetitions, minVowels} = options
        let vowelsFound = 0

        if (partition.length <= partitionMaxLength) {
            let validPartition = true
            const set = MultiSet.from(partition)

            for (const element of set) {
                if (set.multiplicity(element) > maxRepetitions) {
                    validPartition = false
                    break
                } else {
                    const rune = this.runesAlphabet.runesByPrimes.get(element)
                    if (this.runesAlphabet.isVowel(rune.rune))
                        ++vowelsFound
                }
            }

            return validPartition && (vowelsFound >= minVowels)
        } else {
            return false
        }
    }

    nearestNumberToTheLeft = number => {
        if (number < this.referenceSet[0])
            return null
        else if (number > this.referenceSet[this.referenceSet.length - 1])
            return this.referenceSet[this.referenceSet.length - 1]
        else {
            for (let i = this.referenceSet.length; i >= 0; i--) {
                if (number > this.referenceSet[i])
                    return this.referenceSet[i]
            }

        }
    }
}