#!/usr/bin/env python
from helpers import *

KEY = "ICE"
CLEARTEXT = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"

print toHexString(xor(textToByteList(CLEARTEXT), textToByteList(KEY)))
