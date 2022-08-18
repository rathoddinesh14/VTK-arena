#!/usr/bin/env python

import vtk


if __name__=='__main__':

    # write a structured grid to vtk file

    # create a structured grid
    sg = vtk.vtkStructuredGrid()

    # 3x3 grid with same scalar value on each cell
    sg.SetDimensions(3,3,1)
    sg.SetPoints(vtk.vtkPoints())
    sg.GetPoints().SetNumberOfPoints(9)
    sg.GetPointData().SetScalars(vtk.vtkDoubleArray())
    sg.GetPointData().GetScalars().SetNumberOfTuples(9)
    sg.GetPointData().GetScalars().SetName("scalars")
    sg.GetPointData().GetScalars().FillComponent(0,1.0)

    # write the structured grid to a vtk file
    writer = vtk.vtkStructuredGridWriter()
    writer.SetFileName("structured_grid.vtk")
    writer.SetInputData(sg)
    writer.Write()


    print("Testing structured grid")