import struct

INT_BYTE_LEN = 4
DOUBLE_BYTE_LEN = 8
DATA_START = 0x800
HEADER_LEN = 0x11c
RESERVE_BYTE_LEN = DATA_START - HEADER_LEN

HORI_DIV_NUM = 14
VERT_DIV_CODE = 25
magnitude = [
  10e-24,
  10e-21,
  10e-18,
  10e-15,
  10e-12,
  10e-9,
  10e-6,
  10e-3,
  1,
  10e3,
  10e6,
  10e9,
  10e12,
  10e15
]

def deal_to_data_unit(f, para_num):
  para = []
  for i in range(0,para_num):
    stream = f.read(DOUBLE_BYTE_LEN)
    data = struct.unpack('d',stream)[0]
    stream = f.read(INT_BYTE_LEN)
    unit = struct.unpack('i',stream)[0]
    stream = f.read(INT_BYTE_LEN)
    para.append(data * magnitude[unit])
  return para
  
def deal_to_int(f, para_num):
  para = []
  for i in range(0,para_num):
    stream = f.read(INT_BYTE_LEN)
    data= struct.unpack('i',stream)[0]
    para.append(data)
  return para
