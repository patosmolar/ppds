from numba import cuda
import numpy as np

@cuda.jit
def convolve(result, mask, image):
    # expects a 2D grid and 2D blocks,
    # a mask with odd numbers of rows and columns, (-1-) 
    # a grayscale image
    
    # (-2-) 2D coordinates of the current thread:
    i, j = cuda.grid(2) 
    
    # (-3-) if the thread coordinates are outside of the image, we ignore the thread:
    image_rows, image_cols = image.shape
    if (i >= image_rows) or (j >= image_cols): 
        return
    
    # To compute the result at coordinates (i, j), we need to use delta_rows rows of the image 
    # before and after the i_th row, 
    # as well as delta_cols columns of the image before and after the j_th column:
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
    