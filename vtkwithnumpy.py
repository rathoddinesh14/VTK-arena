# An example from scipy cookbook demonstrating the use of numpy arrays in vtk

import numpy as np
# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOImage import vtkImageImport
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty
)
from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper
# noinspection PyUnresolvedReferences
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLRayCastImageDisplayHelper


def main():
    colors = vtkNamedColors()

    # We begin by creating the data we want to render.
    # For this tutorial, we create a 3D-image containing three overlaping cubes.
    # This data can of course easily be replaced by data from a medical CT-scan or anything else three dimensional.
    # The only limit is that the data must be reduced to unsigned 8 bit or 16 bit integers.
    data_matrix = np.zeros([75, 75, 75], dtype=np.uint8)
    data_matrix[0:35, 0:35, 0:35] = 50
    data_matrix[25:55, 25:55, 25:55] = 100
    data_matrix[45:74, 45:74, 45:74] = 150

    # For VTK to be able to use the data, it must be stored as a VTK-image.
    #  This can be done by the vtkImageImport-class which
    # imports raw data and stores it.
    dataImporter = vtkImageImport()
    # The previously created array is converted to a string of chars and imported.
    data_string = data_matrix.tobytes()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    # The type of the newly imported data is set to unsigned char (uint8)
    dataImporter.SetDataScalarTypeToUnsignedChar()
    # Because the data that is imported only contains an intensity value
    #  (it isnt RGB-coded or someting similar), the importer must be told this is the case.
    dataImporter.SetNumberOfScalarComponents(1)
    # The following two functions describe how the data is stored and the dimensions of the array it is stored in.
    #  For this simple case, all axes are of length 75 and begins with the first element.
    #  For other data, this is probably not the case.
    # I have to admit however, that I honestly dont know the difference between SetDataExtent()
    #  and SetWholeExtent() although VTK complains if not both are used.
    dataImporter.SetDataExtent(0, 74, 0, 74, 0, 74)
    dataImporter.SetWholeExtent(0, 74, 0, 74, 0, 74)

    # The following class is used to store transparency-values for later retrival.
    #  In our case, we want the value 0 to be
    # completely opaque whereas the three different cubes are given different transparency-values to show how it works.
    alphaChannelFunc = vtkPiecewiseFunction()
    alphaChannelFunc.AddPoint(0, 0.0)
    alphaChannelFunc.AddPoint(50, 0.05)
    alphaChannelFunc.AddPoint(100, 0.1)
    alphaChannelFunc.AddPoint(150, 0.2)

    # This class stores color data and can create color tables from a few color points.
    #  For this demo, we want the three cubes to be of the colors red green and blue.
    colorFunc = vtkColorTransferFunction()
    colorFunc.AddRGBPoint(50, 1.0, 0.0, 0.0)
    colorFunc.AddRGBPoint(100, 0.0, 1.0, 0.0)
    colorFunc.AddRGBPoint(150, 0.0, 0.0, 1.0)

    # The previous two classes stored properties.
    #  Because we want to apply these properties to the volume we want to render,
    # we have to store them in a class that stores volume properties.
    volumeProperty = vtkVolumeProperty()
    volumeProperty.SetColor(colorFunc)
    volumeProperty.SetScalarOpacity(alphaChannelFunc)

    volumeMapper = vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort())

    # The class vtkVolume is used to pair the previously declared volume as well as the properties
    #  to be used when rendering that volume.
    volume = vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    # With almost everything else ready, its time to initialize the renderer and window, as well as
    #  creating a method for exiting the application
    renderer = vtkRenderer()
    renderWin = vtkRenderWindow()
    renderWin.AddRenderer(renderer)
    renderInteractor = vtkRenderWindowInteractor()
    renderInteractor.SetRenderWindow(renderWin)

    # We add the volume to the renderer ...
    renderer.AddVolume(volume)
    renderer.SetBackground(colors.GetColor3d("MistyRose"))

    # set window size.
    renderWin.SetSize(900, 900)

    renderWin.SetWindowName('VTK With Numpy')

    # A simple function to be called when the user decides to quit the application.
    def exitCheck(obj, event):
        if obj.GetEventPending() != 0:
            obj.SetAbortRender(1)

    # Tell the application to use the function as an exit check.
    renderWin.AddObserver("AbortCheckEvent", exitCheck)

    renderInteractor.Initialize()
    # Because nothing will be rendered without any input, we order the first render manually
    #  before control is handed over to the main-loop.
    renderWin.Render()
    renderInteractor.Start()


if __name__ == '__main__':
    main()