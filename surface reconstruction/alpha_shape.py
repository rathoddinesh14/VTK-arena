from descartes import PolygonPatch
import matplotlib.pyplot as plt
import alphashape
import numpy as np
# delaunay from scipy
from scipy.spatial import Delaunay

# points_2d = [(0., 0.), (0., 1.), (1., 1.), (1., 0.),
#           (0.5, 0.25), (0.5, 0.75), (0.25, 0.5), (0.75, 0.5)]

# fig, ax = plt.subplots()
# ax.scatter(*zip(*points_2d))
# plt.show()

# alpha_shape = alphashape.alphashape(points_2d, 2.)
# alpha_shape = alphashape.alphashape(
#     points_2d,
#     lambda ind, r: 1.0 + any(np.array(points_2d)[ind][:,0] == 0.0))

# alpha_shape = alphashape.alphashape(points_2d)

# print(alpha_shape)

# fig, ax = plt.subplots()
# ax.scatter(*zip(*points_2d))
# ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
# plt.show()

# =============================================================================

# points_3d = [
#     (0., 0., 0.), (0., 0., 1.), (0., 1., 0.),
#     (1., 0., 0.), (1., 1., 0.), (1., 0., 1.),
#     (0., 1., 1.), (1., 1., 1.), (.25, .5, .5),
#     (.5, .25, .5), (.5, .5, .25), (.75, .5, .5),
#     (.5, .75, .5), (.5, .5, .75)
# ]

import vtk

# read the vtp file
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName("grain_376.vtp")
reader.Update()

# # get the points
points = reader.GetOutput().GetPoints()

# convert the points to numpy array
points_3d = np.zeros((points.GetNumberOfPoints(), 3))
for i in range(0, points.GetNumberOfPoints()):
    points_3d[i, :] = points.GetPoint(i)

print("shape of points_3d: ", points_3d.shape)

import logging
logger = logging.getLogger()
logger.disabled = True

alpha_shape = alphashape.alphashape(points_3d, 1.0)

print("After performing alpha shape : ", alpha_shape)
alpha_shape.export("alpha_shape_singlegrain.stl")

import trimesh

trimesh.smoothing.filter_humphrey(alpha_shape, beta=0.1)
print("After performing filer humphrey smoothing : ", alpha_shape)
alpha_shape.export("alpha_shape_singlegrain_fh.stl")

trimesh.repair.fill_holes(alpha_shape)
print("After performing fill holes : ", alpha_shape)
trimesh.repair.fill_holes(alpha_shape)
print("Fill holes : ", alpha_shape.fill_holes())
alpha_shape.export("alpha_shape_singlegrain_fillholes.stl")

# convert trimesh to vtk polydata
Ugrid = vtk.vtkPolyData()
Ugrid.SetPoints(vtk.vtkPoints())
Ugrid.SetPolys(vtk.vtkCellArray())

for i in range(0, len(alpha_shape.vertices)):
    # print("i: ", alpha_shape.vertices[i])
    Ugrid.GetPoints().InsertNextPoint(alpha_shape.vertices[i])
    Ugrid.GetPolys().InsertNextCell(1)
    Ugrid.GetPolys().InsertCellPoint(i)

for i in range(0, len(alpha_shape.faces)):
    Ugrid.GetPolys().InsertNextCell(3)
    Ugrid.GetPolys().InsertCellPoint(alpha_shape.faces[i][0])
    Ugrid.GetPolys().InsertCellPoint(alpha_shape.faces[i][1])
    Ugrid.GetPolys().InsertCellPoint(alpha_shape.faces[i][2])

curr_cp = 376
color = [0, 0, 0]
color_scalar = vtk.vtkUnsignedCharArray()
color_scalar.SetNumberOfComponents(3)
color_scalar.SetName("Color")
for i in range(Ugrid.GetNumberOfPoints()):
    color_scalar.InsertNextTuple3(color[0], color[1], color[2])

Ugrid.GetPointData().SetScalars(color_scalar)

# add a unique id to each point
id_scalar = vtk.vtkIdTypeArray()
id_scalar.SetNumberOfComponents(1)
id_scalar.SetName("CP ID")
for i in range(Ugrid.GetNumberOfPoints()):
    id_scalar.InsertNextTuple1(curr_cp)

Ugrid.GetPointData().AddArray(id_scalar)

# add a unique id to each cell
id_scalar = vtk.vtkIdTypeArray()
id_scalar.SetNumberOfComponents(1)
id_scalar.SetName("CP ID")
for i in range(Ugrid.GetNumberOfCells()):
    id_scalar.InsertNextTuple1(curr_cp)

Ugrid.GetCellData().AddArray(id_scalar)

Ugrid.Modified()

# write the vtk file
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName("alpha_shape_singlegrain.vtp")
writer.SetInputData(Ugrid)
writer.Write()


# # plot 3d points
# fig, ax = plt.subplots()
# ax = plt.axes(projection='3d')
# ax.scatter(*zip(*points_3d))
# # plot alpha_shape.vertices as points and alpha_shape.faces as triangles
# ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces)
# # ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
# plt.show()