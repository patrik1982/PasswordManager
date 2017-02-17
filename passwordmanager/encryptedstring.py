import base64

from PyQt5 import Qt

import crypto_utils
import utils


class EncryptedString(Qt.QObject):
    def __init__(self, data=None, is_encrypted=False, *args, **kwargs):
        super(EncryptedString, self).__init__(*args, **kwargs)

        self.__is_encrypted = is_encrypted
        if is_encrypted:
            self.__data = base64.b64decode(data)
        else:
            self.__data = utils.get_bytes(data)

    def is_encrypted(self):
        return self.__is_encrypted

    def clear(self):
        self.__data = None
        self.__is_encrypted = False

    def encrypt(self, password):
        self.__data = crypto_utils.encrypt(self.__data, password)
        self.__is_encrypted = True

    def decrypt(self, password):
        self.__data = crypto_utils.decrypt(self.__data, password)
        self.__is_encrypted = False

    def set_text(self, plaintext, password=None):
        self.__data = utils.get_bytes(plaintext)
        self.__is_encrypted = (password is not None)
        if password:
            self.encrypt(password)

    def get_text(self, password=None):
        if self.__is_encrypted:
            if password:
                return crypto_utils.decrypt(self.__data, password).decode('utf-8')
            else:
                return base64.b64encode(self.__data).decode('utf-8')
        else:
            return self.__data.decode('utf-8')

    def __str__(self):
        return self.get_text()

    def __repr__(self):
        return "EncryptedString(\"%s\", is_encrypted=%s)" % (self, self.is_encrypted())
