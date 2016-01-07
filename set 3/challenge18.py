#!/usr/bin/env python2
from helpers import *
from base64 import b64decode

ciphertext = b64decode(('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/'
                        '2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='))


if __name__ == '__main__':
    print bytesToText(
                decryptCTR(
                            textToByteList(ciphertext),
                            textToByteList('YELLOW SUBMARINE'),
                            0
                          )
                )
