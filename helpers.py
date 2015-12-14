#!/usr/bin/env python
from Crypto.Cipher import AES
import random

def toByteList(text):
    """
    Take a string of hexadecimal characters and return a list of bytes, using
    two characters per byte.

    @type   text:   str
    @param  text:   A string contsisting of the characters 0-9, a-f, A-F

    @rtype:         list
    @return:        A list containing positive integers ranging from 0 to 255
    """
    return [ord(c) for c in text.decode('hex')]


def xor(data, key):
    """
    Multi-byte XOR, rotating over the key

    @type   data:   list
    @param  data:   A list of bytes, the cleartext
    @type   key:    list
    @param  key:    A list of bytes, the key

    @rtype:         list
    @return:        A list of bytes, the ciphertext
    """
    result = []
    for i in xrange(len(data)):
        result.append((data[i] & 0xff) ^ (key[i % len(key) & 0xff]))
    return result


def toHexString(byteList):
    """
    Convert a list of bytes to a hexadecimal string.

    @type   byteList:   list
    @param  byteList:   A list of decimal bytes

    @rtype:             str
    @return:            A string consisting of hexadecimal characters
    """
    return "".join([hex(x)[2:] if x > 15 else '0' + hex(x)[2:] for x in byteList])


def textToHexString(text):
    """
    Convert any given string into its hex equivalent. The string AAAA will be
    converted to 41414141. Python actually knows encode('hex'), which will do
    the same.

    @type   text:   str
    @param  text:   the string that should be converted

    @rtype:         str
    @return:        A string consisting of hexadecimal characters
    """
    return text.encode('hex')


def textToByteList(text):
    """
    Convert any given string into its byte list equivalent. The string AAAA
    will be converted to [65, 65, 65, 65].

    @type   text:   str
    @param  text:   the string that should be converted

    @rtype:         list
    @return:        A list containing positive integers ranging from 0 to 255
    """
    return toByteList(textToHexString(text))


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.

    Taken from http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def hexToText(text):
    return str(bytearray(toByteList(text)))


def bytesToText(bytes):
    return hexToText(toHexString(bytes))


def pkcs7Padding(data, blocklen=16):
    """
    Apply PKCS7 padding to data so that len(data) is a multiple of blocklen
    """
    if len(data) % blocklen != 0:
        diff = blocklen - len(data) % blocklen
        data.extend([diff for x in range(diff)])
    return data


def encryptECB(plain, key):
    """
    Encrypt the plaintext block (16 bytes) with key, using AES in ECB mode

    @type  plain: list
    @param plain: The plaintext
    @type  key:   list
    @param key:   The key to use

    @rtype:   list
    @return:  a list with the encrypted bytes (ciphertext)
    """
    aes = AES.new(bytesToText(key))
    # print 'Blocksize of helper object: %d' % aes.block_size
    return textToByteList(aes.encrypt(bytesToText(pkcs7Padding(plain))))


def encryptCBC(plain, key, iv, blocksize):
    """
    Encrypt a plaintext block with key, using AES in CBC mode

    @type  plain: list
    @param plain: The plaintext
    @type  key:   list
    @param key:   The key
    @type  iv:    list
    @param iv:    The IV or previous ciphertext

    @rtype:       list
    @return:      a list with the encrypted bytes (ciphertext)
    """
    ciphertext = []
    for block in chunks(plain, blocksize):
        block = xor(block, iv)
        iv = encryptECB(block, key)
        ciphertext.extend(iv)
    return ciphertext


def decryptECB(cipher, key):
    """
    Decrypt the ciphertext block (16 bytes) with key, using AES in ECB mode

    @type  cipher: list
    @param cipher: The plaintext
    @type  key:    list
    @param key:    The key to use

    @rtype:        list
    @return:       a list with the decrypted bytes (plaintext)
    """
    aes = AES.new(bytesToText(key), AES.MODE_ECB)
    return textToByteList(aes.decrypt(bytesToText(cipher)))


def decryptCBC(cipher, key, iv):
    """
    Decrypt a ciphertext block with key, using AES in CBC mode

    @type  cipher: list
    @param cipher: The plaintext
    @type  key:    list
    @param key:    The key
    @type  iv:     list
    @param iv:     The IV or previous ciphertext

    @rtype:        list
    @return:       a list with the decrypted bytes (plaintext)
    """
    return xor(decryptECB(cipher, key), iv)


def generateRandomData(len=16):
    key = []
    for i in xrange(len):
        key.append(random.randint(0, 255))
    return key


def verifyECB(ciphertext, blocksize):
    ctblocks = [b for b in chunks(ciphertext, blocksize)]
    detected = []
    for b in ctblocks:
        if ctblocks.count(b) > 1:
            detected.append(b)
    if detected:
        return True
    return False
