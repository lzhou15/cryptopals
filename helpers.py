#!/usr/bin/env python

def hex2list(text):
    return [int(text[i:i+2], 16) for i in xrange(0, len(text), 2)]

def xor2Bytes(b1, b2):
	return (int(b1) & 0xff) ^ (int(b2) & 0xff)

def xor(data, key):
	result = []
	for i in xrange(len(data)):
		result.append(xor2Bytes(data[i], key[i % len(key)]))
	return result


