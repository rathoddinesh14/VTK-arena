# state file generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [766, 815]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [108.41320425160235, 735.7869965288485, 681.3601636256119]
renderView1.CameraViewUp = [0.899699004765539, -0.3604961106398393, 0.2461386906551825]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 1.8452567427040978

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.ViewSize = [765, 815]
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.StereoType = 'Crystal Eyes'
renderView2.CameraPosition = [108.41320425160235, 735.7869965288485, 681.3601636256119]
renderView2.CameraViewUp = [0.899699004765539, -0.3604961106398393, 0.2461386906551825]
renderView2.CameraFocalDisk = 1.0
renderView2.CameraParallelScale = 1.8452567427040978

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.SplitHorizontal(0, 0.500000)
layout1.AssignView(1, renderView1)
layout1.AssignView(2, renderView2)
layout1.SetSize(1532, 815)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView2)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'XML Image Data Reader'
brain_20_decompressedvti = XMLImageDataReader(registrationName='brain_20_decompressed.vti', FileName=['/home/rathod/Git repos/TopologicalCompression/data/brain_20_decompressed.vti'])
brain_20_decompressedvti.PointArrayStatus = ['Decompressed', 'Offsets']
brain_20_decompressedvti.TimeArray = 'None'

# create a new 'TTK PersistenceDiagram'
tTKPersistenceDiagram2 = TTKPersistenceDiagram(registrationName='TTKPersistenceDiagram2', Input=brain_20_decompressedvti)
tTKPersistenceDiagram2.ScalarField = ['POINTS', 'Decompressed']
tTKPersistenceDiagram2.InputOffsetField = ['POINTS', 'Decompressed']

# create a new 'XML Image Data Reader'
brainvti = XMLImageDataReader(registrationName='brain.vti', FileName=['/home/rathod/Git repos/TopologicalCompression/data/brain.vti'])
brainvti.PointArrayStatus = ['Result']
brainvti.TimeArray = 'None'

# create a new 'TTK PersistenceDiagram'
tTKPersistenceDiagram1 = TTKPersistenceDiagram(registrationName='TTKPersistenceDiagram1', Input=brainvti)
tTKPersistenceDiagram1.ScalarField = ['POINTS', 'Result']
tTKPersistenceDiagram1.InputOffsetField = ['POINTS', 'Result']

# create a new 'TTK BottleneckDistance'
tTKBottleneckDistance1 = TTKBottleneckDistance(registrationName='TTKBottleneckDistance1', Persistencediagram1=tTKPersistenceDiagram1,
    Persistencediagram2=tTKPersistenceDiagram2)
tTKBottleneckDistance1.Persistencethreshold = 20.0

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# find source
tTKBottleneckDistance1_1 = FindSource('TTKBottleneckDistance1')

