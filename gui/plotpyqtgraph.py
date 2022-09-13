# import pyside6 QtCore QtGui QtWidgets
from turtle import width
from PySide6 import QtCore, QtGui, QtWidgets


import numpy as np
import pyqtgraph as pg

# dialog class
class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)

        # histogram
        data = {123: (30, "#ff0000"), 456: (50, "#00ff00"), 789: (10, "#0000ff"), 101: (60, "#ffff00")}
        # x - axis is index of data
        x = np.arange(len(data))
        # y - axis is value of data
        print([d[0] for d in data.values()])
        y = np.array([d[0] for d in data.values()])
        # plot histogram with bar in different color
        
        win = pg.plot()
        # bar graph with different color
        self.graphWidget = pg.BarGraphItem(x=x, height=y, width=0.5, brushes=['#ff0000', '#00ff00', '#0000ff', '#ffff00'])
        # x label
        self.graphWidget.setOpts(xlabel='CP ID', ylabel='Usage', title='CP Usage')
        win.addItem(self.graphWidget)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(win)

        # set layout
        self.setLayout(self.layout)

    def update_input(self):
        print(self.input_edit.text())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = SettingsDialog()
    dialog.show()
    sys.exit(app.exec_())