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
    return (array.astype(np.uint8), m, M)
