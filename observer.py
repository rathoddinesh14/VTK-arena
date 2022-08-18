#!/usr/bin/env python

import vtk
import time


def my_callback(obj, string):
    print("Starting a render")


# basic pipeline
cone = vtk.vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

cone_mapper = vtk.vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

cone_actor = vtk.vtkActor()
cone_actor.SetMapper(cone_mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(cone_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# adding the observer
renderer.AddObserver("StartEvent", my_callback)

renderer_window = vtk.vtkRenderWindow()
renderer_window.AddRenderer(renderer)
renderer_window.SetSize(800, 800)

# looping over 360 degrees and the render the cone each time
for i in range(0, 360):
    time.sleep(0.03)
    renderer_window.Render()
    renderer.GetActiveCamera().Azimuth(1)