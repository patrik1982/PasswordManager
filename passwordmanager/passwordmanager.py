from PyQt5 import Qt

import mainwindow


if __name__ == '__main__':

    if True:
        import sys

        app = Qt.QApplication(sys.argv)
        app.setApplicationName("Password Manager")

        passwordmanager = mainwindow.MainWindow()
        passwordmanager.show()

        sys.exit(app.exec_())
    else:
        import encryptedstring

        a = encryptedstring.EncryptedString()
        a.set_text(u"Patrik")
        print(a.get_text())
        a.set_text(u"Patrik ", u"qwertyuiqwertyui")
        print(a.get_text())
        print(a.get_text(u"qwertyuiqwertyui"))
        a.set_text(u"Paåtrik", u"qwertyuiqwertyui")
        print(a.get_text())
        print(a.get_text(u"qwertyuiqwertyui"))
        print()
        print('str:  %s' % a)
        print('repr: %r' % a)
        a.set_text(u"Påtrik")
        print('str:  %s' % a)
        print('repr: %r' % a)
        print()

        a = encryptedstring.EncryptedString("Påtrik", False)
        print(a.get_text())
        a = encryptedstring.EncryptedString("WAc1TmDlTIYZ10XH7vbm8D5BNocCTqgztCkpz++Mpq8=", True)
        print(a.get_text())
        print(a.get_text(u"qwertyuiqwertyui"))
