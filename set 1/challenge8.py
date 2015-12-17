#!/usr/bin/env python2

import helpers

ciphertexts = open('../challenges/static/challenge-data/8.txt').readlines()

print "Checking for ECB"
for c in ciphertexts:
    c = helpers.toByteList(c.strip())
    blocks = list(helpers.chunks(c, 16))
    detected = []
    for b in blocks:
        if blocks.count(b) > 1:
            detected.append(b)
    if detected:
        print "!!!ECB detected"
        outp = helpers.toHexString(c)
        for d in detected:
            d = helpers.toHexString(d)
            outp = outp.replace(d, '\033[94m' + d + '\033[0m')
        print outp
