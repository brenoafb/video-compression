import numpy as np

def read_yuv(filename, width=176, height=144):
    '''
    Read a YUV file to an RGB array of frames.
    '''
    file = open(filename, 'rb')

    frames = []
    while True:
        frame = read_frame(file)
        if frame is None:
            break
        y, u, v = frame
        u = resize_uv(u)
        v = resize_uv(v)
        array = np.dstack((y, u, v))
        rgb_array = ycbcr_to_rgb(array)
        frames.append(rgb_array)
    file.close()
    return np.array(frames)

def read_frame(file, width=176, height=144):
    '''
    Read a single YUV frame
    '''
    Y = read_y(file, width, height)
    UV = read_uv(file, width, height)
    if Y is None or UV is None:
        return None
    return (Y, UV[0], UV[1])
    
def read_y(file, width=176, height=144):
    '''
    Read the Y component of a single frame
    '''
    y_size = width * height
    y_bytes = file.read(y_size)
    if not y_bytes:
        return None
    y_array = yuv_bytelist_to_array(list(y_bytes), width, height)
    return y_array

def read_uv(file, width=176, height=144):
    '''
    Read the U and V components of a single frame
    '''
    uv_size = width * height // 4
    u_bytes = file.read(uv_size)
    if not u_bytes:
        return None
    v_bytes = file.read(uv_size)
    if not v_bytes:
        return None
    u_array = yuv_bytelist_to_array(list(u_bytes), width//2, height//2)
    v_array = yuv_bytelist_to_array(list(v_bytes), width//2, height//2)
    return u_array, v_array
    
def yuv_bytelist_to_array(bytelist, width, height):
    '''
    Convert a list of bytes read from a YUV file to an array
    of integers
    '''
    return np.array(bytelist, dtype=np.uint8).reshape(height, width)

def resize_uv(array):
    '''
    Convert U or V frame to double its size
    '''
    return np.kron(array, np.ones((2, 2))).astype(np.uint8)

# source: https://stackoverflow.com/a/34913974
def rgb_to_ycbcr(im):
    xform = np.array([[.299, .587, .114], [-.1687, -.3313, .5], [.5, -.4187, -.0813]])
    ycbcr = im.dot(xform.T)
    ycbcr[:,:,[1,2]] += 128
    return np.uint8(ycbcr)

def ycbcr_to_rgb(im):
    xform = np.array([[1, 0, 1.402], [1, -0.34414, -.71414], [1, 1.772, 0]])
    rgb = im.astype(np.float)
    rgb[:,:,[1,2]] -= 128
    rgb = rgb.dot(xform.T)
    np.putmask(rgb, rgb > 255, 255)
    np.putmask(rgb, rgb < 0, 0)
    return np.uint8(rgb)