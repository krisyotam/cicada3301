import {Logger} from '../../utils/logger'
import {Partitions} from '../../math/partitions'
import {writeDataToFile} from '../../utils/fileUtils'
import * as os from 'os'
import {RunesAlphabet} from '../runesAlphabet'

export class PartitionsTask {

    constructor() {
        this.logger = new Logger()
        this.partitions = new Partitions()
        this.runesAplhabet = new RunesAlphabet()
    }

    apply = taskConfiguration => {
        const {input: numberToProcess, outputFileName, options} = taskConfiguration
        const {partitionMaxLength, maxRepetitions, minVowels} = options

        let outputData = ''

        outputData = outputData
            .concat(`---- Input number:${numberToProcess}.`)
            .concat(`Options: [partitionMaxLength:${partitionMaxLength},maxRepetitions:${maxRepetitions},minVowels:${minVowels}] Partitions:`)
            .concat(os.EOL)

        const partitions = this.partitions.computePartitions(numberToProcess, options)

        for (const partition of partitions) {
            outputData = outputData.concat('Partition: ')

            const partitionElements = partition.map(x => this.runesAplhabet.runesByPrimes.get(x).letter).join(',')

            outputData = outputData.concat(partitionElements).concat(os.EOL)
        }
        this.logger.log('PartitionsTask', `Generated partitions for:${numberToProcess}`)

        writeDataToFile(outputFileName, outputData)
    }
}