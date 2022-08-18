# import pyside6 QtCore QtGui QtWidgets
from PySide6 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
import numpy as np

# use Qt5Agg backend
matplotlib.use("QtAgg")


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


# dialog class
class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Configure Settings")
        # self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #f0f0f0")

        # horizontal layout to hold text input and button
        input_layout = QtWidgets.QHBoxLayout()
        # text label
        self.input_label = QtWidgets.QLabel("<b>Enter CP ID : </b>")
        self.input_label.setAlignment(QtCore.Qt.AlignCenter)
        # text input
        self.input_edit = QtWidgets.QLineEdit()
        self.input_edit.setAlignment(QtCore.Qt.AlignCenter)
        # self.input_edit.setFixedWidth(200)
        # button
        self.input_button = QtWidgets.QPushButton("Submit")
        self.input_button.setFixedWidth(100)
        self.input_button.clicked.connect(self.update_input)
        # add to layout
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(self.input_button)
        

        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # title to plot
        sc.axes.set_title("Plot")
        # sc.axes.plot([0, 1, 2, 3], [0, 1, 2, 3])

        # histogram
        data = {123: (30, "#ff0000"), 456: (50, "#00ff00"), 789: (10, "#0000ff"), 101: (60, "#ffff00")}
        # x - axis is index of data
        x = np.arange(len(data))
        # y - axis is value of data
        print([d[0] for d in data.values()])
        y = np.array([d[0] for d in data.values()])
        # plot histogram with bar in different color
        sc.axes.bar(x, y, align="center", color=[c[1] for c in data.values()])
       
        # legend for each bar
        for i, v in enumerate(data):
            sc.axes.text(x[i], y[i] + 1, str(v), ha="center")

        # hide x axis values
        sc.axes.set_xticks([])


        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(input_layout)
        self.layout.addWidget(sc)
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