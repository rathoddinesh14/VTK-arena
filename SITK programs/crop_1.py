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
        npa[point[0] - left_bound[0], point[1] - left_bound[1], point[2] - left_bound[2]] = img[point[0], point[1], point[2]]

    print("Marked all points outside the point cloud as 0")

    image = sitk.GetImageFromArray(npa)

    # crop the image
    cropped_image = image[left_bound[0]:right_bound[0], left_bound[1]:right_bound[1], left_bound[2]:right_bound[2]]
    
    cropped_image.SetSpacing(space)
    cropped_image.SetOrigin(origin)
    cropped_image.SetDirection(direction)
    sitk.WriteImage(cropped_image, filename)

    return cropped_image

image_file_reader = sitk.ImageFileReader()
# image_file_reader.SetFileName(sys.argv[1])
image_file_reader.SetFileName("../data/chamf_distance_crop_downsampled_Dry_Deposition.mhd")
image_file_reader.SetImageIO('')

image = image_file_reader.Execute()

print(image.GetSize())
print(image.GetSpacing())
print(image.GetOrigin())
print(image.GetDirection())
print(image.GetPixelIDTypeAsString())
print(image.GetMetaDataKeys())

npa = sitk.GetArrayFromImage(image)


point_cloud = []
# sample 100 points from sphere with radius 10
for x in range(0, 100):
    for y in range(0, 100):
        for z in range(0, 100):
            if (x - 50) ** 2 + (y - 50) ** 2 + (z - 50) ** 2 < 50 ** 2:
                point_cloud.append((x, y, z))
# print(point_cloud)

left_bound = (0, 0, 0)
right_bound = (100, 100, 100)


cropped_image = write_to_mhd(image, image.GetSpacing(), (1,1,1), image.GetDirection(), 'new.mhd', point_cloud, left_bound, right_bound)

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