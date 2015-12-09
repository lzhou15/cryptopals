#!/usr/bin/env python
import sys
from helpers import *

CIPHERTEXT = ("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a39"
              "3b3736")
FREQUENCY_TABLE = {  # english language frequency table
    "e": 12.02, "t": 9.10, "a": 8.12, "o": 7.68, "i": 7.31, "n": 6.95,
    "s": 6.28, "r": 6.02, "h": 5.92, "d": 4.32, "l": 3.98, "u": 2.88,
    "c": 2.71, "m": 2.61, "f": 2.30, "y": 2.11, "w": 2.09, "g": 2.03,
    "p": 1.82, "b": 1.49, "v": 1.11, "k": 0.69, "x": 0.17, "q": 0.11,
    "j": 0.10, "z": 0.07}


def evaluateResults(cleartextList, variance):
    count = 0
    maxcount = 0
    result = ""
    for ct in cleartextList:
        count = 0
        for l in set(ct.lower()):  # get all letters in a single ct
            f = ct.count(l) * 100. / len(ct)  # get character freqency
            try:
                # if l.upper() in 'ETAOINSHRDLU':
                if f >= FREQUENCY_TABLE[l] - variance and \
                   f <= FREQUENCY_TABLE[l] + variance:
                    # everytime a letter freq is between f(l) +- var, incr.
                    # count
                    count += 1
            except KeyError:
                pass
        if count > maxcount:
            maxcount = count
            result = ct
    print maxcount
    return result


def main():
    if len(sys.argv) == 2:
        variance = int(sys.argv[1])
    else:
        variance = 10
    cleartextList = []
    # create all possible ciphertexts
    for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        cleartextList.append(
            str(bytearray(xor(toByteList(CIPHERTEXT), [ord(k)]))))
    print evaluateResults(cleartextList, variance)


if __name__ == '__main__':
    main()
