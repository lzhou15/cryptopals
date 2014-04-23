#!/usr/bin/env python2

import requests
import base64
import helpers

ciphertextURL = "https://gist.github.com/tqbf/3132928/raw"

print "Fetching ciphertexts"
r = requests.get(ciphertextURL)
cipherlist = [base64.b64decode(x) for x in r.text.split()]

print "Checking for ECB"
for c in cipherlist:
    blocks = list(helpers.chunks(c, 16))
    detected = []
    for b in blocks:
        if blocks.count(b) > 1:
            detected.append(b)
    if detected:
        print "!!!ECB detected"
        outp = c
        for d in detected:
            outp = outp.replace(d, '\033[94m' + d + '\033[0m')
        print outp
