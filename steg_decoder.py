# pylint: disable=C0103

"""
Take an input image
Find text in the image
Optional password
"""

import sys
import struct
import itertools
from PIL import Image
import numpy as np
import bitarray as ba
import base64
from Crypto.Cipher import XOR
from Crypto.Cipher import AES
import os

def decrypt(encryptedString, key):
    PADDING = bytes('{', 'utf-8')
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    encrypti = encryptedString
    skey = base64.b64decode(key)
    cipher = AES.new(skey)
    decoded = DecodeAES(cipher, encrypti)
    return decoded

# Input
FILE_NAME = sys.argv[1]

# Read in image
IMG_FILE = Image.open(FILE_NAME)
img_array = np.array(IMG_FILE)

# Least significant bit generator
values = ((rgb & 1) for row in img_array for pixel in row for rgb in pixel)

# Read string len from first 32 bits
num = itertools.islice(values, 32)
len_bytes = ba.bitarray(num).tobytes()
value_len = struct.unpack(">I", len_bytes)[0]
#print(value_len)

# Read text
bit_string = itertools.islice(values, value_len)
text_bytes = ba.bitarray(bit_string).tobytes()

password = " "
# Check for password
if len(sys.argv) > 2:
    password = sys.argv[2]

text = decrypt(text_bytes, password)

print(text.decode("utf-8"))
