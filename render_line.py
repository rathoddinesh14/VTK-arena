import vtk


# generate random adjacency matrix list
adjacency_list = []


print(adjacency_list)

# 2 points
p1 = [0.0, 0.0, 0.0]
p2 = [1.0, 1.0, 1.0]

# points
points = vtk.vtkPoints()
points.InsertNextPoint(p1)
points.InsertNextPoint(p2)

# 1 lines
line = vtk.vtkLine()
line.GetPointIds().SetId(0, 0)
line.GetPointIds().SetId(1, 1)

# cells
lines = vtk.vtkCellArray()
lines.InsertNextCell(line)

# polydata
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetLines(lines)

# tube filter
tube = vtk.vtkTubeFilter()
tube.SetInputData(polydata)
tube.SetRadius(0.1)
tube.SetNumberOfSides(50)
tube.Update()

# mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(tube.GetOutput())

# actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

# render window
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

# interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# render and interact
renderWindow.Render()
renderWindowInteractor.Start()
