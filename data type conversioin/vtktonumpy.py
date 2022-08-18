from vtk import *
from vtk.util.numpy_support import vtk_to_numpy

print("Loading data...")

# read structured grid
reader = vtkXMLImageDataReader()
reader.SetFileName("brain.vti")
reader.Update()

# convert to numpy
point_data = vtk_to_numpy(reader.GetOutput().GetPointData().GetScalars())
grid = vtk_to_numpy(reader.GetOutput())
print("Loaded data.")