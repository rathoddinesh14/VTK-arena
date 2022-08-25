import vtk
import random

def get_eigen_axis_actor(center, eigen_value, eigen_vector, color):
    """
    Get the eigen axis passing through the center
    @param center: center
    @param eigen_value: eigen value of the eigen vector
    @param eigen_vector: eigen vector (x, y, z)
    @param color: color of the eigen axis
    """
    axis = vtk.vtkLineSource()
    axis.SetPoint1([    center[0] + eigen_value * eigen_vector[0], 
                        center[1] + eigen_value * eigen_vector[1],
                        center[2] + eigen_value * eigen_vector[2]])
    axis.SetPoint2([    center[0] - eigen_value * eigen_vector[0],
                        center[1] - eigen_value * eigen_vector[1],
                        center[2] - eigen_value * eigen_vector[2]])
    axis.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(axis.GetOutputPort())
    mapper.Update()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)

    return actor


def get_eigen_vectors_values(points):
    '''
    returns eigen values, vector
    @param points: list of points (x, y, z)
    @return: eigen values, vector
    '''
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

    for i in range(points.GetNumberOfPoints()):
        xArr.InsertNextValue(points.GetPoint(i)[0])
        yArr.InsertNextValue(points.GetPoint(i)[1])
        zArr.InsertNextValue(points.GetPoint(i)[2])

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
    ev = []
    # print("Eigenvalues: ")
    for i in range(eigenvalues.GetNumberOfTuples()):
        # print(eigenvalues.GetValue(i))
        ev.append(eigenvalues.GetValue(i))

    # eigenvectors
    eigenvectors = vtk.vtkDoubleArray()
    pca.GetEigenvectors(eigenvectors)

    eig_vec = [vtk.vtkDoubleArray() for i in range(eigenvectors.GetNumberOfTuples())]
    for i in range(eigenvectors.GetNumberOfTuples()):
        pca.GetEigenvector(i, eig_vec[i])

    eig_vec_2 = []
    for i in range(len(eig_vec)):
        eig_vec_2.append((eig_vec[i].GetValue(0), eig_vec[i].GetValue(1), eig_vec[i].GetValue(2)))

    return eig_vec_2, ev


points = vtk.vtkPoints()
points.SetNumberOfPoints(200)
cellArray = vtk.vtkCellArray()
boxMueller = vtk.vtkBoxMuellerRandomSequence()

centre = [0.0, 0.0, 0.0]

# populate points
for i in range(points.GetNumberOfPoints()):
    # random point in x in [0, 3], y in [0, 5], z in [0, 2]
    # scaled value
    # x = boxMueller.GetScaledValue(0, 3)
    # boxMueller.Next()
    # y = boxMueller.GetScaledValue(0, 5)
    # boxMueller.Next()
    # z = boxMueller.GetScaledValue(0, 2)
    # boxMueller.Next()
    # sample from sphere
    x = random.random() * 4
    y = random.random() * 5
    z = random.random() * 2
    points.SetPoint(i, x, y, z)
    cellArray.InsertNextCell(1)
    cellArray.InsertCellPoint(i)
    # print(x, y, z)
    centre[0] += x
    centre[1] += y
    centre[2] += z

centre[0] /= points.GetNumberOfPoints()
centre[1] /= points.GetNumberOfPoints()
centre[2] /= points.GetNumberOfPoints()

# Create a polydata object
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetVerts(cellArray)

eigenvectors, eigenvalues = get_eigen_vectors_values(points)

print(eigenvectors)
print(eigenvalues)

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
# renderer.AddActor(sactor)
renderer.AddActor(get_eigen_axis_actor(centre, eigenvalues[0], eigenvectors[0], (1, 0, 0)))
renderer.AddActor(get_eigen_axis_actor(centre, eigenvalues[1], eigenvectors[1], (0, 1, 0)))
renderer.AddActor(get_eigen_axis_actor(centre, eigenvalues[2], eigenvectors[2], (0, 0, 1)))
renderer.SetBackground(0.1, 0.2, 0.3) # Background color white

# Render and interact
renderWindow.Render()
renderWindowInteractor.Start()
