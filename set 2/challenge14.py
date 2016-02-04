#!/usr/bin/env python2
from helpers import *
import challenge12 as c12
import random


prefix = generateRandomData(random.randint(2, 32))
print 'Length of random prefix: %d' % len(prefix)
suffix = c12.suffix
key = generateRandomData()


def encrypt(plain):
    s = textToByteList(suffix)
    p = plain + s
    return encryptECB(pkcs7Padding(prefix + p), key)


def detectBlockSize():
    """
    Feed identical bytes of your-string to the function 1 at a time --- start
    with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size
    of the cipher.
    """
    msglen = len(encrypt([]))
    p1 = p2 = ''
    l1 = l2 = msglen
    # first fill up the current block. This also allows us to determine the
    # message size w/o padding, since p1 will eat up the padding bytes until
    # a new block is needed
    while l1 == l2:
        p1 += 'A'
        l2 = len(encrypt(textToByteList(p1)))
    l1 = l2
    # now that the preceding block is full
    while l1 == l2:
        p2 += 'A'
        l2 = len(encrypt(textToByteList(p1 + p2)))
    # in case there is data in front of our data, we need to find out how much
    # padding is needed to align our data to a new block
    paddingsize = len(p1) - 1
    blocksize = len(p2)
    foundDouble = False
    buf = [0x41] * blocksize * 2
    while (not foundDouble) and len(buf) < 4 * blocksize:
        ciphertext = encrypt(buf)
        ctblocks = [c for c in chunks(ciphertext, blocksize)]
        for i in xrange(len(ctblocks) - 1):
            if ctblocks[i] == ctblocks[i + 1]:
                foundDouble = True
                break
        if not foundDouble:
            buf.append(0x41)
    padcount = len(buf) - 2 * blocksize  # num of bytes appended to buffer
    # return (message length of suffix, length of padding, blocksize)
    return (msglen - paddingsize, paddingsize, blocksize, padcount)


def determineBlockOffset(blocksize):
    ciphertext = encrypt([0x41] * 3 * blocksize)
    ciphertexts = [c for c in chunks(ciphertext, blocksize)]
    for off in xrange(len(ciphertexts) - 1):
        if ciphertexts[off] == ciphertexts[off + 1]:
            return off
    return -1


def generateCiphertexts(buffer):
    buffers = {}
    for b in xrange(256):
        buffers[b] = encrypt(buffer + [b])
    return buffers.items()


def guessBytes(maxCount, blocksize, blockOffset, prefixFill):
    buffer = [0x41] * (blocksize - 1 + prefixFill)
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
                    blocksize)][blockCount + blockOffset]  # chunksize, index into cipherblock list

        # compare the block to all possible ciphertexts, recover the plaintext
        for plain, cipher in ciphertexts:  # iterate over all ciphertexts
            # get the block we are interested in, see above
            if [c for c in chunks(cipher, blocksize)][blockCount + blockOffset] == ciphertext:
                recoveredBytes.append(plain)
    return recoveredBytes


def main():
    msglen, padlen, blocksize, prefixCount = detectBlockSize()
    print 'Block size: %d, message length: %d, padlen: %d, prefixCount: %d' % \
          (blocksize, msglen, padlen, prefixCount)

    # check for ECB use
    ciphertext = encrypt([0x41] * 3 * blocksize)
    if not verifyECB(ciphertext, blocksize):
        print 'No ECB usage detected'
        sys.exit(-1)
    blockOffset = determineBlockOffset(blocksize)
    print 'Repeating block at pos. %d' % blockOffset
    # now try to recover the plaintext
    plaintext = guessBytes(msglen, blocksize, blockOffset, prefixCount)
    print 'Length of recovered plaintext: %d\n%s' % (len(plaintext),
                                                     bytesToText(plaintext))


if __name__ == '__main__':
    main()
