import 'regenerator-runtime/runtime'
import {RunesAsPrimes} from './runesAsPrimes'

it('words from first matrix: ᚪᚾᚪᛚᚩᚷ and ᚳᚪᚱᚾᚪᛚ prime values sum is 320', () => {

    const sut = new RunesAsPrimes()

    expect(sut.wordAsSumOfPrimes('ᚪᚾᚪᛚᚩᚷ')).toEqual(320)
    expect(sut.wordAsSumOfPrimes('ᚳᚪᚱᚾᚪᛚ')).toEqual(320)
})

it('words from first matrix: ᛒᚢᚠᚠᛖᚱᛋ and ᛗᚩᚢᚱᚾᚠᚢᛚ prime values sum is 320', () => {

    const sut = new RunesAsPrimes()

    expect(sut.wordAsSumOfPrimes('ᛒᚢᚠᚠᛖᚱᛋ')).toEqual(199)
    expect(sut.wordAsSumOfPrimes('ᛗᚩᚢᚱᚾᚠᚢᛚ')).toEqual(199)
})