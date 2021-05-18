from compression import compress_sequence
from yuv_reader import read_yuv
from file_utils import writeFile, readFile
from decompression import build_sequence

import time
import numpy as np
import matplotlib.pyplot as plt

def videoCompression(filename, block_size = 16, delta = 50):
  frames = read_yuv(filename)
  first_frame, residuals, motion_vectors = compress_sequence(frames, block_size, delta)
  filename_out = "video.vid"
  writeFile(filename_out, first_frame, residuals, motion_vectors)
  return filename_out

def videoDecompression(filename, block_size = 16):
  print("Começando a descompressão ...")

  rec_first_frame, rec_residuals, rec_motion_vectors = readFile(filename)
  recovered = build_sequence(rec_first_frame, rec_residuals, rec_motion_vectors, block_size)
  recovered = np.array(recovered)
  for i in range(recovered.shape[0]):
    plt.imshow(recovered[i,:,:])
    plt.pause(0.03)
  '''
  fig = plt.figure(1)
  ax = fig.add_subplot( 111 )
  ax.set_title("My Title")
  im = ax.imshow(np.zeros((144, 176, 3))) #Imagem inicial preta
  fig.show()
  im.axes.figure.canvas.draw()

  tstart = time.time()
  for a in range(len(recovered)):
    ax.set_title(str(a))
    im.set_data(recovered[a])
    im.axes.figure.canvas.draw()

  print('FPS:', 100 / (time.time() - tstart))'''

if __name__ == "__main__":
  filename = input("Informe o nome (caminho) do video YUV a ser codificado: ")
  filename_out = videoCompression(filename)
  videoDecompression(filename_out)
