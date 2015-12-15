#!/usr/bin/env python2
from pprint import pprint
from helpers import *

accounts = {}
teststrings = ['email=foo@bar.baz&uid=10&role=user',
               'email=baz@qux.com&uid=11&role=user',
               'email=admin@admin.com&uid=1&role=admin']


def parseString(string):
    account = {}
    kvpairs = string.split('&')
    for kv in kvpairs:
        k, v = kv.split('=', 1)
        account[k] = v
    return account


def profile_for(name):
    # remove special characters
    name = name.replace('=', '_')
    name = name.replace('&', '_')
    return 'email=' + name + '&uid=10&role=user'


def main():
    key = generateRandomData()
    # 10x A to fill the first block, then admin padding for the next block
    plaintext = profile_for('A' * 10 + 'admin' + '\x0b' * 0xb)
    ciphertext = encryptECB(textToByteList(plaintext), key)
    adminBlock = ciphertext[16:32]  # this is the block that contains admin
    plaintext = profile_for('admin1@me.com')
    print 'pre-encrypted data: ' + str(parseString(plaintext))
    ciphertext = encryptECB(textToByteList(plaintext), key)
    ciphertext = ciphertext[:-16] + adminBlock
    plaintext = decryptECB(ciphertext, key)
    print 'manipulated: ' + \
          str(parseString(bytesToText(removePkcs7Padding(plaintext))))


if __name__ == '__main__':
    main()
