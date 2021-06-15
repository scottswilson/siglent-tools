import os
import argparse
import re
from datetime import datetime

class VcdWriter:
  DATE = 'date'
  VERSION = 'version'
  COMMENT = 'comment'
  TIMESCALE = 'timescale'
  SCOPE = 'scope'
  VAR = 'var'
  UPSCOPE = 'upscope'
  END_DEF = 'enddefinitions'

  HEADER_KEYWORDS = [
    DATE,
    VERSION,
    COMMENT,
    TIMESCALE,
    SCOPE,
    VAR,
    UPSCOPE,
    END_DEF,
  ]

  BASE_CHAR = '!'

  def __init__(self, siglent_iter, **kwargs):
    self.header_info = {}
    self.header_info[self.DATE] = datetime.today().strftime("%Y-%m-%d")

    for key in self.HEADER_KEYWORDS:
      self.header_info[key] = [kwargs.get(key, '')]
    
    self.iter = siglent_iter
    self.PopulateHeader()

  def PopulateHeader(self):
    self.header_info[self.VAR] = []
    self.symbols = []
    first_time, first_logic_data = next(iter(self.iter))
    self.first_time = first_time
    for i in range(len(first_logic_data)):
      symbol = chr(ord(self.BASE_CHAR)+i)
      self.symbols.append(symbol)
      self.header_info[self.VAR].append(
        'wire {} {} D{}'.format( 1, symbol, i)
      )

  def Save(self, fp):
    with open(fp, 'w+') as f:
      self.WriteHeader(f)
      self.WriteData(f)

  def WriteHeader(self, open_file):
    for key, vals in self.header_info.items():
      for val in vals:
        open_file.write(f' ${key} {val} $end\n')

  def WriteData(self, open_file):
    time, last_logic_data = next(self.iter)
    diff = [str(int(x))+self.symbols[i] for i, x in enumerate(last_logic_data)]
    self.WriteDataLine(open_file, time, diff)

    for time, logic_data in self.iter:
      diff = [str(int(x))+self.symbols[i] for i, x in enumerate(logic_data) if x != last_logic_data[i]]
      if diff:
        self.WriteDataLine(open_file, time, diff)
      last_logic_data = logic_data

  def WriteDataLine(self, open_file, time, change_data):
    open_file.write('#{:<15} {}\n'.format(time-self.first_time, ' '.join(change_data)))

