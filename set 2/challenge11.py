#!/usr/bin/env python2
import random
from helpers import *

functions = [encryptECB, encryptCBC]


def generateRandomData(len=16):
    key = []
    for i in xrange(len):
        key.append(random.randint(0, 255))
    return key


def encryptionOracle(inp, encrypt):
    randomData = generateRandomData(random.randint(5, 10))
    inp = pkcs7Padding(randomData + inp + randomData, 16)
    key = generateRandomData()

    args = [inp, key]
    if encrypt == encryptCBC:
        args.append(generateRandomData())
    ct = encrypt(*args)
    print '(Mode: %s)' % encrypt.func_name
    return ct


def generateKindaRandomPlaintextList():
    sameBlock = 'A' * 32  # this block will be repeated a couple of times
    plaintext = ''
    while len(plaintext) < 400 + random.randint(0, 20):
        choice = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
        if choice in [0]:
            plaintext += sameBlock
        else:
            plaintext += bytesToText(generateRandomData(random.randint(5, 16)))
    while plaintext.count(sameBlock) < 2:
        plaintext += sameBlock
    # print plaintext.replace(sameBlock, '\033[94m' + sameBlock + '\033[0m')
    return textToByteList(plaintext)


def main():
    plaintext = generateKindaRandomPlaintextList()
    plaintext = pkcs7Padding(plaintext, 16)
    ciphertext = encryptionOracle(plaintext, random.choice(functions))

    ctblocks = [b for b in chunks(ciphertext, 16)]
    detected = []
    for b in ctblocks:
        if ctblocks.count(b) > 1:
            detected.append(b)
    if detected:
        print "!!!ECB detected"
        outp = toHexString(ciphertext)
        for d in detected:
            d = toHexString(d)
            outp = outp.replace(d, '\033[31m' + d + '\033[0m')
        print outp

if __name__ == '__main__':
    main()
