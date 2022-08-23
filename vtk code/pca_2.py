import vtk

points = vtk.vtkPoints()
points.SetNumberOfPoints(200)
cellArray = vtk.vtkCellArray()
boxMueller = vtk.vtkBoxMuellerRandomSequence()

centre = [0.0, 0.0, 0.0]

for i in range(200):
    # random point in x in [0, 3], y in [0, 5], z in [0, 2]
    # scaled value
    x = boxMueller.GetScaledValue(0, 3)
    boxMueller.Next()
    y = boxMueller.GetScaledValue(0, 5)
    boxMueller.Next()
    z = boxMueller.GetScaledValue(0, 2)
    boxMueller.Next()
    points.SetPoint(i, x, y, z)
    cellArray.InsertNextCell(1)
    cellArray.InsertCellPoint(i)
    print(x, y, z)
    centre[0] += x
    centre[1] += y
    centre[2] += z

centre[0] /= 200
centre[1] /= 200
centre[2] /= 200

# Create a polydata object
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetVerts(cellArray)

# vtk double array
xArr = vtk.vtkDoubleArray()
xArr.SetName("x")
xArr.SetNumberOfComponents(1)

yArr = vtk.vtkDoubleArray()
yArr.SetName("y")
yArr.SetNumberOfComponents(1)

zArr = vtk.vtkDoubleArray()
zArr.SetName("z")
zArr.SetNumberOfComponents(1)

for i in range(200):
    xArr.InsertNextValue(polydata.GetPoint(i)[0])
    yArr.InsertNextValue(polydata.GetPoint(i)[1])
    zArr.InsertNextValue(polydata.GetPoint(i)[2])

# vtk table
table = vtk.vtkTable()
table.AddColumn(xArr)
table.AddColumn(yArr)
table.AddColumn(zArr)

# vtk pca
pca = vtk.vtkPCAStatistics()
pca.SetInputData(table)
pca.SetColumnStatus("x", 1)
pca.SetColumnStatus("y", 1)
pca.SetColumnStatus("z", 1)
pca.RequestSelectedColumns()
pca.SetDeriveOption(True)
pca.Update()

# eigenvalues
eigenvalues = vtk.vtkDoubleArray()
pca.GetEigenvalues(eigenvalues)
print("Eigenvalues: ")
for i in range(eigenvalues.GetNumberOfTuples()):
    print(eigenvalues.GetValue(i))

# eigenvectors
eigenvectors = vtk.vtkDoubleArray()
pca.GetEigenvectors(eigenvectors)
# print("Eigenvectors: ")
# for i in range(eigenvectors.GetNumberOfTuples()):
#     print(eigenvectors.GetValue(i))

eig_vec = [vtk.vtkDoubleArray() for i in range(eigenvectors.GetNumberOfTuples())]
for i in range(eigenvectors.GetNumberOfTuples()):
    pca.GetEigenvector(i, eig_vec[i])

print("Eigenvectors: ")
for i in range(eigenvectors.GetNumberOfTuples()):
    print(eig_vec[i].GetValue(0), eig_vec[i].GetValue(1), eig_vec[i].GetValue(2))

# end points of eigenvectors
ev_1_end_1 = [0.0, 0.0, 0.0]
ev_1_end_2 = [0.0, 0.0, 0.0]
# calculate end points of eigenvectors
for i in range(0, 3):
    ev_1_end_1[i] = centre[i] + eig_vec[0].GetValue(i) * eigenvalues.GetValue(0) / 2
    ev_1_end_2[i] = centre[i] - eig_vec[0].GetValue(i) * eigenvalues.GetValue(0) / 2

ev_2_end_1 = [0.0, 0.0, 0.0]
ev_2_end_2 = [0.0, 0.0, 0.0]
for i in range(0, 3):
    ev_2_end_1[i] = centre[i] + eig_vec[1].GetValue(i) * eigenvalues.GetValue(1) / 2
    ev_2_end_2[i] = centre[i] - eig_vec[1].GetValue(i) * eigenvalues.GetValue(1) / 2

ev_3_end_1 = [0.0, 0.0, 0.0]
ev_3_end_2 = [0.0, 0.0, 0.0]
for i in range(0, 3):
    ev_3_end_1[i] = centre[i] + eig_vec[2].GetValue(i) * eigenvalues.GetValue(2) / 2
    ev_3_end_2[i] = centre[i] - eig_vec[2].GetValue(i) * eigenvalues.GetValue(2) / 2

print("End points of eigenvector 1: ")
print(ev_1_end_1[0], ev_1_end_1[1], ev_1_end_1[2])
print(ev_1_end_2[0], ev_1_end_2[1], ev_1_end_2[2])

# line source
lineSource = vtk.vtkLineSource()
lineSource.SetPoint1(ev_1_end_1)
lineSource.SetPoint2(ev_1_end_2)

# mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(lineSource.GetOutputPort())

# actor
lactor = vtk.vtkActor()
lactor.SetMapper(mapper)
lactor.GetProperty().SetColor(1.0, 0.0, 0.0)

# line source 2
lineSource2 = vtk.vtkLineSource()
lineSource2.SetPoint1(ev_2_end_1)
lineSource2.SetPoint2(ev_2_end_2)

# mapper 2
mapper2 = vtk.vtkPolyDataMapper()
mapper2.SetInputConnection(lineSource2.GetOutputPort())

# actor 2
lactor2 = vtk.vtkActor()
lactor2.SetMapper(mapper2)
lactor2.GetProperty().SetColor(0.0, 1.0, 0.0)

# line source 3
lineSource3 = vtk.vtkLineSource()
lineSource3.SetPoint1(ev_3_end_1)
lineSource3.SetPoint2(ev_3_end_2)

# mapper 3
mapper3 = vtk.vtkPolyDataMapper()
mapper3.SetInputConnection(lineSource3.GetOutputPort())

# actor 3
lactor3 = vtk.vtkActor()
lactor3.SetMapper(mapper3)
lactor3.GetProperty().SetColor(0.0, 0.0, 1.0)


# sphere at centre
sphere = vtk.vtkSphereSource()
sphere.SetCenter(centre)
sphere.SetRadius(1)
sphere.SetThetaResolution(20)
sphere.SetPhiResolution(20)

# mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# actor
sactor = vtk.vtkActor()
sactor.SetMapper(mapper)
sactor.GetProperty().SetColor(1, 0, 0)

# Create a mapper and actor
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Create a renderer, render window, and interactor
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Add the actor to the scene
renderer.AddActor(actor)
renderer.AddActor(sactor)
renderer.AddActor(lactor)
renderer.AddActor(lactor2)
renderer.AddActor(lactor3)
renderer.SetBackground(0.1, 0.2, 0.3) # Background color white

# Render and interact
renderWindow.Render()
renderWindowInteractor.Start()