# show data from tTKBottleneckDistance1_1
tTKBottleneckDistance1_1Display = Show(OutputPort(tTKBottleneckDistance1_1, 2), renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
tTKBottleneckDistance1_1Display.Representation = 'Surface'
tTKBottleneckDistance1_1Display.ColorArrayName = [None, '']
tTKBottleneckDistance1_1Display.SelectTCoordArray = 'None'
tTKBottleneckDistance1_1Display.SelectNormalArray = 'None'
tTKBottleneckDistance1_1Display.SelectTangentArray = 'None'
tTKBottleneckDistance1_1Display.OSPRayScaleFunction = 'PiecewiseFunction'
tTKBottleneckDistance1_1Display.SelectOrientationVectors = 'None'
tTKBottleneckDistance1_1Display.ScaleFactor = -2.0000000000000002e+298
tTKBottleneckDistance1_1Display.SelectScaleArray = 'None'
tTKBottleneckDistance1_1Display.GlyphType = 'Arrow'
tTKBottleneckDistance1_1Display.GlyphTableIndexArray = 'None'
tTKBottleneckDistance1_1Display.GaussianRadius = -1e+297
tTKBottleneckDistance1_1Display.SetScaleArray = [None, '']
tTKBottleneckDistance1_1Display.ScaleTransferFunction = 'PiecewiseFunction'
tTKBottleneckDistance1_1Display.OpacityArray = [None, '']
tTKBottleneckDistance1_1Display.OpacityTransferFunction = 'PiecewiseFunction'
tTKBottleneckDistance1_1Display.DataAxesGrid = 'GridAxesRepresentation'
tTKBottleneckDistance1_1Display.PolarAxes = 'PolarAxesRepresentation'
tTKBottleneckDistance1_1Display.OpacityArrayName = [None, '']

# ----------------------------------------------------------------
# setup the visualization in view 'renderView2'
# ----------------------------------------------------------------

# show data from tTKBottleneckDistance1
tTKBottleneckDistance1Display = Show(tTKBottleneckDistance1, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
tTKBottleneckDistance1Display.Representation = 'Surface'
tTKBottleneckDistance1Display.ColorArrayName = [None, '']
tTKBottleneckDistance1Display.SelectTCoordArray = 'None'
tTKBottleneckDistance1Display.SelectNormalArray = 'None'
tTKBottleneckDistance1Display.SelectTangentArray = 'None'
tTKBottleneckDistance1Display.OSPRayScaleArray = 'Coordinates'
tTKBottleneckDistance1Display.OSPRayScaleFunction = 'PiecewiseFunction'
tTKBottleneckDistance1Display.SelectOrientationVectors = 'Coordinates'
tTKBottleneckDistance1Display.ScaleFactor = 25.5
tTKBottleneckDistance1Display.SelectScaleArray = 'Coordinates'
tTKBottleneckDistance1Display.GlyphType = 'Arrow'
tTKBottleneckDistance1Display.GlyphTableIndexArray = 'Coordinates'
tTKBottleneckDistance1Display.GaussianRadius = 1.2750000000000001
tTKBottleneckDistance1Display.SetScaleArray = ['POINTS', 'Coordinates']
tTKBottleneckDistance1Display.ScaleTransferFunction = 'PiecewiseFunction'
tTKBottleneckDistance1Display.OpacityArray = ['POINTS', 'Coordinates']
tTKBottleneckDistance1Display.OpacityTransferFunction = 'PiecewiseFunction'
tTKBottleneckDistance1Display.DataAxesGrid = 'GridAxesRepresentation'
tTKBottleneckDistance1Display.PolarAxes = 'PolarAxesRepresentation'
tTKBottleneckDistance1Display.ScalarOpacityUnitDistance = 3.2263609018339543
tTKBottleneckDistance1Display.OpacityArrayName = ['POINTS', 'Coordinates']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
tTKBottleneckDistance1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 229.5, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
tTKBottleneckDistance1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 229.5, 1.0, 0.5, 0.0]

# find source
tTKBottleneckDistance1_2 = FindSource('TTKBottleneckDistance1')

# show data from tTKBottleneckDistance1_2
tTKBottleneckDistance1_2Display = Show(OutputPort(tTKBottleneckDistance1_2, 1), renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
tTKBottleneckDistance1_2Display.Representation = 'Surface'
tTKBottleneckDistance1_2Display.ColorArrayName = [None, '']
tTKBottleneckDistance1_2Display.SelectTCoordArray = 'None'
tTKBottleneckDistance1_2Display.SelectNormalArray = 'None'
tTKBottleneckDistance1_2Display.SelectTangentArray = 'None'
tTKBottleneckDistance1_2Display.OSPRayScaleArray = 'Coordinates'
tTKBottleneckDistance1_2Display.OSPRayScaleFunction = 'PiecewiseFunction'
tTKBottleneckDistance1_2Display.SelectOrientationVectors = 'Coordinates'
tTKBottleneckDistance1_2Display.ScaleFactor = 25.5
tTKBottleneckDistance1_2Display.SelectScaleArray = 'Coordinates'
tTKBottleneckDistance1_2Display.GlyphType = 'Arrow'
tTKBottleneckDistance1_2Display.GlyphTableIndexArray = 'Coordinates'
tTKBottleneckDistance1_2Display.GaussianRadius = 1.2750000000000001
tTKBottleneckDistance1_2Display.SetScaleArray = ['POINTS', 'Coordinates']
tTKBottleneckDistance1_2Display.ScaleTransferFunction = 'PiecewiseFunction'
tTKBottleneckDistance1_2Display.OpacityArray = ['POINTS', 'Coordinates']
tTKBottleneckDistance1_2Display.OpacityTransferFunction = 'PiecewiseFunction'
tTKBottleneckDistance1_2Display.DataAxesGrid = 'GridAxesRepresentation'
tTKBottleneckDistance1_2Display.PolarAxes = 'PolarAxesRepresentation'
tTKBottleneckDistance1_2Display.ScalarOpacityUnitDistance = 6.415315017638008
tTKBottleneckDistance1_2Display.OpacityArrayName = ['POINTS', 'Coordinates']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
tTKBottleneckDistance1_2Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 229.5, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
tTKBottleneckDistance1_2Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 229.5, 1.0, 0.5, 0.0]

# show data from tTKBottleneckDistance1_1
tTKBottleneckDistance1_1Display_1 = Show(OutputPort(tTKBottleneckDistance1_1, 2), renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
tTKBottleneckDistance1_1Display_1.Representation = 'Surface'
tTKBottleneckDistance1_1Display_1.ColorArrayName = [None, '']
tTKBottleneckDistance1_1Display_1.SelectTCoordArray = 'None'
tTKBottleneckDistance1_1Display_1.SelectNormalArray = 'None'
tTKBottleneckDistance1_1Display_1.SelectTangentArray = 'None'
tTKBottleneckDistance1_1Display_1.OSPRayScaleFunction = 'PiecewiseFunction'
tTKBottleneckDistance1_1Display_1.SelectOrientationVectors = 'None'
tTKBottleneckDistance1_1Display_1.ScaleFactor = -2.0000000000000002e+298
tTKBottleneckDistance1_1Display_1.SelectScaleArray = 'None'
tTKBottleneckDistance1_1Display_1.GlyphType = 'Arrow'
tTKBottleneckDistance1_1Display_1.GlyphTableIndexArray = 'None'
tTKBottleneckDistance1_1Display_1.GaussianRadius = -1e+297
tTKBottleneckDistance1_1Display_1.SetScaleArray = [None, '']
tTKBottleneckDistance1_1Display_1.ScaleTransferFunction = 'PiecewiseFunction'
tTKBottleneckDistance1_1Display_1.OpacityArray = [None, '']
tTKBottleneckDistance1_1Display_1.OpacityTransferFunction = 'PiecewiseFunction'
tTKBottleneckDistance1_1Display_1.DataAxesGrid = 'GridAxesRepresentation'
tTKBottleneckDistance1_1Display_1.PolarAxes = 'PolarAxesRepresentation'
tTKBottleneckDistance1_1Display_1.OpacityArrayName = [None, '']

# ----------------------------------------------------------------
# restore active source
SetActiveSource(tTKBottleneckDistance1)
# ----------------------------------------------------------------


if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')