from Crypto.Cipher import AES
from Crypto import Random

import hashlib

import utils


def create_aes_password(password):
    passhash = hashlib.sha1(utils.get_bytes(password)).digest()
    return passhash[:16]


def decrypt(ciphertext, password):
    iv = ciphertext[:16]
    cdata = ciphertext[16:]
    cipher = AES.new(create_aes_password(password), AES.MODE_CBC, IV=iv)
    plaintext = cipher.decrypt(cdata)
    return plaintext[:-plaintext[-1]]                   # Remove padding


def decrypt_block(ciphertext, password):
    cipher = AES.new(create_aes_password(password), AES.MODE_ECB)
    return cipher.decrypt(ciphertext)


def encrypt(plaintext, password):
    iv = Random.get_random_bytes(16)
    cipher = AES.new(create_aes_password(password), AES.MODE_CBC, IV=iv)
    plain_bytes = utils.get_bytes(plaintext)
    n = 16 - (len(plain_bytes) % 16)
    plain_data = plain_bytes + bytes([n]*n)
    return iv + cipher.encrypt(plain_data)


def encrypt_block(plaintext, password):
    cipher = AES.new(create_aes_password(password), AES.MODE_ECB)
    return cipher.encrypt(plaintext)
