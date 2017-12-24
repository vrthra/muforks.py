#!/usr/bin/env python3
import sys
import mu
def triangle(a, b, c):
    if a == b:
        if b == c:
            return 'Equilateral'
        else:
            return 'Isosceles'
    else:
        if b == c:
            return "Isosceles"
        else:
            if a == c:
                return "Isosceles"
            else:
                return "Scalene"
def main():
    v = triangle(1, 1, 1)
    assert(v == 'Equilateral')
    v = triangle(1, 2, 1)
    assert(v == 'Isosceles')
    v = triangle(1, 2, 3)
    assert(v == 'Scalene')


main()
