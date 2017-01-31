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
    def __init__(self, parent=None):
        super(EncryptedString, self).__init__(parent)

        self.__plaintext = None
        self.__ciphertext = None

    def is_encrypted(self):
        return self.__ciphertext is not None

    def clear(self):
        self.__ciphertext = None
        self.__plaintext = None

    def encrypt(self, password):
        self.__ciphertext = encrypt(self.__plaintext, password)
        self.__plaintext = None

    def decrypt(self, password):
        self.__plaintext = decrypt(self.__ciphertext, password)
        self.__ciphertext = None

    def set_text(self, plaintext, password=None):
        if password:
            self.__ciphertext = encrypt(plaintext, password)
            self.__plaintext = None
        else:
            self.__plaintext = plaintext
            self.__ciphertext = None

    def get_text(self, password=None):
        if self.is_encrypted():
            if password:
                return decrypt(self.__ciphertext, password)
            else:
                return self.__ciphertext
        else:
            return self.__plaintext
