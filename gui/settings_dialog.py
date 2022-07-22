# import pyside6 QtCore QtGui QtWidgets
from PySide6 import QtCore, QtGui, QtWidgets

# dialog class
class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Configure Settings")
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #f0f0f0")

        rgb_label = []
        self.rgb_edit = []
        # horizontal layout
        rgb_layout = QtWidgets.QHBoxLayout()
        for c in ["r", "g", "b"]:
            # horizontal layout
            c_layout = QtWidgets.QHBoxLayout()
            rgb_label.append(QtWidgets.QLabel("<b>%s</b>" % c))
            self.rgb_edit.append(QtWidgets.QLineEdit())
            self.rgb_edit[-1].setValidator(QtGui.QIntValidator(0, 255))
            self.rgb_edit[-1].setText("0")
            self.rgb_edit[-1].setStyleSheet("background-color: #fff")
            self.rgb_edit[-1].setAlignment(QtCore.Qt.AlignCenter)
            # signal/slot
            self.rgb_edit[-1].textChanged.connect(self.update_color)
            c_layout.addWidget(rgb_label[-1])
            c_layout.addWidget(self.rgb_edit[-1])
            rgb_layout.addLayout(c_layout)

        # slider for [ambient, diffuse, specular] factor
        # vertical layout
        ads_layout = QtWidgets.QVBoxLayout()
        self.factor_slider = []
        for i, f in enumerate(["Ambient", "Diffuse", "Specular", "Specular Power"]):
            # horizontal layout
            factor_layout = QtWidgets.QHBoxLayout()
            # label
            self.factor_label = QtWidgets.QLabel("<b>" + f + " factor</b>")
            self.factor_label.setAlignment(QtCore.Qt.AlignCenter)
            # constant width label
            self.factor_label.setFixedWidth(100)
            # slider
            self.factor_slider.append(QtWidgets.QSlider(QtCore.Qt.Horizontal))
            self.factor_slider[i].setMinimum(0)
            self.factor_slider[i].setMaximum(100)
            self.factor_slider[i].setValue(50)
            self.factor_slider[i].setTickPosition(QtWidgets.QSlider.TicksBelow)
            self.factor_slider[i].setTickInterval(10)
            self.factor_slider[i].setStyleSheet("background-color: #fff")
            self.factor_slider[i].setFocusPolicy(QtCore.Qt.NoFocus)
            self.factor_slider[i].valueChanged.connect(self.update_light_factor)
            # add to layout
            factor_layout.addWidget(self.factor_label)
            factor_layout.addWidget(self.factor_slider[i])
            # add to vertical layout
            ads_layout.addLayout(factor_layout)

        # line edit for Ambient occlustion factor and Ambient occlustion kernel size
        # vertical layout
        ao_layout = QtWidgets.QVBoxLayout()
        self.ao_edit = []
        for i, f in enumerate(["Ambient Occlusion Factor", "Ambient Occlusion Kernel Size"]):
            # horizontal layout
            ao_hlayout = QtWidgets.QHBoxLayout()
            # label
            ao_label = QtWidgets.QLabel("<b>" + f + "</b>")
            ao_label.setAlignment(QtCore.Qt.AlignCenter)
            # constant width label
            ao_label.setFixedWidth(200)
            # line edit
            self.ao_edit.append(QtWidgets.QLineEdit())
            self.ao_edit[i].setText("0")
            self.ao_edit[i].setStyleSheet("background-color: #fff")
            self.ao_edit[i].setAlignment(QtCore.Qt.AlignCenter)
            # signal/slot on finished editing
            self.ao_edit[i].editingFinished.connect(self.update_ao_factor)
            # add to layout
            ao_hlayout.addWidget(ao_label)
            ao_hlayout.addWidget(self.ao_edit[i])
            # add to vertical layout
            ao_layout.addLayout(ao_hlayout)

        # close button
        self.close_button = QtWidgets.QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        # create layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(rgb_layout)
        self.layout.addLayout(ads_layout)
        self.layout.addLayout(ao_layout)
        self.layout.addWidget(self.close_button)

        # set layout
        self.setLayout(self.layout)
    
    def update_color(self):
        try:
            r = int(self.rgb_edit[0].text())
            g = int(self.rgb_edit[1].text())
            b = int(self.rgb_edit[2].text())
            print(r, g, b)
        except ValueError:
            return

    def update_light_factor(self):
        for i in range(3):
            print(self.factor_slider[i].value())

    def update_ao_factor(self):
        for i in range(2):
            print(self.ao_edit[i].text())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = SettingsDialog()
    dialog.show()
    sys.exit(app.exec_())