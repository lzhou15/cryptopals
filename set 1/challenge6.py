import base64
from helpers import *


FREQUENCY_TABLE = {
    "e": 12.02, "t": 9.10, "a": 8.12, "o": 7.68, "i": 7.31, "n": 6.95,
    "s": 6.28, "r": 6.02, "h": 5.92, "d": 4.32, "l": 3.98, "u": 2.88,
    "c": 2.71, "m": 2.61, "f": 2.30, "y": 2.11, "w": 2.09, "g": 2.03,
    "p": 1.82, "b": 1.49, "v": 1.11, "k": 0.69, "x": 0.17, "q": 0.11,
    "j": 0.10, "z": 0.07}


def evaluateAndPrintResults(cleartextList):
    variance = 3.5
    maxcount = 0
    for text, key in cleartextList:
        count = 0
        for l in set(text.lower()):
            f = text.lower().count(l) * 100. / len(text)
            try:
                if f >= FREQUENCY_TABLE[l] - variance and \
                   f <= FREQUENCY_TABLE[l] + variance:
                    count += 1
            except KeyError:
                pass
            if count >= maxcount:
                maxcount = count
                retKey = key
    return retKey


def read_file(filename):
    try:
        h = open(filename, "r")
    except IOError:
        return None

    return base64.b64decode(h.read())


def compute_hamming_distance(s1, s2):
    # convert each string to binary
    bin_s1 = int(s1.encode('hex'), 16)
    bin_s2 = int(s2.encode('hex'), 16)
    # if you XOR the binary numbers and then count the 1s, you get the Hamming
    # distance
    return bin(bin_s1 ^ bin_s2).count("1")


def find_distance(ciphertext, keysize):
    distances = []
    s1 = ciphertext[:keysize]
    for i in range(1, 5):
        s2 = ciphertext[(i + 1) * keysize:(i + 2) * keysize]
        distances.append(compute_hamming_distance(s1, s2))
    return float(sum(distances))/keysize


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
    # read ciphertext
    ciphertext = read_file("challenge6.ciphertext")
    distances = {}

    # calculate hamming distance for each assumed keylength
    for keysize in xrange(3, 41):
        distances[keysize] = find_distance(ciphertext, keysize)

    # select the keylength with the lowest hamming distance
    keysize = min(distances, key=distances.get)
    print 'Assuming keysize %d' % keysize
    # split ciphertext into chunks
    ciphertext_blocks = [s for s in chunks(ciphertext, keysize)]

    # transpose all chunks
    transposed_blocks = transpose_blocks(ciphertext_blocks, keysize)

    key = ''
    # solve single-byte xor for each chunk
    for block in transposed_blocks:
        cleartextList = []
        for k in range(127):
            cleartextList.append(
                (str(bytearray(xor(textToByteList(block), [k]))), k)
            )
        key += chr(evaluateAndPrintResults(cleartextList))
    print key

if __name__ == '__main__':
    main()
