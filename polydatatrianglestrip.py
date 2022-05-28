# single triangle strip

import vtk
import numpy as np
import math



def main():
    # triangle strip
    points = vtk.vtkPoints()
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(0, 1, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(1, 1, 0)
    points.InsertNextPoint(2, 0, 0)
    points.InsertNextPoint(2, 1, 0)
    points.InsertNextPoint(3, 0, 0)
    points.InsertNextPoint(3, 1, 0)

    strips = vtk.vtkCellArray()
    numCells = 8
    strips.InsertNextCell(numCells)
    for i in range(numCells):
        strips.InsertCellPoint(i)

    triangleStrip = vtk.vtkPolyData()
    triangleStrip.SetPoints(points)
    triangleStrip.SetStrips(strips)

    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(triangleStrip)

    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # render
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0, 0, 0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(640, 480)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    renderWindow.Render()
    interactor.Start()

main()