#!/usr/bin/env python
from helpers import *

s1 = "1c0111001f010100061a024b53535009181c"
s2 = "686974207468652062756c6c277320657965"

print toHexString(xor(toByteList(s1), toByteList(s2)))