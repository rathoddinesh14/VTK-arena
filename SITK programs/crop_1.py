import SimpleITK as sitk
import numpy as np
import sys


def write_to_mhd(img, space, origin, direction, filename, point_cloud, left_bound, right_bound):
    # npa = sitk.GetArrayFromImage(img)
    # # set all points within the bounding box to 0 except the ones in the point cloud
    # for x in range(left_bound[0], right_bound[0]):
    #     print("Processing : " + str(x - left_bound[0]) + " of " + str(right_bound[0] - left_bound[0]))
    #     for y in range(left_bound[1], right_bound[1]):
    #         for z in range(left_bound[2], right_bound[2]):
    #             if (x, y, z) not in point_cloud:
    #                 # print(x, y, z, npa[x, y, z])
    #                 npa[x, y, z] = 0

    # make zero numpy array of the same size as the original image
    npa = np.zeros((right_bound[0] - left_bound[0], right_bound[1] - left_bound[1], right_bound[2] - left_bound[2]), dtype=np.float32)
    # fill the array with the points in the point cloud
    for point in point_cloud:
        npa[point[0] - left_bound[0]-1, point[1] - left_bound[1]-1, point[2] - left_bound[2]-1] = img[point[0], point[1], point[2]]

    # print("Marked all points outside the point cloud as 0")

    # traspose the array to get the correct orientation
    npa = np.transpose(npa, (2, 1, 0))

    image = sitk.GetImageFromArray(npa)

    # crop the image
    # cropped_image = img[left_bound[0]:right_bound[0], left_bound[1]:right_bound[1], left_bound[2]:right_bound[2]]
    
    image.SetSpacing(space)
    image.SetOrigin(origin)
    image.SetDirection(direction)
    sitk.WriteImage(image, filename)

    return image

image_file_reader = sitk.ImageFileReader()
# image_file_reader.SetFileName(sys.argv[1])
image_file_reader.SetFileName("/home/rathod/Downloads/M.Tech Project Data/Outputs_05/chamf_distance_Steel.mhd")
image_file_reader.SetImageIO('')

image = image_file_reader.Execute()

print(image.GetSize())
print(image.GetSpacing())
print(image.GetOrigin())
print(image.GetDirection())
print(image.GetPixelIDTypeAsString())
print(image.GetMetaDataKeys())

# npa = sitk.GetArrayFromImage(image)


point_cloud = []
import vtk
# grain_41586.vtp 
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName("data/grain_41586.vtp")
reader.Update()
polydata = reader.GetOutput()


bounds = polydata.GetBounds()
offset = 1
left_bound = (int(bounds[0]) - offset, int(bounds[2]) - offset, int(bounds[4]) - offset)
right_bound = (int(bounds[1]) + offset, int(bounds[3]) + offset, int(bounds[5]) + offset)

points = polydata.GetPoints()
for i in range(points.GetNumberOfPoints()):
    point = points.GetPoint(i)
    # body center coordinate is point
    # add all corner points of the voxel to the point cloud
    for x in range(int(point[0]), int(point[0]) + 2):
        for y in range(int(point[1]), int(point[1]) + 2):
            for z in range(int(point[2]), int(point[2]) + 2):
                point_cloud.append((x, y, z))


cropped_image = write_to_mhd(image, image.GetSpacing(), left_bound, image.GetDirection(), 'new.mhd', point_cloud, left_bound, right_bound)

print(cropped_image.GetSize())

# # set all points to 0 except the ones in the point cloud
# for i in range(npa.shape[0]):
#     for j in range(npa.shape[1]):
#         for k in range(npa.shape[2]):
#             if (i, j, k) not in point_cloud:
#                 npa[i, j, k] = 0

# # write the image
# image_file_writer = sitk.ImageFileWriter()
# image_file_writer.SetFileName("cropped.mhd")
# image_file_writer.Execute(sitk.GetImageFromArray(npa))