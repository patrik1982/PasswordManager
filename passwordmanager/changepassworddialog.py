import hashlib

from PyQt5 import Qt
from PyQt5 import QtCore

import utils


class ChangePasswordDialog(Qt.QDialog):
    def __init__(self, current_password_hash, *args, **kwargs):
        super(ChangePasswordDialog, self).__init__(*args, **kwargs)

        self.__current_password_hash = current_password_hash
        self.__current_password_input = None
        self.__new_password_input = None
        self.__verify_password_input = None
        self.__ok_cancel = None

        self.init_ui()

        self.update_ok_button()

    def init_ui(self):
        layout = Qt.QHBoxLayout()

        self.__current_password_input = Qt.QLineEdit("")
        self.__current_password_input.textChanged.connect(self.verify_current_password)
        self.__current_password_input.textChanged.connect(self.update_ok_button)
        lbl_current = Qt.QLabel(u"&Current password:")
        lbl_current.setBuddy(self.__current_password_input)

        self.__new_password_input = Qt.QLineEdit("")
        self.__new_password_input.textChanged.connect(self.verify_new_password)
        self.__new_password_input.textChanged.connect(self.update_ok_button)
        lbl_new = Qt.QLabel(u"&New password:")
        lbl_new.setBuddy(self.__new_password_input)

        self.__verify_password_input = Qt.QLineEdit("")
        self.__verify_password_input.textChanged.connect(self.verify_new_password)
        self.__verify_password_input.textChanged.connect(self.update_ok_button)
        lbl_verify = Qt.QLabel(u"&Verify password:")
        lbl_verify.setBuddy(self.__verify_password_input)

        grid_layout = Qt.QGridLayout()
        grid_layout.addWidget(lbl_current, 0, 0)
        grid_layout.addWidget(self.__current_password_input, 0, 1)
        grid_layout.addWidget(lbl_new, 1, 0)
        grid_layout.addWidget(self.__new_password_input, 1, 1)
        grid_layout.addWidget(lbl_verify, 2, 0)
        grid_layout.addWidget(self.__verify_password_input, 2, 1)

        self.__ok_cancel = Qt.QDialogButtonBox(Qt.QDialogButtonBox.Ok | Qt.QDialogButtonBox.Cancel)
        self.__ok_cancel.setOrientation(Qt.Qt.Vertical)
        self.__ok_cancel.accepted.connect(self.accept)
        self.__ok_cancel.rejected.connect(self.reject)

        layout.addLayout(grid_layout)
        layout.addWidget(self.__ok_cancel)

        self.setLayout(layout)

    def verify_current_password(self, current=u""):
        entered_current_password_hash = hashlib.sha256(utils.get_bytes(self.__current_password_input.text())).digest()

        palette = self.__current_password_input.palette()
        password_ok = entered_current_password_hash == self.__current_password_hash
        if password_ok:
            palette.setColor(self.__current_password_input.backgroundRole(), Qt.QColor(220, 255, 220))
        else:
            palette.setColor(self.__current_password_input.backgroundRole(), Qt.QColor(255, 220, 220))
        self.__current_password_input.setPalette(palette)
        return password_ok

    def verify_new_password(self, current=u""):
        palette = self.__verify_password_input.palette()
        password_ok = self.__new_password_input.text() == self.__verify_password_input.text()
        if password_ok:
            palette.setColor(self.__verify_password_input.backgroundRole(), Qt.QColor(220, 255, 220))
        else:
            palette.setColor(self.__verify_password_input.backgroundRole(), Qt.QColor(255, 220, 220))
        self.__verify_password_input.setPalette(palette)
        return password_ok

    def update_ok_button(self, dummy=u""):
        if self.verify_current_password() and self.verify_new_password():
            self.__ok_cancel.button(Qt.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.__ok_cancel.button(Qt.QDialogButtonBox.Ok).setEnabled(False)

    def get_current_password(self):
        return self.__current_password_input.text()

    def get_new_password(self):
        return self.__new_password_input.text()

    def clear(self):
        self.__current_password_input.setText(u"")
        self.__new_password_input.setText(u"")
        self.__verify_password_input.setText(u"")
