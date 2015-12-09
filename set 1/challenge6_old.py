#!/usr/bin/env python
import base64
import pprint
from helpers import *
from challenge3_freq_an import FREQUENCY_TABLE
from collections import defaultdict


def evaluateResults(cleartextList, variance=5):
    count = 0
    maxcount = 0
    result = ""
    for key, ct in cleartextList:
        count = 0
        for l in set(ct.lower()):
            f = ct.count(l) * 100. / len(ct)
            try:
                if f > FREQUENCY_TABLE[l] - variance and \
                        f < FREQUENCY_TABLE[l] + variance:
                    count += 1
            except KeyError:
                pass
        if count > maxcount:
            maxcount = count
            result = key
            print "Length: %d, Hits: %d" % (len(ct), count)
    return result


def read_file(filename):
    try:
        h = open(filename, "r")
    except IOError:
        return None

    return base64.b64decode(h.read())


def compute_hamming_distance(s1, s2):
    bin_s1 = bin_s2 = 0
    # convert each string to binary
    for c in s1:
        bin_s1 = bin_s1 << 8
        bin_s1 += ord(c)

    for c in s2:
        bin_s2 = bin_s2 << 8
        bin_s2 += ord(c)

    # if you XOR the binary numbers and then count the 1s, you get the Hamming
    # distance
    return bin(bin_s1 ^ bin_s2).count("1")


def compute_hamming_distance2(s1, s2, s3, s4, keysize):
    bin_s1 = bin_s2 = bin_s3 = bin_s4 = 0
    # convert each string to binary
    for c in s1:
        bin_s1 = bin_s1 << 8
        bin_s1 += ord(c)

    for c in s2:
        bin_s2 = bin_s2 << 8
        bin_s2 += ord(c)

    for c in s3:
        bin_s3 = bin_s3 << 8
        bin_s3 += ord(c)

    for c in s4:
        bin_s4 = bin_s4 << 8
        bin_s4 += ord(c)

    # if you XOR the binary numbers and then count the 1s, you get the Hamming
    # distance
    return (bin(bin_s1 ^ bin_s2).count("1") / float(keysize) +
            bin(bin_s1 ^ bin_s3).count("1") / float(keysize) +
            bin(bin_s1 ^ bin_s4).count("1") / float(keysize)) / 3


def find_smallest_distance(distances):
    keylen = dist = 10000
    for k in distances.keys():
        if distances[k] < dist:
            keylen = k
            dist = distances[k]
    return keylen, dist


def transpose_blocks(cipherblocks, blocklen):
    transposed_blocks = []
    s = ""
    for b in range(blocklen):
        for block in cipherblocks:
            try:
                s += block[b]
            except:
                pass
        transposed_blocks.append(s)
        s = ""
    return transposed_blocks


def main():
    ciphertext = read_file("challenge6.ciphertext")
    distances = {}
    for keysize in range(1, 41):
        s1 = ciphertext[:keysize]
        s2 = ciphertext[keysize:2 * keysize]
        s3 = ciphertext[2 * keysize:3 * keysize]
        s4 = ciphertext[3 * keysize:4 * keysize]
    # distances[keysize] = compute_hamming_distance(s1, s2) / float(keysize)
        distances[keysize] = compute_hamming_distance2(s1, s2, s3, s4, keysize)
    keylen, distance = find_smallest_distance(distances)
    print "Keylen: %d" % keylen
    ciphertext_blocks = [s for s in chunks(ciphertext, keylen)]
    print "No. of blocks: %d" % len(ciphertext_blocks)
    transposed_blocks = transpose_blocks(ciphertext_blocks, keylen)
    print "No of transposed blocks: %d" % len(transposed_blocks)
    for b in transposed_blocks:
        print "\tblock len: %d" % len(b)
    # at this point we have keylen transposed blocks
    # every block has supposedly been xor'ed with the same value
    supposed_key = ""
    print "Input Length: %d" % len(ciphertext)
    for block in transposed_blocks:
        cleartextList = []
        for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            cleartextList.append((k,
                str(
                    bytearray(
                        xor(textToByteList(block), textToByteList(k))
                    )
                ))
            )
            print "original length: %d, xored length: %d" % (len(b), len(cleartextList[-1][1]))
        supposed_key += evaluateResults(cleartextList, 6)
    print supposed_key
    # print str(bytearray(xor(toByteList(textToHexString(ciphertext)), toByteList(textToHexString(supposed_key)))))

if __name__ == '__main__':
    main()
