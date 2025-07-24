from i10b8compiler import *

# Calculate first 13 fibonacci numbers

setr_c(reg3, 0)
incr(reg3) # clear register and alu
halt(reg3, input_flag=True) # input from 0 to 13

# if input 0
setr_c(reg0, 0)
incr(reg3, negative=True)
load_c(reg2, get_alias('display_reg0'))
jump_r(reg2, negative=True)

# if input 1
setr_c(reg1, 1)
load_c(reg2, get_alias('display_reg1'))
jump_r(reg2, zero=True)

# @main_cycle
addr(reg0, reg1, alias='main_cycle')
incr(reg3, negative=True)
load_c(reg2, get_alias('display_reg0'))
jump_r(reg2, zero=True)

addr(reg1, reg0)
incr(reg3, negative=True)
load_c(reg2, get_alias('display_reg1'))
jump_r(reg2, zero=True)

load_c(reg2, get_alias('main_cycle'))
jump_r(reg2)

# @display_reg0
halt(reg0, alias='display_reg0')
jump_c(0)

# @display_reg1
halt(reg1, alias='display_reg1')
jump_c(0)

compile_vmem('i10-b8')