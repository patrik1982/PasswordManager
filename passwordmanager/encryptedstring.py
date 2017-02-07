from PyQt5 import Qt

from Crypto.Cipher import AES
from Crypto import Random

import base64
import hashlib

def get_bytes(s):
    if isinstance(s, str):
        s_bytes = s.encode('utf-8')
    elif isinstance(s, bytes):
        s_bytes = s
    elif s is None:
        s_bytes = b""
    else:
        print("Unknown type %s" % (type(s)), s)
        s_bytes = None
    return s_bytes


def create_aes_password(password):
    passhash = hashlib.sha1(get_bytes(password)).digest()
    return passhash[:16]


def decrypt(ciphertext, password):
    iv = ciphertext[:16]
    cdata = ciphertext[16:]
    cipher = AES.new(create_aes_password(password), AES.MODE_CBC, IV=iv)
    plaintext = cipher.decrypt(cdata)
    return plaintext[:-plaintext[-1]]                   # Remove padding


def encrypt(plaintext, password):
    iv = Random.get_random_bytes(16)
    cipher = AES.new(create_aes_password(password), AES.MODE_CBC, IV=iv)
    plain_bytes = get_bytes(plaintext)
    n = 16 - (len(plain_bytes) % 16)
    plain_data = plain_bytes + bytes([n]*n)
    return iv + cipher.encrypt(plain_data)


class EncryptedString(Qt.QObject):
    def __init__(self, data=None, is_encrypted=False, *args, **kwargs):
        super(EncryptedString, self).__init__(*args, **kwargs)

        self.__is_encrypted = is_encrypted
        if is_encrypted:
            self.__data = base64.b64decode(data)
        else:
            self.__data = get_bytes(data)

    def is_encrypted(self):
        return self.__is_encrypted

    def clear(self):
        self.__data = None
        self.__is_encrypted = False

    def encrypt(self, password):
        self.__data = encrypt(self.__data, password)
        self.__is_encrypted = True

    def decrypt(self, password):
        self.__data = decrypt(self.__data, password)
        self.__is_encrypted = False

    def set_text(self, plaintext, password=None):
        self.__data = get_bytes(plaintext)
        self.__is_encrypted = (password is not None)
        if password:
            self.encrypt(password)

    def get_text(self, password=None):
        if self.__is_encrypted:
            if password:
                return decrypt(self.__data, password).decode('utf-8')
            else:
                return base64.b64encode(self.__data).decode('utf-8')
        else:
            return self.__data.decode('utf-8')

    def __str__(self):
        return self.get_text()

    def __repr__(self):
        return "EncryptedString(\"%s\", is_encrypted=%s)" % (self, self.is_encrypted())