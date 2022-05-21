#!/usr/bin/env python

# convert read vti file

import vtk
import sys

reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(sys.argv[1])
reader.Update()
image = reader.GetOutput()

# check the data type
if image.GetScalarType() != vtk.VTK_UNSIGNED_CHAR:
    print("Error: VTK image data type is not unsigned char")
    print(image)
    # get array "Decompressed"
    array = image.GetPointData().GetArray("Decompressed")
    print(array)

    # convert array to unsigned char
    newArray = vtk.vtkUnsignedCharArray()
    newArray.SetNumberOfComponents(array.GetNumberOfComponents())
    newArray.SetNumberOfTuples(array.GetNumberOfTuples())
    for i in range(array.GetNumberOfTuples()):
        newArray.SetTuple(i, array.GetTuple(i))
    
    # set array to image
    image.GetPointData().SetScalars(newArray)


    # cast = vtk.vtkImageCast()
    # cast.SetInputData(image)
    # cast.SetOutputScalarTypeToUnsignedChar()
    # cast.ClampOverflowOn()
    # cast.Update()
    # image = cast.GetOutput()

# writer = vtk.vtkJPEGWriter()
writer = vtk.vtkPNGWriter()
writer.SetFileName(sys.argv[2])
writer.SetInputData(image)
writer.Write()