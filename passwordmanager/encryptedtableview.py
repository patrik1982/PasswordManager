from PyQt5 import Qt

class EncryptedTableView(Qt.QTableView):
    def __init__(self, *args, **kwargs):
        super(EncryptedTableView, self).__init__(*args, **kwargs)
        self.setWordWrap(False)
