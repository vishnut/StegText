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
#from Crypto.Cipher import AES
from Crypto.Cipher import XOR

def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string)

# Input
FILE_NAME = sys.argv[1]
text = sys.argv[2]
"""
diff = len(text) % 16
if diff:
    diff = 16 - diff
    text += diff * ' '
"""
# XOR text with password if given
if len(sys.argv) > 3:
    text = base64.b64encode(XOR.new(sys.argv[3]).encrypt(text))
    print(str(text))
else:
    text = base64.b64encode(XOR.new(" ").encrypt(text))
    print(str(text))
    #sys.argv[3]
    #text = obj.encrypt(text)

# Read in image
IMG_FILE = Image.open(FILE_NAME)
img_array = np.array(IMG_FILE)

# Text to bitstring
text_bytes = ba.bitarray()
#text_bytes.fromstring(text)
text_bytes.frombytes(text)

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

Image.fromarray(img_array).save('out.bmp')
IMG_FILE = Image.open('out.bmp')
img_array = np.array(IMG_FILE)

print("Saved as out.bmp")

