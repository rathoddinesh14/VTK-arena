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
renderView1.ViewSize = [585, 815]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [115.12809515867616, 757.1062141140501, 656.4474860550454]
renderView1.CameraViewUp = [0.9006057145935102, -0.3547199442973931, 0.2511635084146722]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 1.8452567427040978

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.ViewSize = [584, 815]
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.StereoType = 'Crystal Eyes'
renderView2.CameraPosition = [115.12809515867616, 757.1062141140501, 656.4474860550454]
renderView2.CameraViewUp = [0.9006057145935102, -0.3547199442973931, 0.2511635084146722]
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
layout1.SetSize(1170, 815)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView2)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'XML Image Data Reader'
brainvti = XMLImageDataReader(registrationName='brain.vti', FileName=['/home/rathod/Git repos/TopologicalCompression/data/brain.vti'])
brainvti.PointArrayStatus = ['Result']
brainvti.TimeArray = 'None'

# create a new 'TTK PersistenceDiagram'
tTKPersistenceDiagram1 = TTKPersistenceDiagram(registrationName='TTKPersistenceDiagram1', Input=brainvti)
tTKPersistenceDiagram1.ScalarField = ['POINTS', 'Result']
tTKPersistenceDiagram1.InputOffsetField = ['POINTS', 'Result']

# ----------------------------------------------------------------
# restore active source
SetActiveSource(tTKPersistenceDiagram1)
# ----------------------------------------------------------------


if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')