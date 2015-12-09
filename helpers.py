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
