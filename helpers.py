#!/usr/bin/env python

def toByteList(text):
    """
    Take a string of hexadecimal characters and return a list of bytes, using
    two characters per byte.

    @type   text:   str
    @param  text:   A string contsisting of the characters 0-9, a-f, A-F

    @rtype:         list
    @return:        A list containing positive integers ranging from 0 to 255
    """
    return [int(text[i:i+2], 16) for i in xrange(0, len(text), 2)]

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
    @return:            A string contsisting of hexadecimal characters:14
    """
    return "".join([hex(x)[2:] if x>15 else '0'+hex(x)[2:] for x in byteList])


