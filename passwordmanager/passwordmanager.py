from PyQt5 import Qt

class MainWindow(Qt.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUI()

    def setupUI(self):
        pass


if __name__ == '__main__':

    if False:
        import sys

        app = Qt.QApplication(sys.argv)
        app.setApplicationName("Password Manager")

        passwordmanager = MainWindow()
        passwordmanager.show()

        sys.exit(app.exec_())
    else:
        import encryptedstring

        a = encryptedstring.EncryptedString()
        a.set_text(b"Patrik")
        print(a.get_text())
        a.set_text(b"Patrik", b"qwertyuiqwertyui")
        print(a.get_text())
        print(a.get_text(b"qwertyuiqwertyui"))
        a.set_text(b"Patrik", b"qwertyuiqwertyui")
        print(a.get_text())
        print(a.get_text(b"qwertyuiqwertyui"))
