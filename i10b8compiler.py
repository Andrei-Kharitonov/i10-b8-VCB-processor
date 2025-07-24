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
aliases = {}
not_declarated_aliases = []
program_current_size = 1

# Registers
reg0 = 0b00000000
reg1 = 0b00000001
reg2 = 0b00000010
reg3 = 0b00000011

# Compiler functions
def byte_add(byte):
  global binary_data
  global program_current_size

  binary_data += [0b00000000, 0b00000000, 0b00000000, byte]
  program_current_size += 1

def alias_add(alias: str, address: int):
  if alias != None and (len(alias.strip()) > 0):
    aliases[alias] = address - 2

def register_validation(r_2bit, func_name):
  if not (0 <= r_2bit <= 3):
    raise ValueError(f'{func_name} register address must be from 0 to 3 included')

def compile_vmem(file_name: str):
  '''
  Compiling program and write to the .vcbmem file
  '''
  global binary_data
  global program_current_size
  print(f'Program size = {program_current_size} bytes.')
  if (program_current_size <= 256):
    aliases_restore()
    with open(f'{file_name}.vcbmem', "wb") as file:
      file.write(bytearray(binary_data))
    print('Compilation completed!')
  else:
    raise Exception('Compilation failed! The program is bigger than 256 byte.')
  
def get_program_current_size():
  '''
  Return current size of program in bytes
  '''
  return program_current_size

def get_binary_data():
  '''
  Return list of current instructions in binary
  '''
  return binary_data

def get_alias(alias: str):
  '''
  Return value of alias
  '''
  try:
    return aliases[alias]
  except:
    not_declarated_aliases.append([alias, program_current_size])
    return 0

# Restore aliases that were called before declaration
def aliases_restore():
  for i in not_declarated_aliases:
    if i[0] in aliases:
      alias_value = aliases[i[0]]
      binary_instruction = binary_data[4 + i[1] * 4 - 1] >> 4
      if binary_instruction in [0b0110, 0b0111, 0b1000]:
        binary_data[4 + i[1] * 4 + 4 - 1] = alias_value
      elif binary_instruction in [0b0011]:
        if (0 > alias_value > 15):
          raise ValueError('aliases_restore: jump_c argument must be from 0 to 15 included')
        binary_data[4 + i[1] * 4 - 1] += alias_value
  
def get_all_aliases():
  return [aliases, not_declarated_aliases]


# Instructions
def idle(alias=''):
  '''
  Do nothing, but needs for propper processor work
  '''
  inst = 0b00000000
  byte_add(inst)
  alias_add(alias, program_current_size)


def addr(r1_2bit=0, r2_2bit=0, alias=''):
  '''
  Take 2 register addresses as arguments, then write sum of their values in r1_2bit
  '''
  inst = 0b00010000
  register_validation(r1_2bit, 'addr')
  register_validation(r2_2bit, 'addr')
  inst += (r1_2bit << 2) + r2_2bit
  byte_add(inst)
  alias_add(alias, program_current_size)


def subr(r1_2bit=0, r2_2bit=0, alias=''):
  '''
  Take 2 register addresses as arguments, then subtract vaulue of r2_2bit from value of r1_2bit and write result in r1_2bit
  '''
  inst = 0b00100000
  register_validation(r1_2bit, 'subr')
  register_validation(r2_2bit, 'subr')
  inst += (r1_2bit << 2) + r2_2bit
  byte_add(inst)
  alias_add(alias, program_current_size)


def jump_c(address_4bit: int, alias=''):
  '''
  Set current memory address to a address_4bit + 1 in argument
  '''
  inst = 0b00110000
  if not (0 <= address_4bit <= 15):
    raise ValueError('jump_c address argument must be from 0 to 15 included')
  inst += address_4bit
  byte_add(inst)
  alias_add(alias, program_current_size)


def jump_r(r_2bit=0, overflow=False, negative=False, zero=False, alias=''):
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
  elif overflow and not negative and not zero:
    inst += 0b00000001
  elif negative and not overflow and not zero:
    inst += 0b00000010
  elif zero and not overflow and not negative:
    inst += 0b00000011
  else:
    raise ValueError('jump_r can take only 1 flag')
  byte_add(inst)
  alias_add(alias, program_current_size)


def setr_c(r_2bit=0, num_4bit=0, alias=''):
  '''
  Set 2 bit number in register (mostly used to set value of reg to 0 or 1)
  '''
  inst = 0b01010000
  if not (0 <= num_4bit <= 15):
    raise ValueError('setr_c number argument must be from 0 to 15 included')
  register_validation(r_2bit, 'setr_c')
  inst += (r_2bit << 2) + num_4bit
  byte_add(inst)
  alias_add(alias, program_current_size)


def load_c(r_2bit=0, num_8bit=0, alias=''):
  '''
  Load number in register
  '''
  inst = 0b01100000
  if num_8bit != None and not (0 <= num_8bit <= 255):
    raise ValueError('load_c number argument must be from 0 to 255 included')
  register_validation(r_2bit, 'load_c')
  inst += (r_2bit << 2)
  byte_add(inst)
  alias_add(alias, program_current_size)
  byte_add(num_8bit)


def load_m(r_2bit=0, address_8bit=0, alias=''):
  '''
  Load number from memory cell location at address_8bit
  '''
  inst = 0b01110000
  if address_8bit != None and not (0 <= address_8bit <= 255):
    raise ValueError('load_m address argument must be from 0 to 255 included')
  register_validation(r_2bit, 'load_m')
  inst += (r_2bit << 2)
  byte_add(inst)
  alias_add(alias, program_current_size)
  byte_add(address_8bit)


def save_m(r_2bit=0, address_8bit=0, alias=''):
  '''
  Save value of register to memory cell location at address_8bit
  '''
  inst = 0b10000000
  if address_8bit != None and not (0 <= address_8bit <= 255):
    raise ValueError('save_m address argument must be from 0 to 255 included')
  register_validation(r_2bit, 'save_m')
  inst += (r_2bit << 2)
  byte_add(inst)
  alias_add(alias, program_current_size)
  byte_add(address_8bit)


def incr(r_2bit=0, negative=False, alias=''):
  '''
  Increment value of register. If contain flag negative - decrement.
  '''
  inst = 0b10010000
  register_validation(r_2bit, 'incr')
  inst += (r_2bit << 2)
  if negative:
    inst += 0b00000010
  byte_add(inst)
  alias_add(alias, program_current_size)


def halt(r_2bit=0, input_flag=False, alias=''):
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
  alias_add(alias, program_current_size)


__all__ = [
  'reg0', 'reg1', 'reg2', 'reg3',
  'idle', 'addr', 'subr', 'jump_c', 'jump_r', 'setr_c', 'load_c', 'load_m', 'save_m', 'incr', 'halt',
  'compile_vmem', 'get_program_current_size', 'get_binary_data', 'get_alias', 'get_all_aliases'
]