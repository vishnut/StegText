# pylint: disable=C0103

"""
Take an input image
Hide text in the image
Optional password
"""

import sys
import os
import struct
from PIL import Image
import numpy as np
import bitarray as ba

# Input
FILE_NAME = sys.argv[1]
text = sys.argv[2]

# XOR text with password if given
if len(sys.argv) > 3:
    text ^= sys.argv[3]

# Read in image
IMG_FILE = Image.open(FILE_NAME)
img_array = np.array(IMG_FILE)

# Text to bitstring
text_bytes = ba.bitarray()
text_bytes.fromstring(text)

# Text length to bitstring
str_len = len(text_bytes)
len_bytes = ba.bitarray()
len_bytes.frombytes(struct.pack(">I", str_len))

out_bitstring = list(len_bytes)
out_bitstring.extend(text_bytes)
print(out_bitstring)

index = 0
for ix, ival in enumerate(img_array):
    for jx, jval in enumerate(ival):
        for kx, _ in enumerate(jval):
            try:
                if out_bitstring[index]:
                    img_array[ix][jx][kx] |= 1
                else:
                    img_array[ix][jx][kx] &= ~1
                print(out_bitstring[index], img_array[ix][jx][kx])
                index += 1
            except IndexError:
                break

print("before")
index = 0
for ix, ival in enumerate(img_array):
    for jx, jval in enumerate(ival):
        for kx, _ in enumerate(jval):
            if index < 8:
                print(img_array[ix][jx][kx])
                index += 1

Image.fromarray(img_array).save('out.bmp')
IMG_FILE = Image.open('out.bmp')
img_array = np.array(IMG_FILE)

print("new")
index = 0
for ix, ival in enumerate(img_array):
    for jx, jval in enumerate(ival):
        for kx, _ in enumerate(jval):
            if index < 8:
                print(img_array[ix][jx][kx])
                index += 1




