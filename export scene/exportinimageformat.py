import vtk

# Create a renderer, render window, and interactor
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

# Add some actors to the renderer
sphere = vtk.vtkSphereSource()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(1)
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())
actor = vtk.vtkActor()
actor.SetMapper(mapper)
renderer.AddActor(actor)

# Render the scene
renderWindow.Render()

# Create a window-to-image filter and set its input to the render window
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renderWindow)

# Set the image format and file name
w2if.SetInputBufferTypeToRGBA()

# Update the filter and write the output image
w2if.Update()
writer = vtk.vtkPNGWriter()
writer.SetFileName("sphere.png")
writer.SetInputConnection(w2if.GetOutputPort())
writer.Write()
