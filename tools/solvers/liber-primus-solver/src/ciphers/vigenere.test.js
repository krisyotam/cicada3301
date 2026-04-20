import {Vigenere} from './vigenere'
import {RunesAlphabet} from '../core/runesAlphabet'

it('translates ᚢᛠᛝᛋᛇᚠᚳ.ᚱᛇᚢᚷᛈᛠᛠ-ᚠᚹᛉ/ into WEL[C,K]OME.WEL[C,K]OME-PIL/ using key ᛞᛁᚢᛁᚾᛁᛏᚣ', () => {
    const input = 'ᚢᛠᛝᛋᛇᚠᚳ.ᚱᛇᚢᚷᛈᛠᛠ-ᚠᚹᛉ/'
    const runesTranslator = new RunesAlphabet()
    const vigenere = new Vigenere('ᛞᛁᚢᛁᚾᛁᛏᚣ')

    const result = vigenere.apply(input)

    expect(runesTranslator.translate(result)).toEqual('WEL[C,K]OME.WEL[C,K]OME-PIL/')

})