import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget,\
    QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout
from PySide6.QtGui import QPainter, QBrush, QPen, QPolygonF, \
    QPainterPath, QLinearGradient, QColor
from PySide6.QtCore import Qt, QPoint
import vtk
import random
import colormapdropdown
import os

from qtrangeslider import QRangeSlider

QSS = """
QSlider {
    min-height: 20px;
}

QSlider::groove:horizontal {
    border: 0px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #888, stop:1 #ddd);
    height: 20px;
    border-radius: 10px;
}

QSlider::handle {
    background: qradialgradient(cx:0, cy:0, radius: 1.2, fx:0.35,
                                fy:0.3, stop:0 #eef, stop:1 #002);
    height: 20px;
    width: 20px;
    border-radius: 10px;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #227, stop:1 #77a);
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
}

QRangeSlider {
    qproperty-barColor: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #227, stop:1 #77a);
}
"""



def make_lut(table_size):
    table = vtk.vtkLookupTable()
    table.SetNumberOfTableValues(table_size)
    table.SetTableRange(0, table_size)
    table.Build()

    nc = vtk.vtkNamedColors()

    # Set the colors in the lookup table with random colors
    for i in range(table_size):
        table.SetTableValue(i, random.random(), random.random(), random.random(), 1.0)
        # print(table.GetTableValue(i))

    return table

class TransferFunctionWidget(QWidget):
    def __init__(self, parent=None):
        super(TransferFunctionWidget, self).__init__(parent)
        self.setFixedSize(parent.widget_width, parent.widget_height)
        self.points = []
        self.selected_point = None
        # Load the vtk color map
        self.lut = make_lut(256)

    def add_point(self, x, y):
        self.points.append(QPoint(x, y))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(Qt.white))
        painter.drawLine(0, self.height(), self.width(), self.height())
        painter.drawLine(0, 0, 0, self.height())

        polygon = QPolygonF(self.points)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawPolyline(polygon)

        for point in self.points:
            painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
            painter.drawPoint(point)

        if self.selected_point:
            painter.setPen(QPen(Qt.blue, 5, Qt.SolidLine))
            painter.drawPoint(self.selected_point)

        # fill the transfer function
        self.fill_transfer_function(painter)

    def mousePressEvent(self, event):
        curr_pos = event.position()
        for point in self.points:
            if (curr_pos - point).manhattanLength() <= 5:
                self.selected_point = point
                break
        else:
            # add new point in the sorted order of x
            for i, point in enumerate(self.points):
                if curr_pos.x() < point.x():
                    self.points.insert(i, curr_pos)
                    self.update()
                    return
            
            self.add_point(curr_pos.x(), curr_pos.y())

    def fill_transfer_function(self, painter : QPainter):
        path = QPainterPath()
        path.moveTo(0, self.height())

        for point in self.points:
            path.lineTo(point)

        path.lineTo(self.width(), self.height())
        path.closeSubpath()

        # Create the gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)
        num_of_colors = self.lut.GetNumberOfTableValues()
        for i in range(num_of_colors):
            color = [0, 0, 0]
            self.lut.GetColor(float(i)/num_of_colors, color)
            gradient.setColorAt(float(i)/num_of_colors, QColor(color[0]*255, color[1]*255, color[2]*255))

        painter.fillPath(path, QBrush(gradient))

    def mouseMoveEvent(self, event):
        if self.selected_point:
            curr_pos = event.position()
            # make sure the point between next and previous point
            if self.selected_point != self.points[0]:
                prev_point = self.points[self.points.index(self.selected_point) - 1]
                if curr_pos.x() < prev_point.x():
                    curr_pos.setX(prev_point.x())
            if self.selected_point != self.points[-1]:
                next_point = self.points[self.points.index(self.selected_point) + 1]
                if curr_pos.x() > next_point.x():
                    curr_pos.setX(next_point.x())

            # check if the point is in the widget
            if curr_pos.x() < 0:
                curr_pos.setX(0)
            if curr_pos.x() > self.width():
                curr_pos.setX(self.width())
            
            if curr_pos.y() < 0:
                curr_pos.setY(0)
            if curr_pos.y() > self.height():
                curr_pos.setY(self.height())

            self.selected_point.setX(curr_pos.x())
            self.selected_point.setY(curr_pos.y())
            self.update()

    def update_cmap(self, cmap):
        self.lut = cmap
        self.update()

    def set_control_points(self, points):
        x1 = self.width() * points[0] / 100
        x2 = self.width() * points[1] / 100
        y1 = self.height() / 2
        y2 = self.height() / 2
        self.points = [ QPoint(0, self.height()),
                        QPoint(x1, self.height()),
                        QPoint(x1, y1),
                        QPoint(x2, y2),
                        QPoint(x2, self.height()),
                        QPoint(self.width(), self.height())]
        self.update()

