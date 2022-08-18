#!/usr/bin/env python

'''
This example shows how to create an unstructured grid.
'''

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    VTK_LINE,
    VTK_POLYGON,
    VTK_QUAD,
    VTK_TETRA,
    VTK_TRIANGLE,
    VTK_TRIANGLE_STRIP,
    VTK_VERTEX,
    vtkUnstructuredGrid
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():
    colors = vtkNamedColors()

    x = [[0, 0, 0], [1, 0, 0], [2, 0, 0], [0, 1, 0], [1, 1, 0],
         [2, 1, 0], [0, 0, 1], [1, 0, 1], [2, 0, 1], [0, 1, 1],
         [1, 1, 1], [2, 1, 1], [0, 1, 2], [1, 1, 2], [2, 1, 2],
         [0, 1, 3], [1, 1, 3], [2, 1, 3], [0, 1, 4], [1, 1, 4],
         [2, 1, 4], [0, 1, 5], [1, 1, 5], [2, 1, 5], [0, 1, 6],
         [1, 1, 6], [2, 1, 6]]

    points = vtkPoints()
    for i in range(0, len(x)):
        points.InsertPoint(i, x[i])

    # print the number of points
    print("There are %d points." % points.GetNumberOfPoints())

    pts = [[0, 1, 4, 3, 6, 7, 10, 9],  # hexahedron
           [1, 2, 5, 4, 7, 8, 11, 10],  # hexahedron
           [6, 10, 9, 12, 0, 0, 0, 0],  # tetrahdron
           [8, 11, 10, 14, 0, 0, 0, 0],  # tetrahdron
           [16, 17, 14, 13, 12, 15, 0, 0],  # polygon
           [18, 15, 19, 16, 20, 17, 0, 0],  # triangle strip
           [22, 23, 20, 19, 0, 0, 0, 0],    # quad
           [21, 22, 18, 0, 0, 0, 0, 0],     # triangle
           [22, 19, 18, 0, 0, 0, 0, 0],     # triangle
           [23, 26, 0, 0, 0, 0, 0, 0],      # line
           [21, 24, 0, 0, 0, 0, 0, 0],      # line
           [25, 0, 0, 0, 0, 0, 0, 0]]       # vertex

    print(len(x), len(pts))
    ugrid = vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.Allocate(100)
    ugrid.InsertNextCell(VTK_HEXAHEDRON, 8, pts[0])
    ugrid.InsertNextCell(VTK_HEXAHEDRON, 8, pts[1])
    ugrid.InsertNextCell(VTK_TETRA, 4, pts[2][:4])
    ugrid.InsertNextCell(VTK_TETRA, 4, pts[3][:4])
    ugrid.InsertNextCell(VTK_POLYGON, 6, pts[4][:6])
    ugrid.InsertNextCell(VTK_TRIANGLE_STRIP, 6, pts[5][:6])
    ugrid.InsertNextCell(VTK_QUAD, 4, pts[6][:4])
    ugrid.InsertNextCell(VTK_TRIANGLE, 3, pts[7][:3])
    ugrid.InsertNextCell(VTK_TRIANGLE, 3, pts[8][:3])
    ugrid.InsertNextCell(VTK_LINE, 2, pts[9][:2])
    ugrid.InsertNextCell(VTK_LINE, 2, pts[10][:2])
    ugrid.InsertNextCell(VTK_VERTEX, 1, pts[11][:1])

    ugridMapper = vtkDataSetMapper()
    ugridMapper.SetInputData(ugrid)

    ugridActor = vtkActor()
    ugridActor.SetMapper(ugridMapper)
    ugridActor.GetProperty().SetColor(colors.GetColor3d('Peacock'))
    ugridActor.GetProperty().EdgeVisibilityOn()  # show edges

    renderer = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(renderer)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    renderer.AddActor(ugridActor)
    renderer.SetBackground(colors.GetColor3d('Beige'))

    renderer.ResetCamera()
    renderer.GetActiveCamera().Elevation(60.0)
    renderer.GetActiveCamera().Azimuth(30.0)
    renderer.GetActiveCamera().Dolly(1.0)

    renWin.SetSize(640, 480)
    renWin.SetWindowName('UGrid')

    # Interact with the data.
    renWin.Render()
    iren.Start()


if __name__ == '__main__':
    main()
