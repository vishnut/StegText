# pylint: disable=C0103

"""
Take an input image
Hide text in the image
Optional password
"""

import sys
import struct
from PIL import Image
import numpy as np
import bitarray as ba
import base64
from Crypto.Cipher import AES
from Crypto.Cipher import XOR
import os
import itertools

skey = ''

def encryption(privateInfo):
    BLOCK_SIZE = 16
    PADDING = '{'
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    secret = os.urandom(BLOCK_SIZE)
    global skey
    skey = secret
    print('encryption key:', secret)
    cipher = AES.new(secret)
    encoded = EncodeAES(cipher, privateInfo)
    print('Encrypted string:', encoded)
    token = base64.b64encode(secret).decode('utf-8')
    print("Token: ", token)
    return encoded

# Input
FILE_NAME = sys.argv[1]
text = sys.argv[2]

# XOR text with password if given
if len(sys.argv) > 3:
    #text = base64.b64encode(XOR.new(sys.argv[3]).encrypt(text))
    text = encryption(text)
    print(str(text))
else:
    #text = base64.b64encode(XOR.new(" ").encrypt(text))
    text = encryption(text)
    print(str(text))
    #sys.argv[3]
    #text = obj.encrypt(text)

#print("DECODED", decryption(text))

# Read in image
IMG_FILE = Image.open(FILE_NAME)
img_array = np.array(IMG_FILE)

# Text to bitstring
text_bytes = ba.bitarray()
#text_bytes.fromstring(text)
text_bytes.frombytes(text)

# Text length to bitstring
str_len = len(text_bytes)
print(str_len)
len_bytes = ba.bitarray()
len_bytes.frombytes(struct.pack(">I", str_len))
print(len_bytes)

out_bitstring = list(len_bytes)
out_bitstring.extend(text_bytes)

index = 0
for ix, ival in enumerate(img_array):
    for jx, jval in enumerate(ival):
        for kx, _ in enumerate(jval):
            try:
                if out_bitstring[index]:
                    img_array[ix][jx][kx] |= 1
                else:
                    img_array[ix][jx][kx] &= ~1
                index += 1
            except IndexError:
                break

Image.fromarray(img_array).save('out.bmp')

print("Saved as out.bmp")