class RangeSlider(QWidget):
    def __init__(self, parent=None):
        super(RangeSlider, self).__init__(parent)
        self.parent_widget : TransferFunctionWithColorMap = parent
        self.styled_range_hslider = QRangeSlider(Qt.Horizontal)
        self.styled_range_hslider.setValue((20, 80))
        self.styled_range_hslider.setStyleSheet(QSS)

        # create labels
        self.label_left = QLabel("0", self)
        self.label_right = QLabel("100", self)
        self.label_min = QLabel("Min", self)
        self.label_max = QLabel("Max", self)

        # create layout
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label_left)
        hbox1.addStretch(1)
        hbox1.addWidget(self.label_right)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.label_min)
        hbox2.addStretch(1)
        hbox2.addWidget(self.label_max)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox1)
        vbox.addWidget(self.styled_range_hslider)
        vbox.addLayout(hbox2)

        # on slider value change
        self.styled_range_hslider.valueChanged.connect(self.on_slider_value_change)

        self.layout = vbox

    def on_slider_value_change(self, value):
        value = self.styled_range_hslider.value()
        self.label_left.setText(str(value[0]))
        self.label_right.setText(str(value[1]))
        self.parent_widget.transfer_function_widget.set_control_points(value)

class TransferFunctionWithColorMap(QWidget):
    def __init__(self, parent=None):
        super(TransferFunctionWithColorMap, self).__init__(parent)
        self.widget_width = 500
        self.widget_height = 500

        self.layout = QVBoxLayout(self)
        self.transfer_function_widget = TransferFunctionWidget(self)
        self.transfer_function_widget.add_point(0, self.widget_height)
        self.transfer_function_widget.add_point(self.widget_width, 0)
        self.layout.addWidget(self.transfer_function_widget)
        
        base_loc = "/home/dinesh/Downloads/keycolormaps/KeyColormaps"
        colormaps = []
        for i in os.listdir(base_loc):
            if i.endswith(".png"):
                filename = i.split(".")[0]
                colormaps.append(colormapdropdown.ColorMap(filename, 
                                        os.path.join(base_loc, filename + ".xml"), 
                                        os.path.join(base_loc, i)))

        self.color_map_widget = colormapdropdown.ColormapChooserWidget(colormaps,
                                                self.widget_width,
                                                self.transfer_function_widget)
        self.layout.addWidget(self.color_map_widget)

        # add reset button
        self.reset_button = QPushButton("Reset Transfer Function")
        self.reset_button.setFixedWidth(200)
        # align to center of the widget
        self.reset_button.clicked.connect(self.reset)

        self.layout.addWidget(self.reset_button, alignment=Qt.AlignCenter)

        self.styled_range_hslider = RangeSlider(self)
        self.layout.addWidget(self.styled_range_hslider)

    def reset(self):
        self.transfer_function_widget.points = []
        self.transfer_function_widget.add_point(0, self.widget_height)
        self.transfer_function_widget.add_point(self.widget_width, 0)
        self.transfer_function_widget.update()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.transfer_function_color_map = TransferFunctionWithColorMap(self)
        self.layout.addWidget(self.transfer_function_color_map)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
