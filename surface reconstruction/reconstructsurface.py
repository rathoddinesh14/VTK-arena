import pyvista as pv
import vtk
import numpy as np
import math

# read the vtp file
# reader = vtk.vtkXMLPolyDataReader()
# reader.SetFileName("/Users/rathod_ias/Documents/GitHub/compositum-3d-visualization/grain_boundary.vtp")
# reader.Update()

# # # get the points
# points = reader.GetOutput().GetPoints()

# convert the points to numpy array
# points_array = np.zeros((points.GetNumberOfPoints(), 3))
# for i in range(0, points.GetNumberOfPoints()):
#     points_array[i, :] = points.GetPoint(i)

# points = pv.wrap(pv.Sphere().points)


points_array = np.zeros((129600, 3))
# sphere surface
for theta in range(0, 360):
    for phi in range(0, 360):
        x = 1.0 * math.sin(math.radians(theta)) * math.cos(math.radians(phi))
        y = 1.0 * math.sin(math.radians(theta)) * math.sin(math.radians(phi))
        z = 1.0 * math.cos(math.radians(theta))
        i = theta * 360 + phi
        points_array[i, :] = x, y, z

points = pv.wrap(points_array)
surf = points.reconstruct_surface()
print(surf)

pl = pv.Plotter(shape=(1, 2))
pl.add_mesh(points)
pl.add_title('Point Cloud of 3D Surface')
pl.subplot(0, 1)
pl.add_mesh(surf, color=True, show_edges=True)
pl.add_title('Reconstructed Surface')
pl.show()