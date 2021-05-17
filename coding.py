import bitstring as bs
import numpy as np
import io
from PIL import Image

#--Coding utils------

def codedVector(motion_vector):
    code = bs.Bits(bin= '0b')
    for x in motion_vector:
      code += codeExpGolombExt(x)
    return code

def codeExpGolombExt(number):
  if number > 0:
    value = 2*number - 1
  else:
    value = -2*number
  size = int(np.log2(value+1)) + 1
  code = bs.Bits(bin= '0b0') * (size-1)
  code += bs.Bits(uint= value+1, length= size)
  return code

def encodeToJpeg(residual):
    #bytesio_residual = io.BytesIO(residual.astype(np.uint8).tobytes())
    with io.BytesIO() as f:
      im = Image.fromarray(residual)
      im.save(f, format='JPEG')
      return f.getvalue()

def decodeFromJpeg(img_bytes):
    with io.BytesIO() as f:
      f.write(img_bytes)
      with Image.open(f) as im:
        return np.asarray(im)

#--File reading------

def readNumber(file_bits: bs.Bits):
  idx = 0
  size = 0
  value = bs.Bits(bin= '0b')

  b = file_bits[idx]

  while(not b):
      size += 1
      idx += 1
      b = file_bits[idx]
  
  for i in range(size+1):
    #print(idx, file_bits.len, size)
    b = file_bits[idx]
    value += bs.Bits(bin= '0b1') if b else bs.Bits(bin= '0b0')
    idx += 1

  value = value.uint - 1
  if value % 2 == 0:
    number = -1*value//2
  else:
    number = (value + 1)//2

  return file_bits[idx:], number

def getFrame(video_bytes, first=False):
  num_blocks = 144//16 * 176//16
  vector = []
  offset = 0

  if not first:
    bits_size = int.from_bytes(video_bytes[:2], byteorder='big')
    bytes_used = int(np.ceil(bits_size/8))
    offset = 2 + bytes_used
    bit_vector = bs.Bits(bytes= video_bytes[2:offset], length= bits_size)
    vmin_n = int.from_bytes(video_bytes[offset: offset+2], byteorder='big', signed= True)
    vmax_n = int.from_bytes(video_bytes[offset+2:offset+4], byteorder='big', signed= True)
    offset = offset+4
    for i in range(num_blocks):
      bit_vector, value1 = readNumber(bit_vector)
      bit_vector, value2 = readNumber(bit_vector)
      vector.append((value1, value2))

  img_len = int.from_bytes(video_bytes[offset: offset+3], byteorder='big')
  offset = offset+3
  img_bytes = video_bytes[offset:img_len + offset]
  offset = img_len + offset

  img_array = decodeFromJpeg(img_bytes)

  if first:
    return img_array, video_bytes[offset:]

  else:
    return np.array(vector), vmin_n, vmax_n, img_array, video_bytes[offset:]

#--File writing------

def writeVector(motion_vectors, video_bits):
  for v in motion_vectors:
    video_bits += codedVector(v)
  return video_bits

#f = file object
def writeFrame(f, residual, motion_vectors, vmin, vmax, first=False):
  residual_jpg = encodeToJpeg(residual)
  if not first:
    bits = writeVector(motion_vectors, bs.Bits(bin= '0b'))
    #Tamanho em bits do vetor (incluso padding)
    bs.Bits(uint= bits.len, length=16).tofile(f)
    bits.tofile(f)
    bs.Bits(int= int(vmin), length=16).tofile(f)
    bs.Bits(int= int(vmax), length=16).tofile(f)
  img = residual_jpg
  bs.Bits(uint= len(img), length=24).tofile(f)
  f.write(img)