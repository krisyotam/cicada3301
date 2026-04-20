import {writeFile} from '../../utils/fileUtils'
import {Vigenere} from '../../ciphers/vigenere'
import {HillCipher} from '../../ciphers/hillCipher'
import {Logger} from '../../utils/logger'
import {Atbash} from '../../ciphers/atbash'
import {Shift} from '../../ciphers/shift'
import {LiberPrimusSplitter} from '../liberPrimusSplitter'

export class DecryptTask {

    constructor(fileData) {
        this.fileData = fileData
        this.logger = new Logger()
        this.atbash = new Atbash()
        this.shift = new Shift()
        this.liberPrimusSplitter = new LiberPrimusSplitter()
    }

    apply = taskConfiguration => {
        const {inputFileName, outputFileName} = taskConfiguration
        let fileData = this.fileData(inputFileName)
        let splitterChar = ''

        for (const task of taskConfiguration.pipeline) {
            const {cipher} = task

            if (cipher === 'direct') {
            } else if (cipher === 'atbash') {
                fileData = this.atbash.apply(fileData)
            } else if (cipher === 'shift') {
                const {by} = task

                fileData = this.shift.apply(fileData, Number(by))
            } else if (cipher === 'vigenere') {
                fileData = this.vigenereCipher(task, fileData, splitterChar)
            } else if (cipher === 'hill') {
                fileData = this.hillCipher(task, fileData, splitterChar)
            } else {
                throw 'unsupported or malformed cipher'
            }
        }

        writeFile(outputFileName, fileData)
    }

    vigenereCipher = (task, fileData) => {
        const {splitBy, key} = task
        const splitterChar = this.liberPrimusSplitter.getSplitterChar(splitBy)
        let result = ''

        for (const chunk of this.liberPrimusSplitter.split(fileData, splitBy)) {
            const vigenere = new Vigenere(key)

            const decryptedChunk = vigenere.apply(chunk)

            result = result.concat(decryptedChunk).concat(splitterChar)
        }

        return result
    }

    hillCipher = (task, fileData) => {
        const {splitBy, matrix, isDecryptionMatrix} = task
        const splitterChar = this.liberPrimusSplitter.getSplitterChar(splitBy)
        let result = ''
        const matrixEncryption = new HillCipher(matrix, isDecryptionMatrix)

        for (const chunk of this.liberPrimusSplitter.split(fileData, splitBy)) {

            const decryptedChunk = matrixEncryption.apply(chunk)

            result = result.concat(decryptedChunk).concat(splitterChar)
        }

        return result
    }
}