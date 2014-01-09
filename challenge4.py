#!/usr/bin/env python
import sys
from helpers import *

LANG_CODES = [
    'af', 'ar', 'az', 'bg', 'ca', 'ceb', 'cs', 'cy', 'da', 'de', 'en', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'ha', 'haw', 'hi', 'hr', 'hu', 'id', 'is', 'it', 'kk', 'ky', 'la', 'lt', 'lv', 'mk',
    'mn', 'nb', 'ne', 'nl', 'nr', 'nso', 'pl', 'ps', 'pt', 'pt_BR', 'pt_PT', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sr', 'ss', 'st', 'sv', 'sw', 'tl', 'tlh', 'tn', 'tr', 'ts', 'uk', 'ur', 'uz', 've', 'xh', 'zu']


def readTrigrams(language):
    trigrams = []
    for line in open("./trigrams/" + language).readlines():
        trigrams.append(line[:3])
    return trigrams


def evaluateAndPrintResults(cleartextList, language):
    trigrams = readTrigrams(language)
    for text in cleartextList:
        count = 0
        for t in trigrams:
            count += text.lower().count(t)
        if count > 4:
            print text


def printUsage():
    print "Usage: %s [language code]" % sys.argv[0]
    print """Available languages:
    af ar az bg ca ceb cs cy
    da de en es et eu fa fi
    fr ha haw hi hr hu id is
    it kk ky la lt lv mk mn
    nb ne nl nr nso pl ps pt
    pt_BR pt_PT ro ru sk sl so sq
    sr ss st sv sw tl tlh tn
    tr ts uk ur uz ve xh zu"""


def main():
    if len(sys.argv) != 2:
        printUsage()
        sys.exit(1)
    if not sys.argv[1] in LANG_CODES:
        print "Language code not found"
        printUsage()
        sys.exit(2)

    ciphertexts = [x.strip() for x in open("./challenge4.txt").readlines()]
    cleartextList = []
    for k in range(127):
        for cipher in ciphertexts:
            cleartextList.append(
                str(bytearray(xor(toByteList(cipher), [k]))))

    evaluateAndPrintResults(cleartextList, sys.argv[1])


if __name__ == '__main__':
    main()
