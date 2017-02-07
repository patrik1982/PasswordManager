from PyQt5 import Qt

from Crypto.Cipher import AES
from Crypto import Random


def decrypt(ciphertext, password):
    iv = ciphertext[:16]
    cdata = ciphertext[16:]
    cipher = AES.new(password, AES.MODE_CBC, IV=iv)
    plaintext = cipher.decrypt(cdata)
    return plaintext[:-plaintext[-1]]                   # Remove padding


def encrypt(plaintext, password):
    iv = Random.get_random_bytes(16)
    cipher = AES.new(password, AES.MODE_CBC, IV=iv)
    n = 16 - (len(plaintext) % 16)
    plain_data = plaintext + bytes([n]*n)
    return iv + cipher.encrypt(plain_data)


class EncryptedString(Qt.QObject):
    def __init__(self, *args, **kwargs):
        super(EncryptedString, self).__init__(*args, **kwargs)

        self.__data = None
        self.__is_encrypted = False

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
        self.__data = plaintext
        self.__is_encrypted = (password is not None)
        if password:
            self.encrypt(password)

    def get_text(self, password=None):
        if self.__is_encrypted:
            if password:
                return decrypt(self.__data, password)
            else:
                return self.__data
        else:
            return self.__data
