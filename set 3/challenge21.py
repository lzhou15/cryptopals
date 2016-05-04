#!/usr/bin/env python2
from helpers import *


def main():
    m = MersenneTwister(12345678)
    for i in range(10):
        print m.random(),
        if i % 5 == 4:
            print


if __name__ == '__main__':
    main()
