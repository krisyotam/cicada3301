import {Atbash} from './atbash'
import {RunesAlphabet} from '../core/runesAlphabet'

it('translates ᚱ-ᛝᚱᚪᛗᚹ. into A-WARN[NG,ING].', () => {
    const runesTranslator = new RunesAlphabet()
    const atBash = new Atbash()

    const input = 'ᚱ-ᛝᚱᚪᛗᚹ.'
    const atBashResult = atBash.apply(input)
    const actual = runesTranslator.translate(atBashResult)

    expect(actual).toEqual('A-WARN[NG,ING].')
})