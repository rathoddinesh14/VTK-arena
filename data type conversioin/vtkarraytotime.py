import sys
import vtk

writer = vtk.vtkXMLImageDataWriter()

data_to_write = vtk.vtkImageData()

writer.SetFileName(sys.argv[2] + ".vti")

# time step
writer.SetNumberOfTimeSteps(60)
writer.SetInputData(data_to_write)
writer.Start()

for i in range(60):
    # read vti file
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(sys.argv[1] + str(i) + ".vti")
    reader.Update()
    
    # array name to write
    array_name = ""
    if i < 5:
        array_name = "00" + str(i*2)
    elif i < 49:
        array_name = "0" + str(i*2)
    else:
        array_name = str(i*2)

    image = vtk.vtkImageData()
    image.GetPointData().SetActiveScalars(array_name)
    image.DeepCopy(reader.GetOutput())

    data_to_write.ShallowCopy(image)
    writer.WriteNextTime(i)

writer.Stop()