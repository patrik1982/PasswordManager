from PyQt5 import Qt

from Crypto import Random

from encryptedstring import EncryptedString


class EncryptedTableModel(Qt.QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super(EncryptedTableModel, self).__init__(*args, **kwargs)

        self.__headers = None
        self.__table = None
        self.__password = u""
        self.__random_password = None

        self.init_data()

    def clear(self):
        self.init_data()
        self.modelReset.emit()

    def init_data(self):
        password = u"qwerty"
        self.__headers = [EncryptedString(u"Website"), EncryptedString(u"Username"), EncryptedString(u"Password")]
        self.__table = [
            [EncryptedString(u"gmail.com"), EncryptedString(u"patrik1982"), EncryptedString(u"mypass")],
            [EncryptedString(u"yahoo.com"), EncryptedString(u"pater"), EncryptedString(u"mypass")],
            [EncryptedString(u"facebook.com"), EncryptedString(u"nisse"), EncryptedString(u"my!%p4sS")],
            [EncryptedString(u"amazon.de"), EncryptedString(u"björn"), EncryptedString(u"Lösenård fäm")],
        ]
        for row in self.__table:
            row[-1].encrypt(password)
        self.__table[1][0].encrypt(password)
        self.__table[2][1].encrypt(password)

        self.__password = password

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
            return self.__table[index.row()][index.column()].get_text()

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

    def set_password(self, password):
        self.__password = password

    def insertRow(self, index, parent=Qt.QModelIndex(), *args, **kwargs):
        new_row = [EncryptedString(u""), EncryptedString(u""), EncryptedString(u"")]
        self.beginInsertRows(parent, index, index)
        self.__table.insert(index, new_row)
        self.endInsertRows()

    def removeRow(self, row, parent=Qt.QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(parent, row, row)
        del self.__table[row]
        self.endRemoveRows()
        return True
