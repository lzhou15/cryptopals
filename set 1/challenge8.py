#!/usr/bin/env python2

from helpers import *

ciphertexts = open('../challenges/static/challenge-data/8.txt').readlines()

for c in ciphertexts:
    c = toByteList(c.strip())
    blocks = list(chunks(c, 16))
    detected = []
    for b in blocks:
        if blocks.count(b) > 1:
            detected.append(b)
    if detected:
        outp = toHexString(c)
        for d in detected:
            d = toHexString(d)
            outp = outp.replace(d, '\033[94m' + d + '\033[0m')
        print outp

