#!/usr/bin/env python2
from helpers import *
from base64 import b64decode
import sys

appendix = b64decode(
    ('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg'
     'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq'
     'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg'
     'YnkK'))
key = generateRandomData(32)


def encrypt(plain):
    a = textToByteList(appendix)
    plain.extend(a)
    return encryptECB(plain, key)


def detectBlockSize():
    """
    Feed identical bytes of your-string to the function 1 at a time --- start
    with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size
    of the cipher.
    """
    msglen = len(encrypt([]))
    p1 = p2 = ''
    l1 = l2 = len(encrypt([]))
    # first fill up the current block. This also allows us to determine the
    # message size w/o padding, since p1 will eat up the padding bytes until
    # a new block is needed
    while l1 == l2:
        p1 += 'A'
        l2 = len(encrypt(textToByteList(p1 + p2)))
    l1 = l2
    # now that the preceding block is full
    while l1 == l2:
        p2 += 'A'
        l2 = len(encrypt(textToByteList(p1 + p2)))
    # return (message length of appendix, blocksize)
    return (msglen - len(p1) + 1, len(p2))


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
        ciphertext = [c for c in chunks(encrypt(buffer[len(recoveredBytes):]),
                                        blocksize)][blockCount]
        for plain, cipher in ciphertexts:
            if [c for c in chunks(cipher, blocksize)][blockCount] \
               == ciphertext:
                recoveredBytes.append(plain)
    return recoveredBytes


def main():
    msglen, blocksize = detectBlockSize()
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
