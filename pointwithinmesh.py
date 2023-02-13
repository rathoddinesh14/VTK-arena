import vtk

# Create a vtkPoints object to store the vertices of the tetrahedron
points = vtk.vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 1)

cells = vtk.vtkCellArray()
for i in range(4):
    triangle = vtk.vtkTriangle()
    triangle.GetPointIds().SetId(0, i)
    triangle.GetPointIds().SetId(1, (i + 1) % 4)
    triangle.GetPointIds().SetId(2, (i + 2) % 4)
    cells.InsertNextCell(triangle)

# polydata
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetPolys(cells)

write = vtk.vtkXMLPolyDataWriter()
write.SetFileName("tetrahedron.vtp")
write.SetInputData(polydata)
write.Write()

# test points
testPoints = vtk.vtkPoints()
testPoints.InsertNextPoint(1.5, 0.25, 0.23)

# test points polydata
testPolyData = vtk.vtkPolyData()
testPolyData.SetPoints(testPoints)

# enclosed points filter
enclosedPoints = vtk.vtkSelectEnclosedPoints()
enclosedPoints.SetInputData(testPolyData)
enclosedPoints.SetSurfaceData(polydata)
enclosedPoints.Update()

# check if the point is inside the tetrahedron
print(enclosedPoints.IsInside(0))
