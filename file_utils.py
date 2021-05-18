from coding import getFrame, writeFrame
from img_utils import scale_from_img

def readFile (filename):
  video_bytes = b''
  with open(filename, "rb") as f:
    video_bytes = f.read()

  rec_residuals = []
  rec_motion_vectors = []

  rec_first_frame, video_bytes = getFrame(video_bytes, first=True)

  while (video_bytes != b''):
    vector, vmin_n, vmax_n, img_array, video_bytes = getFrame(video_bytes)
    rec_residuals.append((img_array, vmin_n, vmax_n))
    rec_motion_vectors.append(vector)

  return rec_first_frame, rec_residuals, rec_motion_vectors

def writeFile (filename, first_frame, residuals, motion_vectors, quality= 95):
  with open(filename, "wb") as f:
    writeFrame(f, first_frame, None, None, None, first=True, quality = quality)
    for i in range(len(residuals)):
      writeFrame(f, residuals[i][0], motion_vectors[i], residuals[i][1], residuals[i][2], quality=quality)