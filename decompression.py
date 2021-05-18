import numpy as np
from block_utils import blocks_to_frame, get_block_from_motion_vectors 
from img_utils import scale_to_img, scale_from_img

def build_sequence(frame, residuals, motion_vectors, block_size):
  '''
  Given frame 0, build the entire sequence
  '''
  frames = [frame]
  prev_frame = None
  for ((residual, m, M), motion_vector) in zip(residuals, motion_vectors):

    scaled_residual = scale_from_img(residual, m, M)
    #print(scaled_residual)

    if prev_frame is None:
      curr_frame = build_frame(frame, scaled_residual, motion_vector, block_size)
    else:
      curr_frame = build_frame(prev_frame, scaled_residual, motion_vector, block_size)
    frames.append(curr_frame)
    prev_frame = curr_frame
  return np.array(frames)

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
  next_frame = np.around(next_frame)
  next_frame[next_frame > 255] = 255
  next_frame[next_frame < 0] = 0

  return next_frame.astype(np.uint8)