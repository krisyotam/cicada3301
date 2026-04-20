import {HillCipher} from './hillCipher'
import {RunesAlphabet} from '../core/runesAlphabet'

it('decrypts using encryption matrix: [[3,3],[2,5]]', () => {
    const runesAlphabet = new RunesAlphabet()
    const matrix = [[3, 3], [2, 5]]
    const hillCipher = new HillCipher(matrix, false)
    const inputText = 'ᛚᛗᚱᚪᛗ-ᛈᚩᚱᚢᚩᚠᛠ.'
    const expected = 'HELLO-PILGRIM.'

    const result = hillCipher.apply(inputText)

    expect(runesAlphabet.translate(result)).toEqual(expected)
})