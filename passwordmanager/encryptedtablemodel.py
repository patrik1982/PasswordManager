from PyQt5 import Qt
from PyQt5 import QtCore

from Crypto.Cipher import AES
from Crypto import Random

import hashlib

from encryptedstring import EncryptedString


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


def encrypt_block(plaintext, password):
    cipher = AES.new(create_aes_password(password), AES.MODE_ECB)
    return cipher.encrypt(plaintext)


def decrypt_block(ciphertext, password):
    cipher = AES.new(create_aes_password(password), AES.MODE_ECB)
    return cipher.decrypt(ciphertext)


class EncryptedTableModel(Qt.QAbstractTableModel):
    passwordStateChanged = QtCore.pyqtSignal([bool])

    def __init__(self, *args, **kwargs):
        super(EncryptedTableModel, self).__init__(*args, **kwargs)

        self.__headers = None
        self.__table = None
        self.__password_hash = None
        self.__encrypted_random_password = None
        self.__random_password = None

        self.init_data()

    def clear(self):
        self.init_data()
        self.modelReset.emit()

    def init_data(self):
        initial_password = u""
        self.__password_hash = hashlib.sha256(get_bytes(initial_password)).digest()
        random_password = Random.get_random_bytes(16)   # The actual password used
        self.__encrypted_random_password = encrypt_block(random_password, initial_password)
        self.__random_password = None
        self.set_decrypt_only_selected(False)

        # Ugly hack to get an initial database before load-file functionality is implemented
        old_password = u""
        new_password = u"qwerty"
        if self.validate_password(old_password):
            self.__password_hash = hashlib.sha256(get_bytes(new_password)).digest()

            random_password = decrypt_block(self.__encrypted_random_password, old_password)
            self.__encrypted_random_password = encrypt_block(random_password, new_password)
            self.__headers = [EncryptedString(u"Website"), EncryptedString(u"Username"), EncryptedString(u"Password")]
            self.__table = [
                [EncryptedString(u"gmail.com"), EncryptedString(u"patrik1982"), EncryptedString(u"mypass")],
                [EncryptedString(u"yahoo.com"), EncryptedString(u"pater"), EncryptedString(u"mypass")],
                [EncryptedString(u"facebook.com"), EncryptedString(u"nisse"), EncryptedString(u"my!%p4sS")],
                [EncryptedString(u"amazon.de"), EncryptedString(u"björn"), EncryptedString(u"Lösenård fäm")],
            ]
            for row in self.__table:
                row[-1].encrypt(random_password)
            self.__table[1][0].encrypt(random_password)
            self.__table[2][1].encrypt(random_password)
        self.passwordStateChanged.emit(False)

    def decrypt_only_selected(self):
        return self.__decrypt_only_selected

    def set_decrypt_only_selected(self, value):
        self.__decrypt_only_selected = value

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.__table)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.__headers)

    def headerData(self, section, orientation, role=Qt.Qt.DisplayRole):
        if role == Qt.Qt.DisplayRole:
            if orientation == 1:
                return self.__headers[section].get_text()
            else:
                return str(section+1)
        else:
            return Qt.QVariant()

    def setData(self, index=Qt.QModelIndex(), value=Qt.QVariant(), role=Qt.Qt.EditRole):
        if role == Qt.Qt.EditRole:
            self.__table[index.row()][index.column()].set_text(value)
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def data(self, index=Qt.QModelIndex(), role=Qt.Qt.DisplayRole):
        if role == Qt.Qt.DisplayRole:
            if self.__decrypt_only_selected:
                selection = self.parent().selectionModel()
                if index in selection.selectedIndexes():
                    return self.__table[index.row()][index.column()].get_text(self.__random_password)
                else:
                    return self.__table[index.row()][index.column()].get_text()
            else:
                return self.__table[index.row()][index.column()].get_text(self.__random_password)

        elif role == Qt.Qt.EditRole:
            return self.__table[index.row()][index.column()].get_text()

        elif role == Qt.Qt.BackgroundRole:
            if self.__table[index.row()][index.column()].is_encrypted():
                return Qt.QBrush(Qt.QColor(250, 220, 220))
            else:
                return Qt.QVariant()
        else:
            return Qt.QVariant()

    def flags(self, index):
        return Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsSelectable | Qt.Qt.ItemIsEditable

    def validate_password(self, password):
        return hashlib.sha256(get_bytes(password)).digest() == self.__password_hash

    def set_password(self, password):
        if self.validate_password(password):
            self.__random_password = decrypt_block(self.__encrypted_random_password, password)
            self.passwordStateChanged.emit(True)
        else:
            self.__random_password = u""
            self.passwordStateChanged.emit(False)

    def change_password(self, old_password, new_password):
        if self.validate_password(old_password):
            self.__password_hash = hashlib.sha256(get_bytes(new_password)).digest()
            random_password = decrypt_block(self.__encrypted_random_password, old_password)
            self.__encrypted_random_password = encrypt_block(random_password, new_password)
            return True
        else:
            return False

    def insertRow(self, index, parent=Qt.QModelIndex(), *args, **kwargs):
        new_row = [EncryptedString(u""), EncryptedString(u""), EncryptedString(u"")]
        self.beginInsertRows(parent, index, index)
        self.__table.insert(index, new_row)
        self.endInsertRows()
        return True

    def removeRow(self, row, parent=Qt.QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(parent, row, row)
        del self.__table[row]
        self.endRemoveRows()
        return True

    def toggle_encryption(self, index=Qt.QModelIndex()):
        enc_string = self.__table[index.row()][index.column()]

        if self.__random_password:  # A valid password has been entered
            if enc_string.is_encrypted():
                enc_string.decrypt(self.__random_password)
            else:
                enc_string.encrypt(self.__random_password)
            self.dataChanged.emit(index, index)
            return True
        else:
            return False
