from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QComboBox, QVBoxLayout, QWidget
import os
import xml.etree.ElementTree as ET
import vtk

class ColormapChooserWidget(QWidget):
    def __init__(self, colormaps, width, parent=None):
        super().__init__()
        self.parent = parent

        self.colormaps = colormaps
        self.color_width = width
        # Create the UI components
        self.colormap_label = QLabel()
        self.colormap_label.setFixedSize(self.color_width, 50)
        self.colormap_dropdown = QComboBox()
        for cmap in colormaps:
            self.colormap_dropdown.addItem(cmap.name)
        self.colormap_dropdown.currentIndexChanged.connect(self.on_colormap_changed)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.colormap_label)
        layout.addWidget(self.colormap_dropdown)
        self.setLayout(layout)

        # Set the default colormap
        self.set_colormap(0)

    def set_colormap(self, cmap_index):
        # Load the colormap preview image
        cmap = self.colormaps[cmap_index]
        pixmap = QPixmap(cmap.preview_loc)
        # resize the image to fit the label size and change the aspect ratio
        pixmap = pixmap.scaled(self.colormap_label.size())
        self.colormap_label.setPixmap(pixmap)

    def on_colormap_changed(self, index):
        self.set_colormap(index)
        self.parent.update_cmap(self.get_colormap())

    def get_colormap(self):
        tree = ET.parse(self.colormaps[self.colormap_dropdown.currentIndex()].file_loc)
        root = tree.getroot()

        # <ColorMaps>
            # <ColorMap space="Lab" indexedLookup="false" group="Interlinked" name="Yellow Orange 5 / Brown 9 / Blue 8">
                # <Point x="0" o="1" r="0.301961" g="0.047059" b="0.090196"/>
        
        root = root.find("ColorMap")

        ctf = vtk.vtkColorTransferFunction()
        ctf.SetColorSpaceToDiverging()

        # Get the points
        points = []
        for point in root.findall("Point"):
            # points.append((float(point.attrib["x"]), 
            #                float(point.attrib["r"]), 
            #                float(point.attrib["g"]), 
            #                float(point.attrib["b"])))
        
            ctf.AddRGBPoint(float(point.attrib["x"]), 
                            float(point.attrib["r"]), 
                            float(point.attrib["g"]), 
                            float(point.attrib["b"]))
        
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(self.color_width)
        lut.Build()

        for i in range(self.color_width):
            rgb = list(ctf.GetColor(float(i)/self.color_width)) + [1]
            lut.SetTableValue(i, rgb)

        return lut

class ColorMap():
    def __init__(self, name, file_loc, preview_loc):
        self.name = name
        self.file_loc = file_loc
        self.preview_loc = preview_loc

if __name__ == "__main__":
    # /home/dinesh/Downloads/keycolormaps/KeyColormaps
    base_loc = "/home/dinesh/Downloads/keycolormaps/KeyColormaps"
    colormaps = []
    for i in os.listdir(base_loc):
        if i.endswith(".png"):
            filename = i.split(".")[0]
            colormaps.append(ColorMap(filename, 
                                      os.path.join(base_loc, filename + ".xml"), 
                                      os.path.join(base_loc, i)))

    app = QApplication([])
    widget = ColormapChooserWidget(colormaps)
    widget.show()
    app.exec()
