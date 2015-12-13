#!/usr/bin/env python2

from helpers import *
from base64 import b64decode


def main():
    key = textToByteList('YELLOW SUBMARINE')
    path = '../challenges/static/challenge-data/10.txt'
    lines = open(path).readlines()
    ct = []
    for l in lines:
        ct.extend(textToByteList(b64decode(l)))
    prev = [ord(i) for i in '\x00' * 16]  # IV for CBC
    pt = []
    for block in chunks(ct, 16):
        pt.extend(decryptCBC(block, key, prev))
        prev = block
    print bytearray(pt)

if __name__ == '__main__':
    main()
