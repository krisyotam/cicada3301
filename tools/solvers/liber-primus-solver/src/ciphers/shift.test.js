import {Shift} from './shift'

it('when asked to shift (ᚻ,4) returns ᛇ', () => {
    const shiftOperator = new Shift()

    expect(shiftOperator.apply('ᚻ', 4)).toEqual('ᛇ')
})

it('when asked to shift (ᛠ,2) returns ᚢ', () => {
    const shiftOperator = new Shift()

    expect(shiftOperator.apply('ᛠ', 2)).toEqual('ᚢ')
})

it('when asked to shift (ᛠ,-2) returns ᚣ', () => {
    const shiftOperator = new Shift()

    expect(shiftOperator.apply('ᛠ', -2)).toEqual('ᚣ')
})

it('when asked to shift (ᚠ,-2) returns ᛡ', () => {
    const shiftOperator = new Shift()

    expect(shiftOperator.apply('ᚠ', -2)).toEqual('ᛡ')
})

it('when asked to shift (ᚠ,-29) returns ᚠ', () => {
    const shiftOperator = new Shift()

    expect(shiftOperator.apply('ᚠ', -29)).toEqual('ᚠ')
})

it('when asked to shift (ᚾ,-31) returns ᚹ', () => {
    const shiftOperator = new Shift()

    expect(shiftOperator.apply('ᚾ', -31)).toEqual('ᚹ')
})