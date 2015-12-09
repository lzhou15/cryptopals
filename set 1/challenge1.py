#!/usr/bin/env python2
import base64
from helpers import *

thestring = ("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706"
             "f69736f6e6f7573206d757368726f6f6d")


def builtin():
    print thestring.decode("hex")
    print base64.b64encode(thestring.decode("hex"))


def myBase64(text):
    b64index = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456"
                "789+/")
    b64result = ""
    for t in [text[i:i + 3] for i in xrange(0, len(text), 3)]:
        while len(t) < 3:
            t += "\x00"
        n = ((ord(t[0])) << 16) + ((ord(t[1])) << 8) + (ord(t[2]))
        b64result += b64index[(n >> 18) & 0x3f]
        b64result += b64index[(n >> 12) & 0x3f]
        b64result += b64index[(n >> 6) & 0x3f]
        b64result += b64index[n & 0x3f]
    if len(text) % 3 > 0:
        append = 3 - (len(text) % 3)
        b64result = b64result[:-append]
        for i in xrange(append):
            b64result += "="
    return b64result


def manually():
    print hexToText(thestring)
    print myBase64(hexToText(thestring))

builtin()
manually()
