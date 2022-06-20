from descartes import PolygonPatch
import matplotlib.pyplot as plt
import alphashape
import numpy as np

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
reader.SetFileName("/Users/rathod_ias/Documents/GitHub/compositum-3d-visualization/singlegrain.vtp")
reader.Update()

# # get the points
points = reader.GetOutput().GetPoints()

# convert the points to numpy array
points_3d = np.zeros((points.GetNumberOfPoints(), 3))
for i in range(0, points.GetNumberOfPoints()):
    points_3d[i, :] = points.GetPoint(i)

alpha_shape = alphashape.alphashape(points_3d, 1.0)

print("After performing alpha shape : ", alpha_shape)
alpha_shape.export("singlegrain.stl")

import trimesh

trimesh.smoothing.filter_humphrey(alpha_shape, beta=0.1)
print("After performing filer humphrey smoothing : ", alpha_shape)
alpha_shape.export("singlegrain_fh.stl")

trimesh.repair.fill_holes(alpha_shape)
print("After performing fill holes : ", alpha_shape)
trimesh.repair.fill_holes(alpha_shape)
print("Fill holes : ", alpha_shape.fill_holes())
alpha_shape.export("singlegrain_fillholes.stl")

# plot 3d points
fig, ax = plt.subplots()
ax = plt.axes(projection='3d')
ax.scatter(*zip(*points_3d))
# plot alpha_shape.vertices as points and alpha_shape.faces as triangles
ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces)
# ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
plt.show()