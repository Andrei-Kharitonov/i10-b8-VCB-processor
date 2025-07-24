from i10b8compiler import *

# Calculate first 13 fibonacci numbers

display_reg0 = 23 # address to display reg0
display_reg1 = 25 # address to display reg1
main_cycle = 10 # address of start of main cycle

halt(reg3, input_flag=True) # input from 0 to 13

# input 0
setr_c(reg0, 0)
incr(reg3, negative=True)
load_c(reg2, display_reg0)
jump_r(reg2, negative=True)

# input 1
setr_c(reg1, 1)
load_c(reg2, display_reg1)
jump_r(reg2, zero=True)

# @main_cycle
addr(reg0, reg1)
incr(reg3, negative=True)
load_c(reg2, display_reg0)
jump_r(reg2, zero=True)

addr(reg1, reg0)
incr(reg3, negative=True)
load_c(reg2, display_reg1)
jump_r(reg2, zero=True)

load_c(reg2, main_cycle)
jump_r(reg2)

# @display_reg0
halt(reg0)
jump_c(0)
# @display_reg1
halt(reg1)
jump_c(0)

compile_vmem('i10-b8')