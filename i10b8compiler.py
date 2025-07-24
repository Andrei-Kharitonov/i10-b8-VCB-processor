# Compiler
# =====================================
# idle       NA
# 0000       ----
#
# addr       reg       reg
# 0001       [00]      [00]
#
# subr       reg       reg
# 0010       [00]      [00]
#
# jump_c     const
# 0011       [0000]
#
# jump_r     reg       flags_[d/o/n/z]
# 0100       [00]      [00]
#
# setr_c     reg       const
# 0101       [00]      [00]
#
# load_c     reg       const
# 0110       [00]--    [00000000]
#
# load_m     reg       mem
# 0111       [00]--    [00000000]
#
# save_m     reg       mem
# 1000       [00]--    [00000000]
#
# incr       reg       neg
# 1001       [00]      [0]-
#
# halt       reg       input
# 1111       [00]      [0]-
# =====================================

# First 4 bytes must be empty
binary_data = [0b00000000, 0b00000000, 0b00000000, 0b00000000]
program_size = 1

# Registers
reg0 = 0b00000000
reg1 = 0b00000001
reg2 = 0b00000010
reg3 = 0b00000011

# Compiler functions
def byte_add(byte):
  global binary_data
  global program_size
  if not (0 <= byte <= 255):
    raise ValueError('byte_add argument must be from 0 to 255 included')
  binary_data += [0b00000000, 0b00000000, 0b00000000, byte]
  program_size += 1

def register_validation(r_2bit, func_name):
  if not (0 <= r_2bit <= 3):
    raise ValueError(f'{func_name} register address must be from 0 to 3 included')

def compile_vmem(file_name: str):
  '''
  Compiling program and write to the .vcbmem file
  '''
  global binary_data
  global program_size
  print(f'Program size = {program_size} bytes.')
  if (program_size <= 256):
    with open(f'{file_name}.vcbmem', "wb") as file:
      file.write(bytearray(binary_data))
    print('Compilation completed!')
  else:
    raise Exception('Compilation failed! The program is bigger than 256 byte.')
  
def get_program_size():
  '''
  Return current size of program in bytes
  '''
  global program_size
  return program_size

def get_binary_data():
  '''
  Return list of current instructions in binary
  '''
  global binary_data
  return binary_data

# Instructions
def idle():
  '''
  Do nothing, but needs for propper processor work
  '''
  inst = 0b00000000
  byte_add(inst)

def addr(r1_2bit: int, r2_2bit: int):
  '''
  Take 2 register addresses as arguments, then write sum of their values in r1_2bit
  '''
  inst = 0b00010000
  register_validation(r1_2bit, 'addr')
  register_validation(r2_2bit, 'addr')
  inst += (r1_2bit << 2) + r2_2bit
  byte_add(inst)

def subr(r1_2bit: int, r2_2bit: int):
  '''
  Take 2 register addresses as arguments, then subtract vaulue of r2_2bit from value of r1_2bit and write result in r1_2bit
  '''
  inst = 0b00100000
  register_validation(r1_2bit, 'subr')
  register_validation(r2_2bit, 'subr')
  inst += (r1_2bit << 2) + r2_2bit
  byte_add(inst)

def jump_c(address_4bit: int):
  '''
  Set current memory address to a address_4bit + 1 in argument
  '''
  inst = 0b00110000
  if not (0 <= address_4bit <= 15):
    raise ValueError('jump_c address argument must be from 0 to 15 included')
  inst += address_4bit
  byte_add(inst)

def jump_r(r_2bit: int, overflow=False, negative=False, zero=False):
  '''
  Set current memory address to a vaule of r_2bit + 1. Contain facultative condition flags:
  overflow - make jump_r only if result of last math operation cause overflow;
  negative - make jump_r only if result of last math operation was negative;
  zero - make jump_r only if result of last math operation was zero.
  '''
  inst = 0b01000000
  register_validation(r_2bit, 'jump_r')
  inst += (r_2bit << 2)
  if not overflow and not negative and not zero:
    inst += 0b00000000
  if overflow and not negative and not zero:
    inst += 0b00000001
  elif negative and not overflow and not zero:
    inst += 0b00000010
  elif zero and not overflow and not negative:
    inst += 0b00000011
  else:
    raise ValueError('jump_r can take only 1 flag')
  byte_add(inst)

def setr_c(r_2bit: int, num_4bit: int):
  '''
  Set 2 bit number in register (mostly used to set value of reg to 0 or 1)
  '''
  inst = 0b01010000
  if not (0 <= num_4bit <= 15):
    raise ValueError('setr_c number argument must be from 0 to 15 included')
  register_validation(r_2bit, 'setr_c')
  inst += (r_2bit << 2) + num_4bit
  byte_add(inst)

def load_c(r_2bit: int, num_8bit: int):
  '''
  Load number in register
  '''
  inst = 0b01100000
  if not (0 <= num_8bit <= 255):
    raise ValueError('load_c number argument must be from 0 to 255 included')
  register_validation(r_2bit, 'load_c')
  inst += (r_2bit << 2)
  byte_add(inst)
  byte_add(num_8bit)

def load_m(r_2bit: int, address_8bit: int):
  '''
  Load number from memory cell location at address_8bit
  '''
  inst = 0b01110000
  if not (0 <= address_8bit <= 255):
    raise ValueError('load_m address argument must be from 0 to 255 included')
  register_validation(r_2bit, 'load_m')
  inst += (r_2bit << 2)
  byte_add(inst)
  byte_add(address_8bit)

def save_m(r_2bit: int, address_8bit: int):
  '''
  Save value of register to memory cell location at address_8bit
  '''
  inst = 0b10000000
  if not (0 <= address_8bit <= 255):
    raise ValueError('save_m address argument must be from 0 to 255 included')
  register_validation(r_2bit, 'save_m')
  inst += (r_2bit << 2)
  byte_add(inst)
  byte_add(address_8bit)

def incr(r_2bit: int, negative=False):
  '''
  Increment value of register. If contain flag negative - decrement.
  '''
  inst = 0b10010000
  register_validation(r_2bit, 'incr')
  inst += (r_2bit << 2)
  if negative:
    inst += 0b00000010
  byte_add(inst)

def halt(r_2bit: int, input_flag=False):
  '''
  Stops program execution and display value of register untill "continue" button press.
  If has input_flag - doesn't display value. Instead of this it write value from input when "continue" button pressed into register.
  '''
  inst = 0b11110000
  register_validation(r_2bit, 'halt')
  inst += (r_2bit << 2)
  if input_flag:
    inst += 0b00000010
  byte_add(inst)

__all__ = [
  'reg0', 'reg1', 'reg2', 'reg3',
  'idle', 'addr', 'subr', 'jump_c', 'jump_r', 'setr_c', 'load_c', 'load_m', 'save_m', 'incr', 'halt',
  'compile_vmem', 'get_program_size', 'get_binary_data'
]