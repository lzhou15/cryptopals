#!/usr/bin/env python2

import sys


def do_padding(text, length):
    diff = length - len(text)
    return text + chr(diff) * diff


def main():
    if len(sys.argv) != 3:
        print 'missing input'
        print 'Usage: %s <input> <length>' % (sys.argv[0])
        sys.exit(1)
    try:
        padded_length = int(sys.argv[2])
    except ValueError:
        print 'length is not a number'
        print 'Usage: %s <input> <length>' % (sys.argv[0])
        sys.exit(2)
    unpadded_text = sys.argv[1]

    if len(unpadded_text) >= padded_length:
        print 'input is not smaller than length'
        print 'Usage: %s <input> <length>' %(sys.argv[0])
        sys.exit(3)

    print do_padding(unpadded_text, padded_length)


if __name__ == '__main__':
    main()
