from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._model = QtGui.QStandardItemModel(3, 8)
        self._table = QtWidgets.QTableView(
            selectionMode=QtWidgets.QAbstractItemView.MultiSelection,
            clicked=self.on_clicked,
        )
        self._table.setModel(self._model)
        self.fill_table()
        self.setCentralWidget(self._table)

    def fill_table(self):
        data = [
            ('A', (0, 0), (1, 4)),
            ('B', (0, 4), (1, 4)),
            ('one', (1, 0), (1, 2)),
            ('two', (1, 2), (1, 2)),
            ('three', (1, 4), (1, 2)),
            ('four', (1, 6), (1, 2)),
            ('x', (2, 0), (1, 1)),
            ('y', (2, 1), (1, 1)),
            ('x', (2, 2), (1, 1)),
            ('y', (2, 3), (1, 1)),
            ('x', (2, 4), (1, 1)),
            ('y', (2, 5), (1, 1)),
            ('x', (2, 6), (1, 1)),
            ('y', (2, 7), (1, 1)),
        ]
        for text, (r, c), (rs, cs) in data:
            it = QtGui.QStandardItem(text)
            self._model.setItem(r, c, it)
            self._table.setSpan(r, c, rs, cs)

    @QtCore.pyqtSlot('QModelIndex')
    def on_clicked(self, ix):
        print('----')
        self._table.clearSelection()
        row, column = ix.row(), ix.column()
        indexes = [ix]
        for i in range(row):
            ix = self._model.index(i, column)
            indexes.append(ix)
        for i in indexes:
            print(i.row(),i.column())
        for ix in indexes:
            r = self._table.visualRect(ix)
            self._table.setSelection(r, QtCore.QItemSelectionModel.Select)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
