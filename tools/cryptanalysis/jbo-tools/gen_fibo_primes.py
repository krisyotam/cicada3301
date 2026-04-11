#!/usr/bin/env python3
import sympy

expected = [ 2, 3, 5, 7, 13, 23, 43, 79, 149, 263, 463, 829, 1481, 2593, 4507, 7817 ]

x = []
curr_prime = 2
fib_a, fib_b = 1, 1
try:
    while True:
        x.append(curr_prime)
        print(f'\rCurrent size: {len(x)}, press CTRL+C to finish...', end='')
        for _ in range(max(1, fib_b - fib_a)):
            curr_prime = sympy.nextprime(curr_prime)
        fib_a, fib_b = fib_b, fib_a + fib_b

except KeyboardInterrupt:
    assert x[:len(expected)] == expected, Exception('Mismatch')
    print('')
    for i in x:
        print(i)

