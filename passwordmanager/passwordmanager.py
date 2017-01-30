from PyQt5 import Qt

class MainWindow(Qt.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUI()

    def setupUI(self):
        pass


if __name__ == '__main__':
    import sys

    app = Qt.QApplication(sys.argv)
    app.setApplicationName("Password Manager")

    passwordmanager = MainWindow()
    passwordmanager.show()

    sys.exit(app.exec_())