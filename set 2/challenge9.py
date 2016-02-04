#!/usr/bin/env python2

import sys
from helpers import pkcs7Padding, textToByteList


def main():
    if len(sys.argv) != 3:
        print 'missing input'
        print 'Usage: %s <input> <blocklen>' % (sys.argv[0])
        sys.exit(1)
    try:
        blocklen = int(sys.argv[2])
    except ValueError:
        print 'length is not a number'
        print 'Usage: %s <input> <blocklen>' % (sys.argv[0])
        sys.exit(2)
    unpadded_text = sys.argv[1]

    print pkcs7Padding(textToByteList(unpadded_text), blocklen)


if __name__ == '__main__':
    main()
