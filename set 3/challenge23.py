#!/usr/bin/env python2
from helpers import *

def untemper(number):
    number ^= (number >> 18)
    # b = a ^ ((b << 15) & d)

def main():
    unknown_seed = 0xbeefface
    target = MersenneTwister(unknown_seed)
    numbers = []
    for i in range(target.n):
        numbers.append(target.random())
    clone = MersenneTwister(0)
    for i in range(target.n):
        clone.mt[i] = untemper(numbers[i])
    if clone.random() == target.random():
        print "Cloning successful"
    else:
        print "Cloning failed :-("


if __name__ == '__main__':
    main()
