import {phi} from './mathUtils'

test.each`
n       | value
${1}    |${1}
${108}  |${36}
${69}   |${44}
`('phi($n) equals $value', ({n, value}) => expect(phi(n)).toEqual(value))