#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkIOLegacy import vtkDataSetReader
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOGeometry import (
    vtkBYUReader,
    vtkOBJReader,
    vtkSTLReader
)
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():
    pd_fn = get_program_parameters()

    colors = vtkNamedColors()

    polyData = ReadPolyData(pd_fn)
    mapper = vtkPolyDataMapper()
    mapper.SetInputData(polyData)

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetDiffuseColor(colors.GetColor3d('Crimson'))
    actor.GetProperty().SetSpecular(.6)
    actor.GetProperty().SetSpecularPower(30)

    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(900, 900)
    renderWindow.SetWindowName('Save Scene To Field Data')

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('Silver'))

    # Interact to change camera.
    renderWindow.Render()
    renderWindowInteractor.Start()

    # After the interaction is done, save the scene.
    SaveSceneToFieldData(polyData, actor, renderer.GetActiveCamera())
    renderWindowInteractor.Initialize()
    renderWindow.Render()
    renderWindowInteractor.Start()

    # # After interaction , restore the scene.
    RestoreSceneFromFieldData(polyData, actor, renderer.GetActiveCamera())
    renderWindowInteractor.Initialize()
    renderWindow.Render()
    renderWindowInteractor.Start()


def get_program_parameters():
    import argparse
    description = 'Saving a scene to field data.'
    epilogue = '''
    '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('data_file', help='A polydata file e.g. Armadillo.ply.')
    args = parser.parse_args()
    return args.data_file


def ReadPolyData(file_name):
    '''
    this function reads the input file and returns the polydata
    @param file_name: the name of the file to read
    @return: the polydata
    '''
    import os
    path, extension = os.path.splitext(file_name)
    extension = extension.lower()
    if extension == '.ply':
        reader = vtkPLYReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == '.vtp':
        reader = vtkXMLPolyDataReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == '.obj':
        reader = vtkOBJReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == '.stl':
        reader = vtkSTLReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == '.vtk':
        reader = vtkDataSetReader()
        reader.SetFileName(file_name)
        reader.Update()
        # reader contains unStructuredGrid data
        # So, we need to convert it to polydata using GeometryFilter
        gmtry_filter = vtkGeometryFilter()
        gmtry_filter.SetInputConnection(reader.GetOutputPort())
        gmtry_filter.Update()
        poly_data = gmtry_filter.GetOutput()
    elif extension == '.g':
        reader = vtkBYUReader()
        reader.SetGeometryFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    else:
        # Return a None if the extension is unknown.
        poly_data = None
    return poly_data


def SaveSceneToFieldData(data, actor, camera):
    # Actor
    #   Position, orientation, origin, scale, usrmatrix, usertransform
    # Camera
    #   FocalPoint, Position, ViewUp, ViewAngle, ClippingRange

    fp_format = '{0:.6f}'
    res = dict()
    res['Camera:FocalPoint'] = ', '.join(fp_format.format(n) for n in camera.GetFocalPoint())
    res['Camera:Position'] = ', '.join(fp_format.format(n) for n in camera.GetPosition())
    res['Camera:ViewUp'] = ', '.join(fp_format.format(n) for n in camera.GetViewUp())
    res['Camera:ViewAngle'] = fp_format.format(camera.GetViewAngle())
    res['Camera:ClippingRange'] = ', '.join(fp_format.format(n) for n in camera.GetClippingRange())
    buffer = ''
    for k, v in res.items():
        buffer += k + ' ' + v + '\n'
    cameraArray = vtkStringArray()
    cameraArray.SetNumberOfValues(1)
    cameraArray.SetValue(0, buffer)
    cameraArray.SetName('Camera')
    data.GetFieldData().AddArray(cameraArray)


def RestoreSceneFromFieldData(data, actor, camera):
    import re

    # Some regular expressions.

    reCP = re.compile(r'^Camera:Position')
    reCFP = re.compile(r'^Camera:FocalPoint')
    reCVU = re.compile(r'^Camera:ViewUp')
    reCVA = re.compile(r'^Camera:ViewAngle')
    reCCR = re.compile(r'^Camera:ClippingRange')
    keys = [reCP, reCFP, reCVU, reCVA, reCCR]

    # float_number = re.compile(r'[^0-9.\-]*([0-9e.\-]*[^,])[^0-9.\-]*([0-9e.\-]*[^,])[^0-9.\-]*([0-9e.\-]*[^,])')
    # float_scalar = re.compile(r'[^0-9.\-]*([0-9.\-e]*[^,])')

    buffer = data.GetFieldData().GetAbstractArray('Camera').GetValue(0).split('\n')
    res = dict()
    for line in buffer:
        if not line.strip():
            continue
        line = line.strip().replace(',', '').split()
        for i in keys:
            m = re.match(i, line[0])
            if m:
                k = m.group(0)
                if m:
                    #  Convert the rest of the line to floats.
                    v = list(map(lambda x: float(x), line[1:]))
                    if len(v) == 1:
                        res[k] = v[0]
                    else:
                        res[k] = v
    for k, v in res.items():
        if re.match(reCP, k):
            camera.SetPosition(v)
        elif re.match(reCFP, k):
            camera.SetFocalPoint(v)
        elif re.match(reCVU, k):
            camera.SetViewUp(v)
        elif re.match(reCVA, k):
            camera.SetViewAngle(v)
        elif re.match(reCCR, k):
            camera.SetClippingRange(v)


if __name__ == '__main__':
    main()
