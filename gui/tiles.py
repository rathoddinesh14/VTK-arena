# import pyside6 QtCore QtGui QtWidgets
from PySide6 import QtCore, QtGui, QtWidgets


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # column
    num_cols = 4

    # grid layout
    grid = QtWidgets.QGridLayout()

    # App banner label
    banner = QtWidgets.QLabel("App Banner")
    banner.setAlignment(QtCore.Qt.AlignCenter)
    banner.setStyleSheet("background-color: #000; color: #fff")
    banner.setFixedHeight(50)
    # span across all columns

    # App content label
    content = QtWidgets.QLabel("App Content")
    content.setAlignment(QtCore.Qt.AlignCenter)
    content.setStyleSheet("background-color: #fff; color: #000")
    content.setFixedHeight(300)

    # App footer label
    footer = QtWidgets.QLabel("App Footer")
    footer.setAlignment(QtCore.Qt.AlignCenter)
    footer.setStyleSheet("background-color: #000; color: #fff")
    footer.setFixedHeight(50)

    # Add widgets to grid layout
    grid.addWidget(banner, 0, 0, 1, num_cols)
    grid.addWidget(content, 1, 0, 1, num_cols)
    grid.addWidget(footer, 2, 0, 1, num_cols)

    # add buttons
    for i in range(num_cols):
        button = QtWidgets.QPushButton("Button " + str(i))
        button.setStyleSheet("background-color: #fff; color: #000")
        grid.addWidget(button, 3, i)
    
    # set layout
    widget = QtWidgets.QWidget()
    widget.setLayout(grid)

    # show widget
    widget.show()

    # close app
    sys.exit(app.exec_())