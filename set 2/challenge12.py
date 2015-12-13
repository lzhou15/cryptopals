#!/usr/bin/env python2
from helpers import *
from base64 import b64decode

appendix = b64decode(
    ('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg'
     'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq'
     'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg'
     'YnkK'))
key = generateRandomData()


def detectBlockSize():
    plaintext = [0x41] * 64
    ciphertext = encryptECB(plaintext, key)
    


def main():
    blocksize = detectBlockSize()
    pass


if __name__ == '__main__':
    main()
