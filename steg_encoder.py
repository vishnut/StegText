# pylint: disable=C0103

"""
Take an input image
Hide text in the image
Optional password
"""

import sys
import struct
import os
import base64
from PIL import Image
import numpy as np
import bitarray as ba
from Crypto.Cipher import AES

def encrypt_string(inputString, key=None):
    """
    encrypts inputString using optional given key
    based on example from https://pythonprogramming.net/
    uses AES encryption and urandom keys
    """
    BLOCK_SIZE = 16
    PADDING = '{'
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    secret = key or os.urandom(BLOCK_SIZE)
    cipher = AES.new(secret)
    encoded = EncodeAES(cipher, inputString)
    token = base64.b64encode(secret).decode('utf-8')
    print("Token: ", token)
    return encoded

# Input
FILE_NAME = sys.argv[1]
text = sys.argv[2]

# Encrypt text with password if given
if len(sys.argv) <= 3:
    text = encrypt_string(text, base64.b64decode("dCTt6Co9FG5fUtQDmm97mA=="))
else:
    text = encrypt_string(text)

# Read in image
IMG_FILE = Image.open(FILE_NAME)
img_array = np.array(IMG_FILE)

# Text to bitstring
text_bytes = ba.bitarray()
text_bytes.frombytes(text)

# Text length to bitstring
str_len = len(text_bytes)
len_bytes = ba.bitarray()
len_bytes.frombytes(struct.pack(">I", str_len))

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
