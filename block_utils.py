import numpy as np

def get_block_from_motion_vectors(frame, motion_vector, block_size, i1, j1):
  '''
  Find the corresponding block in frame i+1 from frame i
  '''
  i0 = i1 - motion_vector[0]
  j0 = j1 - motion_vector[1]

  block = frame[i0 : i0 + block_size, j0 : j0 + block_size, :]
  return block

def get_blocks(mat: np.ndarray, block_size: int) -> tuple:
    '''
    Break a matrix into square blocks of the specified size
    For best results, the size of the matrix should be a
    multiple of block_size
    '''
    blocks_per_column = mat.shape[0] // block_size
    blocks_per_row = mat.shape[1] // block_size
    blocks = []
    for i in range(blocks_per_column):
        start1 = i * block_size
        end1 = (i + 1) * block_size
        for j in range(blocks_per_row):
            start2 = j * block_size
            end2 = (j + 1) * block_size
            block = mat[start1:end1, start2:end2,:]
            blocks.append((block, (i * block_size, j * block_size)))
    return blocks

def blocks_to_frame(blocks, height, width):
    '''
    Convert an array of square blocks into a frame of wize
    (height, width)
    '''
    block_size = blocks[0][0].shape[0]
    img = np.zeros((height, width, 3))
    for (block, coords) in blocks:
        p = coords[0]
        q = coords[1]
        for i in range(block_size):
            for j in range(block_size):
                img[p+i,q+j] = block[i,j]
    return img