#!/usr/bin/env python

# pipeline creation and rendering for cylinder

import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkCylinderSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

def render_object_with_center(object, center):
    colors = vtkNamedColors()

    # set the bg color
    bg = map(lambda x: x / 255.0, [26, 51, 100, 255])
    colors.SetColor("BkgColor", *bg)

    object_mapper = vtkPolyDataMapper()
    object_mapper.SetInputConnection(object.GetOutputPort())
    center_mapper = vtkPolyDataMapper()
    center_mapper.SetInputConnection(center.GetOutputPort())

    # this actor is a grouping mechanism: besides the geometry (mapper)
    # it also has a property, transformation matrix, and/or texture map.
    # Here we set its color and rotate it 22.5 degrees
    object_actor = vtkActor()
    center_actor = vtkActor()

    object_actor.SetMapper(object_mapper)
    center_actor.SetMapper(center_mapper)

    object_actor.GetProperty().SetColor(colors.GetColor3d("Orange"))
    object_actor.RotateX(40.0)
    object_actor.RotateY(-20.0)
    object_actor.RotateZ(-30.0)

    # set object transparency
    object_actor.GetProperty().SetOpacity(0.5)

    center_actor.GetProperty().SetColor(colors.GetColor3d("Green"))
    # translate the center
    center_actor.SetPosition(0, 0, 0)

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
    renderer.AddActor(object_actor)
    renderer.AddActor(center_actor)
    renderer.SetBackground(colors.GetColor3d("BkgColor"))
    renderer_window.SetSize(900, 900)
    renderer_window.SetWindowName("object example")

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

def main():
    # polygonal cylinder model with eight circumferential facets
    cylinder = vtkCylinderSource()
    cylinder.SetResolution(8)

    sphere = vtkSphereSource()
    sphere.SetRadius(0.1)
    sphere.SetThetaResolution(100)
    sphere.SetPhiResolution(100)

    render_object_with_center(cylinder, sphere)


if __name__ == '__main__':
    main()
