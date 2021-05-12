import numpy as np

def scale_to_img(array):
    '''
    given an array, scale it so all it's values are in the
    range [0,255]
    '''
    array = array.astype(np.float32)
    array -= array.min()
    array /= array.max()
    array *= 255
    return array.astype(np.uint8)