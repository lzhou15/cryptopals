#!/usr/bin/env python2
from helpers import *
from base64 import b64decode

ciphertext = b64decode(('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/'
                        '2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='))


if __name__ == '__main__':
    ctr = AESCTR(textToByteList('YELLOW SUBMARINE'), 0)
    print bytesToText(ctr.decrypt(textToByteList(ciphertext)))
