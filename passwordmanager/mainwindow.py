from PyQt5 import Qt

import encryptedtableview
import encryptedtablemodel


class MainWindow(Qt.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setup_ui()

        self.create_actions()
        self.create_menus()
        self.create_statusbar()
        self.read_settings()

        self.__current_file = None

    def setup_ui(self):
        self.__encryptedtable = encryptedtableview.EncryptedTableView()
        self.__encryptedtable.setModel(encryptedtablemodel.EncryptedTableModel())
        self.__encryptedtable.resizeColumnsToContents()
        self.setCentralWidget(self.__encryptedtable)

    def new_file(self):
        if self.ok_to_continue():
            self.__encryptedtable.setModel(encryptedtablemodel.EncryptedTableModel())
            self.clear_data()

    def open(self):
        pass

    def save(self):
        if not self.__current_file:
            return self.save_as()
        else:
            return self.save_file(self.__current_file)

    def save_as(self):
        filename = Qt.QFileDialog.getSaveFileName("Save password file", ".", "All files (*.*)")
        if not filename:
            return False
        else:
            return self.save_file(filename)

    def closeEvent(self, event):
        self.write_settings()
        event.accept()

    def clear_data(self):
        pass

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

    def create_menus(self):
        self.__menu_file = self.menuBar().addMenu("&File")
        self.__menu_file.addAction(self.__action_new)
        self.__menu_file.addAction(self.__action_open)
        self.__menu_file.addAction(self.__action_save)
        self.__menu_file.addAction(self.__action_save_as)
        self.__menu_file.addSeparator()
        self.__menu_file.addAction(self.__action_exit)

    def create_statusbar(self):
        locationLabel = Qt.QLabel(" W999 ")
        locationLabel.setAlignment(Qt.Qt.AlignHCenter)
        locationLabel.setMinimumSize(locationLabel.sizeHint())

        formulaLabel = Qt.QLabel()
        formulaLabel.setIndent(3)

        self.statusBar().addWidget(locationLabel)
        self.statusBar().addWidget(formulaLabel)

    def read_settings(self):
        settings = Qt.QSettings("Patrik", "PasswordManager")
        self.restoreGeometry(settings.value("geometry"))

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

    def load_file(self, fileName):
        pass

    def save_file(self, fileName):
        pass
