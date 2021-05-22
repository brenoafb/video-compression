from compression import compress_sequence
from yuv_reader import read_yuv
from file_utils import writeFile, readFile
from decompression import build_sequence

import sys
import numpy as np
import matplotlib.pyplot as plt

def videoCompression(filename, delta = 50, quality=95):
  block_size = 16
  frames = read_yuv(filename)
  first_frame, residuals, motion_vectors = compress_sequence(frames, block_size, delta, quality=quality)
  filename_out = "video.vid"
  writeFile(filename_out, first_frame, residuals, motion_vectors, quality= quality)
  return filename_out

def videoDecompression(filename):
  block_size = 16
  print("Começando a descompressão ...")

  rec_first_frame, rec_residuals, rec_motion_vectors = readFile(filename)
  recovered = build_sequence(rec_first_frame, rec_residuals, rec_motion_vectors, block_size)
  recovered = np.array(recovered)
  for i in range(recovered.shape[0]):
    plt.imshow(recovered[i,:,:])
    plt.pause(0.001)

if __name__ == "__main__":
  filename = input("Informe o nome (caminho) do video YUV a ser codificado: ")
  filename_out = ""
  if (len(sys.argv) > 1):
    quality = int(input("Informe a qualidade do Jpeg a ser utilizado: "))
    delta = int(input("Informe o tamanho da região de busca utilizada (ex: 50 para 25 pixels em cada direção): "))
    filename_out = videoCompression(filename, quality=quality, delta= delta)
  else: filename_out = videoCompression(filename)
  videoDecompression(filename_out)
