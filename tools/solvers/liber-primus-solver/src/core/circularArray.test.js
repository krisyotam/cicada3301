import {CircularArray} from './circularArray'

it('returns the next element', () => {
    const sut = new CircularArray('test'.split(''))

    sut.next()
    sut.next()
    sut.next()
    sut.next()
    sut.next()

    expect(sut.next()).toEqual('e')
})