#!/usr/bin/env python2
from helpers import *
from pprint import pprint
key = generateRandomData()


def encrypt(plain):
    # filter ; and = and replace them with _
    for i in xrange(len(plain)):
        if plain[i] in [ord(';'), ord('=')]:
            plain[i] = ord('_')

    prefix = textToByteList('comment1=cooking%20MCs;userdata=')
    suffix = textToByteList(';comment2=%20like%20a%20pound%20of%20bacon')
    iv = generateRandomData()
    data = pkcs7Padding(prefix + plain + suffix)
    cipher = encryptCBC(data, key, iv, 16)
    return (iv, cipher)


def decrypt(cipher, iv):
    plain = removePkcs7Padding(decryptCBC(cipher, key, iv))
    return parseString(bytesToText(plain))


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
    return account


def main():
    iv, cipher = encrypt(textToByteList(';admin=true'))

    cipher[22] = cipher[22] ^ ord('_') ^ ord('=')
    cipher[16] = cipher[16] ^ ord('_') ^ ord(';')

    pprint(decrypt(cipher, iv))


if __name__ == '__main__':
    main()
