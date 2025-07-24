from i10b8compiler import *

# this program display sum of 2 numbers
load_c(reg0, 25)
load_c(reg1, 17)
addr(reg0, reg1)
halt(reg0) # display 42
jump_c(0)

compile_vmem('i10-b8')