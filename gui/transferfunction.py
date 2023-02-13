import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPainter, QBrush, QPen, QPolygonF, QPainterPath
from PySide6.QtCore import Qt, QPoint

class TransferFunctionWidget(QWidget):
    def __init__(self, parent=None):
        super(TransferFunctionWidget, self).__init__(parent)
        self.setFixedSize(500, 500)
        self.points = []
        self.selected_point = None

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

        painter.fillPath(path, QBrush(Qt.gray))



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

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.transfer_function_widget = TransferFunctionWidget(self)

        self.transfer_function_widget.add_point(0, 500)
        self.transfer_function_widget.add_point(500, 0)

        self.layout.addWidget(self.transfer_function_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
