import numpy as np
from block_utils import blocks_to_frame
from img_utils import scale_to_img

def build_frame(frame, residual, motion_vectors, block_size):
  '''
  Build frame i+1 from frame i
  '''
  blocks_per_column = frame.shape[0] // block_size
  blocks_per_row = frame.shape[1] // block_size
  coords = []
  for i in range(blocks_per_column):
      i1 = i * block_size
      for j in range(blocks_per_row):
          j1 = j * block_size
          coords.append((i1, j1))
    
  blocks = []
  for (motion_vector, (i1, j1)) in zip(motion_vectors, coords):
      block = get_block_from_motion_vectors(frame, motion_vector, block_size, i1, j1)
      blocks.append((block, (i1, j1)))
  
  next_frame = blocks_to_frame(blocks, frame.shape[0], frame.shape[1])
  next_frame += residual

  return next_frame

def get_block_from_motion_vectors(frame, motion_vector, block_size, i1, j1):
  '''
  Find the corresponding block in frame i+1 from frame i
  '''
  i0 = i1 - motion_vector[0]
  j0 = j1 - motion_vector[1]

  block = frame[i0 : i0 + block_size, j0 : j0 + block_size, :]
  return block


def get_residual_and_vectors(frame, blocks, delta):
  block_size = blocks[0][0].shape[0]
  height, width= frame.shape
  residuals = []
  motion_vectors = []
  for (block, coords) in blocks:
      found_coords = get_matching_block(frame, block, coords[0], coords[1], delta)
      found_block = frame[found_coords[0] : found_coords[0] + block_size,
                          found_coords[1] : found_coords[1] + block_size,
                          :]
      motion_vector = (coords[0] - found_coords[0], coords[1] - found_coords[1])
      residual = block.astype(np.float32) - found_block.astype(np.float32)
      residuals.append((residual, coords))
      motion_vectors.append(motion_vector)

  residual = scale_to_img(blocks_to_frame(residuals, height, width))
  return (residual, motion_vectors)

def get_matching_block(mat: np.ndarray, block: np.ndarray, i0: int, j0: int, delta: int) -> np.ndarray:
    '''
    Given a block belonging to frame n+1 with coordinates (i0, j0),
    find the block in frame i (mat) that minimizes the error around
    a vicinity of size delta
    '''
    block_size = block.shape[0]
    
    start_i = max(0, i0 - delta // 2)
    stop_i = min(i0 + delta // 2, mat.shape[0] - block_size)
    
    start_j = max(0, j0 - delta // 2)
    stop_j = min(j0 + delta // 2, mat.shape[1] - block_size)
    
    min_err = float('inf')
    coords = None
    
    for i in range(start_i, stop_i):
        for j in range(start_j, stop_j):
            curr_block = mat[i : i + block_size, j : j + block_size, :]
            err = np.linalg.norm(block - curr_block)
            if err < min_err:
                min_err = err
                coords = (i, j)
    return coords