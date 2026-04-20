import {RunesAlphabet} from './runesAlphabet'

import 'regenerator-runtime/runtime'

it('recognises that ᚣ is a rune', () => {
    const input = 'ᚣ'

    const runesTranslator = new RunesAlphabet()

    expect(runesTranslator.isRune(input)).toEqual(true)
})

it('recognises that 6 is not  a rune', () => {
    const input = '6'

    const runesTranslator = new RunesAlphabet()

    expect(runesTranslator.isRune(input)).toEqual(false)
})