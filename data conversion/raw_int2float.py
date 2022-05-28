import vtk
import sys

# reading the raw file
reader = vtk.vtkStructuredPointsReader()
filename = sys.argv[1]
reader.SetFileName(filename)
reader.Update()

# print the metadata of the raw file
ugrid = reader.GetOutput()
print("Number of points:", ugrid.GetNumberOfPoints())
print("Number of cells:", ugrid.GetNumberOfCells())
