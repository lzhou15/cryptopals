#!/usr/bin/env python2
from helpers import *
from base64 import b64decode


class AESCTR_25(AESCTR):

    def edit(self, ciphertext, offset, newtext):
        self.reset()
        if offset + len(newtext) > len(ciphertext):
            raise IndexError('offset too high')
        for i in range(offset):
            self.nextKeyByte()  # pop offset keybytes off the keystream
        ct = list(ciphertext)  # I do not want to modify the original ciphertext
        for n in newtext:
            ct[offset] = self.encrypt([n])[0]  # encrypt returns a list
            offset += 1
        return ct


def main():
    # first get the plaintext that I am going to recover
    plaintext = open('../challenges/static/challenge-data/25.txt').read()
    plaintext = b64decode(plaintext)
    plaintext = decryptECB(textToByteList(plaintext), textToByteList('YELLOW SUBMARINE'))

    # encrypt the plaintext using a random key
    random_key = generateRandomData(16)
    ctr = AESCTR_25(random_key, random.randint(0, 2**16 - 1))
    ciphertext = ctr.encrypt(plaintext)

    # use the edit API to encrypt a plaintext that I know with the same key
    my_plaintext = textToByteList('A' * len(ciphertext))
    my_ciphertext = ctr.edit(ciphertext, 0, my_plaintext)
    ctr.reset()

    # by xor'ing the original ciphertext and the new cipertext, I get the target plaintext xor'ed with my known
    # plaintext: (target ^ key) ^ (known ^ key) == target ^ key ^ known ^ key == target ^ known
    intermediate_text = xor(ciphertext, my_ciphertext)

    # to recover the plaintext, xor with my plaintext to recover the target plaintext
    target_plaintext = xor(intermediate_text, my_plaintext)
    print bytesToText(target_plaintext)


if __name__ == '__main__':
    main()
