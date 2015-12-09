#!/usr/bin/env python2
import sys
from helpers import *

CIPHERTEXT = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
# CIPHERTEXT = "4554414f494e20534852444c55"
LANG_CODES = [
    'af', 'ar', 'az', 'bg', 'ca', 'ceb', 'cs', 'cy', 'da', 'de', 'en', 'es',
    'et', 'eu', 'fa', 'fi', 'fr', 'ha', 'haw', 'hi', 'hr', 'hu', 'id', 'is',
    'it', 'kk', 'ky', 'la', 'lt', 'lv', 'mk', 'mn', 'nb', 'ne', 'nl', 'nr',
    'nso', 'pl', 'ps', 'pt', 'pt_BR', 'pt_PT', 'ro', 'ru', 'sk', 'sl', 'so',
    'sq', 'sr', 'ss', 'st', 'sv', 'sw', 'tl', 'tlh', 'tn', 'tr', 'ts', 'uk',
    'ur', 'uz', 've', 'xh', 'zu']


def readTrigrams(language):
    trigrams = []
    for line in open("./trigrams/" + language).readlines():
        trigrams.append(line[:3])
    return trigrams


def evaluateResults(cleartextList, language):
    trigrams = readTrigrams(language)
    result = ""
    count = 0
    for text in cleartextList:
        currentCount = 0
        for t in trigrams:
            currentCount += text.lower().count(t)
        if currentCount > count:
            count = currentCount
            result = text
    return (result, count)


def printUsage():
    print "Usage: %s [language code]" % sys.argv[0]
    print """Available languages:
    af ar az
    bg
    ca ceb cs cy
    da de
    en es et eu
    fa fi fr
    ha haw hi hr hu
    id is it
    kk ky
    la lt lv
    mk mn
    nb ne nl nr nso
    pl ps pt pt_BR pt_PT
    ro ru
    sk sl so sq sr ss st sv sw
    tl tlh tn tr ts
    uk ur uz
    ve
    xh
    zu"""


def main():
    if len(sys.argv) != 2:
        printUsage()
        sys.exit(1)
    if not sys.argv[1] in LANG_CODES:
        print "Language code not found"
        printUsage()
        sys.exit(2)

    cleartextList = []
    # xor the ciphertext with every possible key to get a list of all possible
    # ciphertexts
    for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        cleartextList.append(
            str(bytearray(xor(toByteList(CIPHERTEXT), [ord(k)])))
        )
    # run the evaluation routine against all ciphertexts and find the text
    # that is most likely the plaintext
    print "%s (%d hits)" % evaluateResults(cleartextList, sys.argv[1])


if __name__ == '__main__':
    main()
