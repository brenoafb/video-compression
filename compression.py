import numpy as np
from block_utils import blocks_to_frame, get_blocks, get_block_from_motion_vectors 
from img_utils import scale_to_img
import matplotlib.pyplot as plt

def compress_sequence(frames, block_size, delta):
  '''
  Given a sequence of frames, compress it into residuals
  and motion vectors
  '''
  first_frame = frames[0]
  prev_frame = first_frame
  residuals = []
  motion_vectors = []
  for (i, curr_frame) in enumerate(frames[1:]):
    print(i)
    blocks = get_blocks(curr_frame, block_size)
    residual, m, M, motion_vector = get_residual_and_vectors(prev_frame, blocks, delta)
    # scaled_residual = residual.astype(np.float32)
    # scaled_residual /= 255.0
    # scaled_residual *= M
    # scaled_residual += m
    residuals.append((residual, m, M))
    motion_vectors.append(motion_vector)
    prev_frame = curr_frame
  return (first_frame, residuals, motion_vectors)

def get_residual_and_vectors(frame, blocks, delta):
  block_size = blocks[0][0].shape[0]
  height, width, _ = frame.shape
  block_residuals = []
  motion_vectors = []
  for (block, coords) in blocks:
      found_coords = get_matching_block(frame, block, coords[0], coords[1], delta)
      found_block = frame[found_coords[0] : found_coords[0] + block_size,
                          found_coords[1] : found_coords[1] + block_size,
                          :]
      motion_vector = (coords[0] - found_coords[0], coords[1] - found_coords[1])
      block_residual = block.astype(np.float32) - found_block.astype(np.float32)
      block_residuals.append((block_residual, coords))
      motion_vectors.append(motion_vector)

  (residual, m, M) = scale_to_img(blocks_to_frame(block_residuals, height, width))
  return (residual, m, M, motion_vectors)

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