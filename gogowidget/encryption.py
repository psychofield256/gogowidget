from os import path
import rsa

def loadorgen(keyfilenames:tuple, size:int=2048):
    "Try to load keys in files. If cannot, create and save them in files."
    publicfile, privatefile = keyfilenames
    try:
        with open(publicfile, 'rb') as f:
            publickey = rsa.PublicKey.load_pkcs1(f.read())
        with open(privatefile, 'rb') as f:
            privatekey = rsa.PrivateKey.load_pkcs1(f.read())
    except IOError:
        publickey, privatekey = rsa.newkeys(size)
        with open(publicfile, 'wb') as f:
            f.write(publickey.save_pkcs1())
        with open(privatefile, 'wb') as f:
            f.write(privatekey.save_pkcs1())
    return (publickey, privatekey)
