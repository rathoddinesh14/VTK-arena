#!/usr/bin/env python

import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkBoxWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


# 3d widget works in event loop.

def main(argv):
    colors = vtkNamedColors()

    #
    # Cone is a source process object. it produces data
    # (output type is vtkPolyData) which other filters may process.
    #
    cone = vtkConeSource()
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(10)

    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())

    #
    # Create an actor to represent the cone. The actor orchestrates rendering
    # of the mapper's graphics primitives. An actor also refers to properties
    # via a vtkProperty instance, and includes an internal transformation
    # matrix. We set this actor's mapper to be coneMapper which we created
    # above.
    #
    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(colors.GetColor3d('Bisque'))

    ren1 = vtkRenderer()
    ren1.AddActor(coneActor)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(900, 900)
    renWin.SetWindowName('3D Widget')

    #
    # The vtkRenderWindowInteractor class watches for events (e.g., keypress,
    # mouse) in the vtkRenderWindow. These events are translated into
    # event invocations that VTK understands (see VTK/Common/vtkCommand.h
    # for all events that VTK processes). Then observers of these VTK
    # events can process them as appropriate.
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    #
    # By default the vtkRenderWindowInteractor instantiates an instance
    # of vtkInteractorStyle. vtkInteractorStyle translates a set of events
    # it observes into operations on the camera, actors, and/or properties
    # in the vtkRenderWindow associated with the vtkRenderWinodwInteractor.
    # Here we specify a particular interactor style.
    style = vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(style)

    #
    # Here we use a vtkBoxWidget to transform the underlying coneActor (by
    # manipulating its transformation matrix).
    # The SetInteractor method is how 3D widgets are associated with the render
    # window interactor. Internally, SetInteractor sets up a bunch of callbacks
    # using the Command/Observer mechanism (AddObserver()). The place factor
    # controls the initial size of the widget with respect to the bounding box
    # of the input to the widget.
    boxWidget = vtkBoxWidget()
    boxWidget.SetInteractor(iren)
    boxWidget.SetPlaceFactor(1.5)
    boxWidget.GetOutlineProperty().SetColor(colors.GetColor3d('Gold'))

    #
    # Place the interactor initially. The input to a 3D widget is used to
    # initially position and scale the widget. The EndInteractionEvent is
    # observed which invokes the SelectPolygons callback.
    #
    boxWidget.SetProp3D(coneActor)
    boxWidget.PlaceWidget()
    callback = vtkMyCallback()
    boxWidget.AddObserver('InteractionEvent', callback)

    #
    # Normally the user presses the 'i' key to bring a 3D widget to life. Here
    # we will manually enable it so it appears with the cone.
    #
    boxWidget.On()

    #
    # Start the event loop.
    #
    iren.Initialize()
    iren.Start()


class vtkMyCallback(object):
    """
    Callback for the interaction.
    """

    def __call__(self, caller, ev):
        # print class name
        print(caller.GetClassName())
        t = vtkTransform()
        print(t)
        widget = caller  # caller is the box widget
        widget.GetTransform(t)
        print(t)
        widget.GetProp3D().SetUserTransform(t)


if __name__ == '__main__':
    import sys

    main(sys.argv)
