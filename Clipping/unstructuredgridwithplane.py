#!/usr/bin/env python

import collections

import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import (
    vtkCellTypes,
    vtkPlane
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTableBasedClipDataSet
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def get_program_parameters():
    import argparse
    description = 'Use a vtkTableBasedClipDataSet to clip vtkUnstructuredGrid.'
    epilogue = '''
 Use a vtkTableBasedClipDataSet to clip a vtkUnstructuredGrid.
 The resulting output and clipped output are presented in yellow and red
 respectively. To illustrate the clipped interfaces, the example uses a
 vtkTransform to rotate each output about their centers.
 Note: This clipping filter does retain the original cells if they are not
  clipped.

   '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue, 
                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='treemesh.vtk')
    args = parser.parse_args()
    return args.filename


def main():
    filename = get_program_parameters()

    # Create the reader for the data.
    reader = vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()

    bounds = reader.GetOutput().GetBounds()
    print('Bounds:', bounds)
    center = reader.GetOutput().GetCenter()
    print('Center:', center)

    colors = vtkNamedColors()
    renderer = vtkRenderer()
    renderer.SetBackground(colors.GetColor3d('Wheat'))
    renderer.UseHiddenLineRemovalOn()

    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 800)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    xnorm = [-1.0, -1.0, 1.0]

    clipPlane = vtkPlane()
    clipPlane.SetOrigin(reader.GetOutput().GetCenter())
    clipPlane.SetNormal(xnorm)

    clipper = vtkTableBasedClipDataSet()
    clipper.SetClipFunction(clipPlane)
    clipper.SetInputData(reader.GetOutput())
    clipper.SetValue(0.0)  # try clipping with a value
    clipper.GenerateClippedOutputOn()  # try commenting this line out
    clipper.Update()  # this trigger the action of clipping in the pipeline

    insideMapper = vtkDataSetMapper()
    insideMapper.SetInputData(clipper.GetOutput())
    insideMapper.ScalarVisibilityOff()

    insideActor = vtkActor()
    insideActor.SetMapper(insideMapper)
    insideActor.GetProperty().SetDiffuseColor(colors.GetColor3d('banana'))
    insideActor.GetProperty().SetAmbient(.3)
    insideActor.GetProperty().EdgeVisibilityOn()

    clippedMapper = vtkDataSetMapper()
    clippedMapper.SetInputData(clipper.GetClippedOutput())
    clippedMapper.ScalarVisibilityOff()

    clippedActor = vtkActor()
    clippedActor.SetMapper(clippedMapper)
    clippedActor.GetProperty().SetDiffuseColor(colors.GetColor3d('tomato'))
    clippedActor.GetProperty().SetAmbient(.3)
    clippedActor.GetProperty().EdgeVisibilityOn()

    # Create transforms to make a better visualization
    insideTransform = vtkTransform()
    insideTransform.Translate(-(bounds[1] - bounds[0]) * 0.75, 0, 0)
    insideTransform.Translate(center[0], center[1], center[2])
    insideTransform.RotateY(-120.0)
    insideTransform.Translate(-center[0], -center[1], -center[2])
    insideActor.SetUserTransform(insideTransform)

    clippedTransform = vtkTransform()
    clippedTransform.Translate((bounds[1] - bounds[0]) * 0.75, 0, 0)
    clippedTransform.Translate(center[0], center[1], center[2])
    clippedTransform.RotateY(60.0)
    clippedTransform.Translate(-center[0], -center[1], -center[2])
    clippedActor.SetUserTransform(clippedTransform)

    renderer.AddViewProp(clippedActor)
    renderer.AddViewProp(insideActor)

    renderer.ResetCamera()
    renderer.GetActiveCamera().Dolly(0.4)
    renderer.ResetCameraClippingRange()
    renderWindow.Render()
    renderWindow.SetWindowName('Clipping Unstructured Grid With Plane')
    renderWindow.Render()

    interactor.Start()

    # Generate a report
    numberOfCells = clipper.GetOutput().GetNumberOfCells()
    print('------------------------')
    print('The inside dataset contains a \n', clipper.GetOutput(
    ).GetClassName(), ' that has ', numberOfCells, ' cells')
    cellMap = dict()
    for i in range(0, numberOfCells):
        cellMap.setdefault(clipper.GetOutput().GetCellType(i), 0)
        cellMap[clipper.GetOutput().GetCellType(i)] += 1
    # Sort by key and put into an OrderedDict.
    # An OrderedDict remembers the order in which the keys have been inserted.
    for k, v in collections.OrderedDict(sorted(cellMap.items())).items():
        print('\tCell type ', vtkCellTypes.GetClassNameFromTypeId(
            k), ' occurs ', v, ' times.')

    numberOfCells = clipper.GetClippedOutput().GetNumberOfCells()
    print('------------------------')
    print('The clipped dataset contains a \n', clipper.GetClippedOutput()
    .GetClassName(), ' that has ', numberOfCells, ' cells')
    outsideCellMap = dict()
    for i in range(0, numberOfCells):
        outsideCellMap.setdefault(clipper.GetClippedOutput().GetCellType(i), 0)
        outsideCellMap[clipper.GetClippedOutput().GetCellType(i)] += 1
    for k, v in collections.OrderedDict(sorted(outsideCellMap.items())).items():
        print('\tCell type ', vtkCellTypes.GetClassNameFromTypeId(
            k), ' occurs ', v, ' times.')


if __name__ == '__main__':
    main()
