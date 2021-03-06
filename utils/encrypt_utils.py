import base64
import json
import os

from Crypto.Cipher import AES

modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'


def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def encrypted_request(text):
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    return data


def test():
    print encrypted_request(
        'htPNp6MUYqXd/c2YsIovhhmQnn/5Y62aIPK6CTyRDLAA8okWvdwz6UC58AC2pe+tk6A9B9DgEG9H6m9Yt7mzRQyB3nWjvdvrXSiUxxY0BzMzilEP+2RO7LToRLfPpLRY9Y7+/YuO/9iIoPFzArhn8pnAS+r5UbQ7wZTWQ6iUd1cfu+A557dS5w2GmybQuXOYq8BFva9j3vj/4Cy4k3s4fmnj4z2XrZmFZn9Ngdy2ppY=')


if __name__ == '__main__':
    test()
