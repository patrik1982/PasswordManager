from PyQt5 import Qt

from encryptedstring import EncryptedString


class EncryptedTableModel(Qt.QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super(EncryptedTableModel, self).__init__(*args, **kwargs)

        password = b"qwerty"
        self.__headers = [EncryptedString(u"Website"), EncryptedString(u"Username"), EncryptedString(u"Password")]
        self.__table = [
            [EncryptedString(u"gmail.com"), EncryptedString(u"patrik1982"), EncryptedString(u"mypass")],
            [EncryptedString(u"yahoo.com"), EncryptedString(u"patjak"), EncryptedString(u"my pass")],
            [EncryptedString(u"facebook.com"), EncryptedString(u"nisse"), EncryptedString(u"my!%p4sS")],
            [EncryptedString(u"amazon.de"), EncryptedString(u"björn"), EncryptedString(u"Lösenård fäm")],
        ]
        for row in self.__table:
            row[-1].encrypt(password)
        self.__table[1][0].encrypt(password)
        self.__table[2][1].encrypt(password)


    def rowCount(self, parent=Qt.QModelIndex()):
        return len(self.__table)

    def columnCount(self, parent=Qt.QModelIndex()):
        return len(self.__headers)

    def headerData(self, section, orientation, role=Qt.Qt.DisplayRole):
        if role == Qt.Qt.DisplayRole:
            if orientation == 1:
                return self.__headers[section].get_text()
            else:
                return str(section+1)
        else:
            return None

    def data(self, index=Qt.QModelIndex(), role=Qt.Qt.DisplayRole):
        if role == Qt.Qt.DisplayRole:
            return self.__table[index.row()][index.column()].get_text()
        elif role == Qt.Qt.BackgroundRole:
            if self.__table[index.row()][index.column()].is_encrypted():
                return Qt.QBrush(Qt.QColor(250, 220, 220))
            else:
                return None
        else:
            return None
