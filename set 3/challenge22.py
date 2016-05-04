#!/usr/bin/env python2
from helpers import *
import time
import random


def get_random(timestamp):
    m = MersenneTwister(timestamp)
    return m.random()


def recover_seed(random_number, timestamp):
    for i in xrange(2100):
        m = MersenneTwister(timestamp - i)
        if m.random() == random_number:
            return timestamp - i
    return False


def main():
    timestamp = int(time.time()) + random.randint(40, 1000)
    print " Original seed", timestamp
    random_number = get_random(timestamp)
    timestamp += random.randint(40, 1000)
    seed = recover_seed(random_number, timestamp)
    if seed is not False:
        print "Recovered seed", seed

if __name__ == '__main__':
    main()