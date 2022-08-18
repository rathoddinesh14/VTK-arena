import vtk
import math

# pdb reader
reader = vtk.vtkPDBReader()
reader.SetFileName("/Users/rathod_ias/GitHub/VTK-arena/IO/lys.pdb")
reader.SetHBScale(1.0)
reader.SetBScale(1.0)
reader.Update()

# print number of atoms
print("Number of atoms: {0}".format(reader.GetNumberOfAtoms()))

resolution = math.sqrt(300000 / reader.GetNumberOfAtoms())

if resolution < 4:
    resolution = 4

if resolution > 20:
    resolution = 20

print("Resolution: {0}".format(resolution))

# sphere
sphere = vtk.vtkSphereSource()
sphere.SetThetaResolution(resolution)
sphere.SetPhiResolution(resolution)
sphere.SetRadius(1.0)
sphere.SetCenter(0, 0, 0)

# glyph
glyph = vtk.vtkGlyph3D()
glyph.SetInputConnection(reader.GetOutputPort())
glyph.SetSourceConnection(sphere.GetOutputPort())
glyph.SetOrient(1)
glyph.SetColorMode(1)
glyph.SetScaleMode(2)
glyph.SetScaleFactor(0.25)

# polydata mapping
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(glyph.GetOutputPort())
mapper.UseLookupTableScalarRangeOff()
mapper.ScalarVisibilityOn()
mapper.SetScalarModeToDefault()

# actor
atom = vtk.vtkActor()
atom.SetMapper(mapper)

# renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(atom)
renderer.SetBackground(0.2, 0.2, 0.2)

# tube
tube = vtk.vtkTubeFilter()
tube.SetInputConnection(reader.GetOutputPort())
tube.SetNumberOfSides(resolution)
tube.CappingOff()
tube.SetRadius(0.1)
tube.SetVaryRadius(0)
tube.SetRadiusFactor(10)

# bond mapper
bondMapper = vtk.vtkPolyDataMapper()
bondMapper.SetInputConnection(tube.GetOutputPort())
bondMapper.UseLookupTableScalarRangeOff()
bondMapper.ScalarVisibilityOff()
bondMapper.SetScalarModeToDefault()

# bond actor
bond = vtk.vtkActor()
bond.SetMapper(bondMapper)
bond.GetProperty().SetColor(0.5, 0.5, 0.5)
renderer.AddActor(bond)

# window
window = vtk.vtkRenderWindow()
window.SetSize(600, 600)
window.AddRenderer(renderer)

# interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)
interactor.Initialize()
interactor.Start()