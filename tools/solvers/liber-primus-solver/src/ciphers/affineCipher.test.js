import {AffineCipher} from './affineCipher'
import {RunesAlphabet} from '../core/runesAlphabet'

it('translates ᛟᚩᚩᛞᛝᛁ-ᛈᛞᚠᛗᛁᛄ. into AFFINE-CIPHER when a=2 and b=3', () => {
    const runesAlphabet = new RunesAlphabet()
    const affineCipher = new AffineCipher(2, 3)
    const actual = affineCipher.apply('ᛟᚩᚩᛞᛝᛁ-ᛈᛞᚠᛗᛁᛄ.')

    expect(runesAlphabet.translate(actual)).toEqual('AFFINE-[C,K]IPHER.')
})