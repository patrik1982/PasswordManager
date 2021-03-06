from PyQt5 import Qt

import os

import encryptedtablemodel
import changepassworddialog


UNICODE_PADLOCK = b"\xf0\x9f\x94\x92".decode('utf-8')
UNICODE_OPEN_PADLOCK = b"\xf0\x9f\x94\x93".decode('utf-8')


class MainWindow(Qt.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.__encryptedtable = None
        self.__tablemodel = None

        self.__location_label = None
        self.__lock_label = None

        self.__action_new = None
        self.__action_open = None
        self.__action_save = None
        self.__action_save_as = None
        self.__action_exit = None
        self.__action_toggle_only_selected = None
        self.__action_toggle_encryption = None
        self.__action_insert_row_above = None
        self.__action_insert_row_below = None
        self.__action_delete_row = None
        self.__action_clear_password = None
        self.__action_set_password = None

        self.__menu_file = None
        self.__menu_edit = None
        self.__menu_tools = None

        self.__current_file = None

        self.setup_ui()
        self.create_statusbar()
        self.create_actions()
        self.create_menus()
        self.read_settings()

        self.__tablemodel.clear()

    def setup_ui(self):
        self.__encryptedtable = Qt.QTableView()
        self.__tablemodel = encryptedtablemodel.EncryptedTableModel(parent=self.__encryptedtable)
        self.__tablemodel.passwordStateChanged.connect(self.update_security_display)
        self.__encryptedtable.setModel(self.__tablemodel)
        self.__encryptedtable.resizeColumnsToContents()
        self.setCentralWidget(self.__encryptedtable)

    def update_security_display(self, valid):
        self.__lock_label.setText(UNICODE_PADLOCK)
        palette = self.__lock_label.palette()
        if valid:
            self.__lock_label.setText(u" " + UNICODE_PADLOCK + u" ")
            palette.setColor(Qt.QPalette.Window, Qt.QColor(Qt.Qt.green));
        else:
            self.__lock_label.setText(u" " + UNICODE_OPEN_PADLOCK + u" ")
            palette.setColor(Qt.QPalette.Window, Qt.QColor(Qt.Qt.red));
        self.__lock_label.setPalette(palette);

    def new_file(self):
        if self.ok_to_continue():
            self.__tablemodel.clear()
            self.__encryptedtable.setModel(self.__tablemodel)
            self.__current_file = None

    def open(self):
        (filename, _) = Qt.QFileDialog.getOpenFileName(self, u"Save password file", u".")
        if filename:
            self.load_file(filename)

    def save(self):
        if not self.__current_file:
            return self.save_as()
        else:
            return self.save_file(self.__current_file)

    def save_as(self):
        (filename, _) = Qt.QFileDialog.getSaveFileName(self, u"Save password file", u".")
        if not filename:
            return False
        else:
            return self.save_file(filename)

    def toggle_only_selected(self):
        self.__tablemodel.set_decrypt_only_selected(self.__action_toggle_only_selected.isChecked())
        topleft_index = self.__tablemodel.index(0,0)
        bottomright_index = self.__tablemodel.index(self.__tablemodel.rowCount()-1,self.__tablemodel.columnCount()-1)
        self.__tablemodel.dataChanged.emit(topleft_index, bottomright_index)

    def toggle_encryption(self):
        selection = self.__encryptedtable.selectionModel()
        for index in selection.selectedIndexes():
            self.__tablemodel.toggle_encryption(index)

    def insert_row_above(self):
        selection = self.__encryptedtable.selectionModel()
        current_index = selection.currentIndex()
        if current_index:
            self.__tablemodel.insertRow(current_index.row())

    def insert_row_below(self):
        selection = self.__encryptedtable.selectionModel()
        current_index = selection.currentIndex()
        if current_index:
            self.__tablemodel.insertRow(current_index.row() + 1)

    def delete_row(self):
        selection = self.__encryptedtable.selectionModel()
        current_index = selection.currentIndex()
        if current_index:
            self.__tablemodel.removeRow(current_index.row())

    def set_password(self):
        dlg = changepassworddialog.ChangePasswordDialog(self.__tablemodel.get_password_hash())
        if dlg.exec_() == Qt.QDialog.Accepted:
            self.__tablemodel.change_password(dlg.get_current_password(), dlg.get_new_password())
            self.__tablemodel.set_password(dlg.get_new_password())
            dlg.clear()

    def enter_password(self):
        (text, input_valid) = Qt.QInputDialog.getText(self, u"Enter password", u"Password", Qt.QLineEdit.Password)
        if input_valid:
            self.__tablemodel.set_password(text)

    def clear_password(self):
        self.__tablemodel.set_password(u"")
        self.__tablemodel.modelReset.emit()

    def closeEvent(self, event):
        self.write_settings()
        event.accept()

    def create_actions(self):
        self.__action_new = Qt.QAction(u"&New", self)
        self.__action_new.setShortcut(Qt.QKeySequence.New)
        self.__action_new.setStatusTip(u"Create a new password file")
        self.__action_new.triggered.connect(self.new_file)

        self.__action_open = Qt.QAction(u"&Open", self)
        self.__action_open.setShortcut(Qt.QKeySequence.Open)
        self.__action_open.setStatusTip(u"Open an existing password file")
        self.__action_open.triggered.connect(self.open)

        self.__action_save = Qt.QAction(u"&Save", self)
        self.__action_save.setShortcut(Qt.QKeySequence.Save)
        self.__action_save.setStatusTip(u"Save password file")
        self.__action_save.triggered.connect(self.save)

        self.__action_save_as = Qt.QAction(u"Save &As...", self)
        self.__action_save_as.setShortcut(Qt.QKeySequence.SaveAs)
        self.__action_save_as.setStatusTip(u"Save password file with a new filename")
        self.__action_save_as.triggered.connect(self.save_as)

        self.__action_exit = Qt.QAction(u"E&xit", self)
        self.__action_exit.setShortcut(Qt.QKeySequence.Quit)
        self.__action_exit.setStatusTip(u"Exit")
        self.__action_exit.triggered.connect(self.close)

        self.__action_toggle_only_selected = Qt.QAction(u"&Decrypt selected cells only", self)
        self.__action_toggle_only_selected.setShortcut("Ctrl+W")
        self.__action_toggle_only_selected.setCheckable(True)
        self.__action_toggle_only_selected.changed.connect(self.toggle_only_selected)
        self.__action_toggle_only_selected.setChecked(self.__tablemodel.decrypt_only_selected())

        self.__action_toggle_encryption = Qt.QAction(u"&Toggle encryption for cell", self)
        self.__action_toggle_encryption.setShortcut("Ctrl+T")
        self.__action_toggle_encryption.setStatusTip(u"Turns encryption on/off for current sell")
        self.__action_toggle_encryption.triggered.connect(self.toggle_encryption)

        self.__action_insert_row_above = Qt.QAction(u"&Insert row above", self)
        self.__action_insert_row_above.setStatusTip(u"Insert row above current row")
        self.__action_insert_row_above.triggered.connect(self.insert_row_above)

        self.__action_insert_row_below = Qt.QAction(u"&Insert row below", self)
        self.__action_insert_row_below.setShortcut("Ctrl+A")
        self.__action_insert_row_below.setStatusTip(u"Insert row below current row")
        self.__action_insert_row_below.triggered.connect(self.insert_row_below)

        self.__action_delete_row = Qt.QAction(u"&Delete row", self)
        self.__action_delete_row.setShortcut("Ctrl+D")
        self.__action_delete_row.setStatusTip(u"Delete current row")
        self.__action_delete_row.triggered.connect(self.delete_row)

        self.__action_enter_password = Qt.QAction(u"&Enter password...", self)
        self.__action_enter_password.setShortcut("Ctrl+E")
        self.__action_enter_password.setStatusTip(u"Enter password for current file")
        self.__action_enter_password.triggered.connect(self.enter_password)

        self.__action_clear_password = Qt.QAction(u"&Clear password...", self)
        self.__action_clear_password.setShortcut("Ctrl+C")
        self.__action_clear_password.setStatusTip(u"Clear password for current file")
        self.__action_clear_password.triggered.connect(self.clear_password)

        self.__action_set_password = Qt.QAction(u"&Set password...", self)
        self.__action_set_password.setShortcut("Ctrl+P")
        self.__action_set_password.setStatusTip(u"Set password for current file")
        self.__action_set_password.triggered.connect(self.set_password)

    def create_menus(self):
        self.__menu_file = self.menuBar().addMenu("&File")
        self.__menu_file.addAction(self.__action_new)
        self.__menu_file.addAction(self.__action_open)
        self.__menu_file.addAction(self.__action_save)
        self.__menu_file.addAction(self.__action_save_as)
        self.__menu_file.addSeparator()
        self.__menu_file.addAction(self.__action_exit)

        self.__menu_edit = self.menuBar().addMenu("&Edit")
        self.__menu_edit.addAction(self.__action_toggle_only_selected)
        self.__menu_edit.addAction(self.__action_toggle_encryption)
        self.__menu_edit.addAction(self.__action_insert_row_above)
        self.__menu_edit.addAction(self.__action_insert_row_below)
        self.__menu_edit.addAction(self.__action_delete_row)

        self.__menu_tools = self.menuBar().addMenu("&Tools")
        self.__menu_tools.addAction(self.__action_enter_password)
        self.__menu_tools.addAction(self.__action_clear_password)
        self.__menu_tools.addAction(self.__action_set_password)

    def create_statusbar(self):
        self.__location_label = Qt.QLabel(" W999 ")
        self.__location_label.setAlignment(Qt.Qt.AlignHCenter)
        self.__location_label.setMinimumSize(self.__location_label.sizeHint())

        self.__lock_label = Qt.QLabel(u"")
        self.__lock_label.setAutoFillBackground(True)
        self.__lock_label.setAlignment(Qt.Qt.AlignHCenter)
        self.__lock_label.setMinimumSize(self.__lock_label.sizeHint())

        self.statusBar().addWidget(self.__location_label)
        self.statusBar().addWidget(self.__lock_label)

    def read_settings(self):
        settings = Qt.QSettings("Patrik", "PasswordManager")
        saved_geometry = settings.value("geometry")
        if saved_geometry:
            self.restoreGeometry(saved_geometry)

    def write_settings(self):
        settings = Qt.QSettings("Patrik", "PasswordManager")
        settings.setValue("geometry", self.saveGeometry())

    def ok_to_continue(self):
        if self.isWindowModified():
            response = Qt.QMessageBox.Warning("Password Manager",
                                              "The document has been modified\nDo you want to save your changes?",
                                              Qt.QMessageBox.Yes | Qt.QMessageBox.No | Qt.QMessageBox.Cancel)
            if response == Qt.QMessageBox.Yes:
                return self.save()
            elif response == Qt.QMessageBox.Cancel:
                return False
        return True

    def load_file(self, filename):
        savefile = open(filename, 'r')
        savedata = ''.join(savefile.readlines())
        savefile.close()
        self.__tablemodel.load_savedata(savedata)
        self.__current_file = filename
        self.__action_toggle_only_selected.setChecked(self.__tablemodel.decrypt_only_selected())

    def save_file(self, filename):
        backup_created = False
        if os.path.exists(filename):
            os.rename(filename, filename+u".backup")
            backup_created = True

        savedata = self.__tablemodel.get_savedata()
        savefile = open(filename, 'w')
        savefile.write(savedata)
        savefile.close()
        self.__current_file = filename

        if backup_created:
            os.remove(filename+u".backup")
