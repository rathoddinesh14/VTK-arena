#!/usr/bin/env python

import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def get_program_parameters():
    import argparse
    description = 'Read a .stl file.'
    epilogue = ''''''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='42400-IDGH.stl')
    args = parser.parse_args()
    return args.filename


def main():

    filename = get_program_parameters()

    colors = vtkNamedColors()

    # set the bg color
    bg = map(lambda x: x / 255.0, [220, 195, 195, 255])
    colors.SetColor("BkgColor", *bg)

    # read STL file
    reader = vtkSTLReader()
    reader.SetFileName(filename)

    # mapper is responsible for pushing the geometry into
    # the graphics library. It may also do color mapping, if scalars or
    # other attributes are defined
    geometry_mapper = vtkPolyDataMapper()
    geometry_mapper.SetInputConnection(reader.GetOutputPort())

    # this actor is a grouping mechanism: besides the geometry (mapper)
    # it also has a property, transformation matrix, and/or texture map.
    # Here we set its color and rotate it 22.5 degrees
    stl_actor = vtkActor()
    stl_actor.SetMapper(geometry_mapper)
    stl_actor.GetProperty().SetColor(colors.GetColor3d("Silver"))
    stl_actor.RotateX(40.0)
    stl_actor.RotateY(-20.0)
    stl_actor.RotateZ(-30.0)

    # graphics structure. The renderer renders into the render window
    # The render window interactor captures mouse events and will per
    # form appropriate camera or actor manipulation depending on the
    # nature of the events
    renderer = vtkRenderer()
    renderer_window = vtkRenderWindow()
    renderer_window.AddRenderer(renderer)
    interactor_renderer = vtkRenderWindowInteractor()
    interactor_renderer.SetRenderWindow(renderer_window)

    # Add the actor to the renderer, set the bg and size
    renderer.AddActor(stl_actor)
    renderer.SetBackground(colors.GetColor3d("BkgColor"))
    renderer_window.SetSize(800, 800)
    renderer_window.SetWindowName("Stereo lithography example")

    # this allows the interactor to initialize itself. It has
    # to be called before the event loop
    interactor_renderer.Initialize()

    # ambient occlusion
    renderer.UseFXAAOn()
    renderer.SetUseDepthPeeling(True)
    renderer.SetOcclusionRatio(0.9)
    renderer.SetUseFXAA(True)
    renderer.SetUseShadows(True)
    renderer.SetMaximumNumberOfPeels(100)

    # we will zoom in a little by accessing the camera
    # and invoking a zoom method on it
    renderer.ResetCamera()
    renderer.GetActiveCamera().Zoom(1.5)
    renderer.Render()

    # Start the event loop
    interactor_renderer.Start()


if __name__ == '__main__':
    main()
