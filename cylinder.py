#!/usr/bin/env python

# pipeline creation and rendering for cylinder

import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():
    colors = vtkNamedColors()

    # set the bg color
    bg = map(lambda x: x / 255.0, [26, 51, 0, 255])
    colors.SetColor("BkgColor", *bg)

    # polygonal cylinder model with eight circumferential facets
    cylinder = vtkCylinderSource()
    cylinder.SetResolution(50)
    cylinder.SetRadius(59)
    cylinder.SetHeight(129.5)
    # center
    cylinder.SetCenter(0.0, 0.0, 0.0)

    # mapper is responsible for pushing the geometry into
    # the graphics library. It may also do color mapping, if scalars or
    # other attributes are defined
    cylinder_mapper = vtkPolyDataMapper()
    cylinder_mapper.SetInputConnection(cylinder.GetOutputPort())

    # this actor is a grouping mechanism: besides the geometry (mapper)
    # it also has a property, transformation matrix, and/or texture map.
    # Here we set its color and rotate it 22.5 degrees
    cylinder_actor = vtkActor()
    cylinder_actor.SetMapper(cylinder_mapper)
    cylinder_actor.GetProperty().SetColor(colors.GetColor3d("Orange"))
    cylinder_actor.RotateX(40.0)
    cylinder_actor.RotateY(-20.0)
    cylinder_actor.RotateZ(-30.0)

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
    renderer.AddActor(cylinder_actor)
    renderer.SetBackground(colors.GetColor3d("BkgColor"))
    renderer_window.SetSize(800, 800)
    renderer_window.SetWindowName("Cylinder example")

    # this allows the interactor to initialize itself. It has
    # to be called before the event loop
    interactor_renderer.Initialize()

    # we will zoom in a little by accessing the camera
    # and invoking a zoom method on it
    renderer.ResetCamera()
    renderer.GetActiveCamera().Zoom(1.5)
    renderer.Render()

    # Start the event loop
    interactor_renderer.Start()


if __name__ == '__main__':
    main()
