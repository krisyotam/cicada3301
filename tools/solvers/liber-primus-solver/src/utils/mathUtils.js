import * as math from 'mathjs'

export const areCoprimes = (a, b) => {
    const absA = math.abs(a)

    if (absA === 0 || b === 0)
        return false
    else if (absA === b)
        return false
    else {
        const gcd = (absA > b) ? math.gcd(absA - b, b) : math.gcd(absA, b - a)

        return gcd === 1
    }
}

export const modInverse = (a, m) => {
    const xgcdResult = math.xgcd(math.abs(a), m).valueOf()

    return xgcdResult[1]
}

export const phi = n => {
    let result = n
    for (let i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            while (n % i == 0)
                n /= i
            result -= result / i
        }
    }
    if (n > 1)
        result -= result / n
    return result
}