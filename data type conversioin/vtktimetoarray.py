import sys
import vtk

# read time varying data vtk file
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(sys.argv[1])
reader.Update()

print(reader.GetOutput())

point_data = reader.GetOutput().GetPointData()
# number of components
num_components = point_data.GetNumberOfComponents()

print(num_components)

for i in range(num_components):
    array = point_data.GetArray(i)
    # array_name = point_data.GetArrayName(i)
    # print(array_name)
    print(array)

    # save as vti file
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName(sys.argv[2] + str(i) + ".vti")

    # get the dimensions of the point data
    dims = reader.GetOutput().GetDimensions()
    print(dims)

    # convert array to vtkTable
    # table = vtk.vtkTable()
    # table.AddColumn(array)
    # table to vtkImageData

    image = vtk.vtkImageData()
    image.SetDimensions(dims)
    # image.SetDimensions(array.GetNumberOfTuples(), 1, 1)
    image.GetPointData().AddArray(array)
    # set table to image
    writer.SetInputData(image)
    writer.Write()