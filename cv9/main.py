import skimage.data
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from numba import cuda
import numpy as np


full_image = rgb2gray(skimage.data.coffee()).astype(np.float32) / 255
plt.figure()
plt.imshow(full_image, cmap='gray')
plt.title("Full size image:")
image = full_image[150:350, 200:400].copy()
plt.figure()
plt.imshow(image, cmap='gray')
plt.title("Part of the image we use:")
plt.show()


@cuda.jit
def convolve(result, mask, image):
    # expects a 2D grid and 2D blocks,
    # a mask with odd numbers of rows and columns, (-1-)
    # a grayscale image

    # (-2-) 2D coordinates of the current thread:
    i, j = cuda.grid(2)

    # (-3-)
    image_rows, image_cols = image.shape
    if (i >= image_rows) or (j >= image_cols):
        return

    delta_rows = mask.shape[0] // 2
    delta_cols = mask.shape[1] // 2

    # The result at coordinates (i, j) is equal to
    # sum_{k, l} mask[k, l] * image[i - k + delta_rows, j - l + delta_cols]
    # with k and l going through the whole mask array:
    s = 0
    for k in range(mask.shape[0]):
        for l in range(mask.shape[1]):
            i_k = i - k + delta_rows
            j_l = j - l + delta_cols
            # (-4-) Check if (i_k, j_k) coordinates are inside the image:
            if (i_k >= 0) and (i_k < image_rows) and (j_l >= 0) and (j_l < image_cols):
                s += mask[k, l] * image[i_k, j_l]
    result[i, j] = s

# We preallocate the result array:
result = np.empty_like(image)

# We choose a random mask:
mask = np.random.rand(13, 13).astype(np.float32)
mask /= mask.sum()  # We normalize the mask
print('Mask shape:', mask.shape)
print('Mask first (3, 3) elements:\n', mask[:3, :3])

# We use blocks of 32x32 pixels:
blockdim = (32, 32)
print('Blocks dimensions:', blockdim)

# We compute grid dimensions big enough to cover the whole image:
griddim = (image.shape[0] // blockdim[0] + 1, image.shape[1] // blockdim[1] + 1)
print('Grid dimensions:', griddim)

# We apply our convolution to our image:
convolve[griddim, blockdim](result, mask, image)

# We plot the result:
plt.figure()
plt.imshow(image, cmap='gray')
plt.title("Before convolution:")
plt.figure()
plt.imshow(result, cmap='gray')
plt.title("After convolution:")
plt.show()
