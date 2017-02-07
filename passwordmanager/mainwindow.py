from PyQt5 import Qt

import encryptedtableview
import encryptedtablemodel


class MainWindow(Qt.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)



        self.setup_ui()

        self.create_statusbar()
        self.read_settings()

    def setup_ui(self):
        self.__tablemodel = encryptedtablemodel.EncryptedTableModel()
        self.__encryptedtable = encryptedtableview.EncryptedTableView()
        self.__encryptedtable.setModel(self.__tablemodel)
        self.__encryptedtable.resizeColumnsToContents()
        self.setCentralWidget(self.__encryptedtable)

    def new_file(self):
        pass

    def open(self):
        pass

    def save(self):
        pass

    def save_as(self):
        pass

    def closeEvent(self, event):
        self.write_settings()
        event.accept()

    def create_actions(self):
        pass

    def create_menus(self):
        pass

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

    def loadFile(self, fileName):
        pass

    def saveFile(self, fileName):
        pass
