#!/usr/bin/env python2
from helpers import *
import challenge12 as c12
import random


prefix = generateRandomData(random.randint(2, 32))
suffix = 'Hier steht Text, der mehr oder weniger random ist.'
key = generateRandomData()


def encrypt(plain):
    s = textToByteList(suffix)
    plain.extend(s)
    return encryptECB(prefix + plain, key)


def generateCiphertexts(buffer):
    buffers = {}
    for b in xrange(256):
        buffers[b] = encrypt(buffer + [b])
    return buffers.items()


def guessBytes(maxCount, blocksize):
    buffer = [0x41] * (blocksize - 1)
    blockCount = 0  # counts the number of recovered blocks
    recoveredBytes = []
    for i in xrange(maxCount):
        if len(recoveredBytes) > 0 and len(recoveredBytes) % blocksize == 0:
            # recovered a full block, increase blockCount and the buffer size
            blockCount += 1
            buffer.extend([0x41] * blocksize)

        # ciphertexts is a list of all possible plaintext blocks
        # it consists of the buffer and all so far recovered bytes
        ciphertexts = generateCiphertexts(buffer[len(recoveredBytes):] +
                                          recoveredBytes)
        # encrypt the buffer, get the block we are currently trying to recover
        # use chunks() to split the whole ciphertext into blocks, list compre-
        # hension to get only the block we are interested in so we can guess
        # the last byte of the block
        ciphertext = [c for c in chunks(  # create list of ciphertext blocks
            encrypt(buffer[len(recoveredBytes):]),  # create ciphertext
            blocksize)][blockCount]  # chunksize, index into cipherblock list

        # compare the block to all possible ciphertexts, recover the plaintext
        for plain, cipher in ciphertexts:  # iterate over all ciphertexts
            # get the block we are interested in, see above
            if [c for c in chunks(cipher, blocksize)][blockCount] \
               == ciphertext:
                recoveredBytes.append(plain)
    return recoveredBytes


def main():
    msglen, padlen, blocksize = c12.detectBlockSize()
    print 'Block size: %d, message length: %d' % (blocksize, msglen)

    # check for ECB use
    ciphertext = encrypt([0x41] * 3 * blocksize)
    if not verifyECB(ciphertext, blocksize):
        print 'No ECB usage detected'
        sys.exit(-1)

    # now try to recover the plaintext
    plaintext = guessBytes(msglen, blocksize)
    print 'Length of recovered plaintext: %d\n%s' % (len(plaintext),
                                                     bytesToText(plaintext))


if __name__ == '__main__':
    main()


