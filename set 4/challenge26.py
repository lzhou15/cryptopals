#!/usr/bin/env python2
from helpers import *
import random

key = generateRandomData()
nonce = random.randint(0, (2**16) - 1)
ctr = AESCTR(key, nonce)


def encrypt(plain):
    global ctr
    ctr.reset()
    # filter ; and = and replace them with _
    for i in xrange(len(plain)):
        if plain[i] in [ord(';'), ord('=')]:
            plain[i] = ord('_')

    prefix = textToByteList('comment1=cooking%20MCs;userdata=')
    suffix = textToByteList(';comment2=%20like%20a%20pound%20of%20bacon')
    data = prefix + plain + suffix
    cipher = ctr.encrypt(data)
    return cipher


def parseString(string):
    account = {}
    kvpairs = string.split(';')
    for kv in kvpairs:
        try:
            k, v = kv.split('=', 1)
        except:
            k = kv
            v = ''
        account[k] = v
    if 'admin' in account.keys() and account['admin'].lower() == 'true':
        print 'You are an admin'
    else:
        print 'You are not an admin'


def main():
    cipher = encrypt(textToByteList(';admin=true'))

    cipher[32] = cipher[32] ^ ord('_') ^ ord(';')
    cipher[38] = cipher[38] ^ ord('_') ^ ord('=')
    ctr.reset()
    parseString(bytesToText(ctr.decrypt(cipher)))


if __name__ == '__main__':
    main()
