import numpy as np

def scale_to_img(array):
    '''
    given an array, scale it so all it's values are in the
    range [0,255]
    '''
    array = array.astype(np.float32)
    m = array.min()
    array -= m
    M = array.max()
    array /= M
    array *= 255
    array = np.around(array)
    return (array.astype(np.uint8), m, M)

def scale_from_img(residual, m, M):
    '''
    given an array, scale it so all it's values are in the
    range [0,255]
    '''
    scaled_residual = residual.astype(np.float32)
    scaled_residual *= M
    scaled_residual /= 255
    scaled_residual += m
    scaled_residual = np.around(scaled_residual)

    return scaled_residual.astype(np.float32)