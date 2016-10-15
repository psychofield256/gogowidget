import base64
import bz2

def compress(bindata):
    return bz2.compress(base64.b64encode(bindata))

def decompress(bindata):
    return base64.b64decode(bz2.decompress(bindata))
