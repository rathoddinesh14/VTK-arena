import SimpleITK as sitk
from scipy.io import savemat
import argparse
import os


def from_raw_2_np(filename):
    '''
    The filename should be .mhd associated with the .raw file
    you want to convert into the numpy array.
    '''
    reader = sitk.ImageFileReader()
    reader.SetImageIO("MetaImageIO")
    reader.SetFileName(filename)

    image = reader.Execute()
    return sitk.GetArrayFromImage(image)


parser = argparse.ArgumentParser(description='Convert .raw into .mat')
parser.add_argument('file_path', metavar='filename', type=str, nargs=1,
                    help='Path to the .mhd file')

args = parser.parse_args()
filepath = args.file_path[0]
filename = os.path.basename(filepath)

arr = from_raw_2_np(f'{filename}')

slice_0 = arr[:, :, 0]
# print(slice_0.shape)

# center
center = (slice_0.shape[0] // 2, slice_0.shape[1] // 2)
print(center)

radius = 91

for k in range(arr.shape[2]):
    # circular mask with radius = radius
    for i in range(slice_0.shape[0]):
        for j in range(slice_0.shape[1]):
            if (i - center[0]) ** 2 + (j - center[1]) ** 2 > radius ** 2:
                arr[i, j, k] = 0

# mask = slice_0 > 6000
# print(mask)

# import numpy as np
# masked = np.zeros(slice_0.shape)
# masked[mask] = slice_0[mask]

# import matplotlib.pyplot as plt

# # plot
# f, ax = plt.subplots(1, 2)
# ax[0].imshow(slice_0, cmap='gray')
# ax[1].imshow(masked, cmap='gray')
# plt.show()

my_var_dict = dict(volm=arr)
filename = os.path.splitext(filename)[0]
savemat(f'{filename}.mat', my_var_dict)