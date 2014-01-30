#!/usr/bin/env python
import base64
import hashlib
import hmac
import time
import sys


SECRET = '-ENTER_YOUR_SECRET_HERE-'
PERIOD = 30.0

counter = int(time.time() / PERIOD)

def int_to_bytestring(i, padding=8):
    result = []
    while i != 0:
        result.append(chr(i & 0xFF))
        i = i >> 8
    return ''.join(reversed(result)).rjust(padding, '\0')

secret = base64.b32decode(SECRET, casefold=True)
msg = int_to_bytestring(counter)
hmac_hash = hmac.new(secret, msg, hashlib.sha1).digest()

offset = ord(hmac_hash[19]) & 0xf
code = ((ord(hmac_hash[offset]) & 0x7f) << 24 |
    (ord(hmac_hash[offset + 1]) & 0xff) << 16 |
    (ord(hmac_hash[offset + 2]) & 0xff) << 8 |
    (ord(hmac_hash[offset + 3]) & 0xff))

token = code % 1000000

sys.stdout.write(" %06d" % token)
