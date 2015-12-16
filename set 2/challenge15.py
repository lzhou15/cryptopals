#!/usr/bin/env python2
from helpers import *

valid = textToByteList("ICE ICE BABY\x04\x04\x04\x04")
invalid1 = textToByteList("ICE ICE BABY\x05\x05\x05\x05")
invalid2 = textToByteList("ICE ICE BABY\x01\x02\x03\x04")


def main():
    print bytesToText(removePkcs7Padding(valid))
    try:
        print bytesToText(removePkcs7Padding(invalid1))
    except ValueError, ve:
        print 'Error: ' + ve.message
    try:
        print bytesToText(removePkcs7Padding(invalid2))
    except ValueError, ve:
        print 'Error: ' + ve.message


if __name__ == '__main__':
    main()
