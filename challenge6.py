#!/usr/bin/env python
import base64
import pprint
from helpers import *
from challenge3 import *
from collections import defaultdict

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


def find_smallest_distance(distances):
    key = val = 10000
    for k in distances.keys():
        if distances[k] < val:
            key = k
            val = distances[k]
    return key, val


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


def do_letter_count(block):
    counts = defaultdict(int)
    for letter in block:
        counts[letter] += 1
    result = sorted(counts, key = counts.get)
    result.reverse()
    # now result[0:3] contains the three most frequent letters
    # it is assumed that one of them corresponds to the letter E
    # print result[0:3]
    return [chr(ord(x) ^ ord('T')) for x in result[0:3]]

def print_permutations(possible_key_values):
    pass

def main():
    ciphertext = read_file("challenge6.ciphertext")
    distances = {}
    for KEYSIZE in range(2, 41):
        s1 = ciphertext[:KEYSIZE]
        s2 = ciphertext[KEYSIZE:2 * KEYSIZE]
        distances[KEYSIZE] = compute_hamming_distance(s1, s2) / float(KEYSIZE)
    keylen, distance = find_smallest_distance(distances)
    ciphertext_blocks = [s for s in chunks(ciphertext, keylen)]
    transposed_blocks = transpose_blocks(ciphertext_blocks, keylen)
    # at this point we have keylen transposed blocks
    # every block has supposedly been xor'ed with the same value
    # do a simple letter count, find the three most used letters
    possible_key_values = []
    for block in transposed_blocks:
        possible_key_values.append(do_letter_count(block))
    pprint.pprint(possible_key_values)

if __name__ == '__main__':
    main()
