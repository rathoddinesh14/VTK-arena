from cProfile import label
from PySide6 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Toolbar")

        label = QtWidgets.QLabel("Toolbar")
        self.setCentralWidget(label)

        toolbar = QtWidgets.QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        action = QtGui.QAction("New", self)
        action.setStatusTip("New document")
        action.triggered.connect(self.onToolbarAction)
        toolbar.addAction(action)

        # separator
        toolbar.addSeparator()

        action = QtGui.QAction("Open", self)
        action.setStatusTip("Open existing document")
        action.triggered.connect(self.onToolbarAction)
        toolbar.addAction(action)

    def onToolbarAction(self, s):
        print(s)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())