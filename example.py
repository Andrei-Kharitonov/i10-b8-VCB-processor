from i10b8compiler import * # import instructions

# This program display sum of 2 numbers

load_c(reg0, 25) # write number 25 in register0
load_c(reg1, 17) # write number 17 in register1
addr(reg0, reg1) # add value of register1 to register0 and wirte result to register0
halt(reg0) # display 42
jump_c(0) # return to start of program

compile_vmem('i10-b8') # compile program