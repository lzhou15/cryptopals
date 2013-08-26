#!/usr/bin/env python
from helpers import *

ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

cleartextList = []
for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
	cleartextList.append(str(bytearray(xor(hex2list(ciphertext), [ord(k)]))))