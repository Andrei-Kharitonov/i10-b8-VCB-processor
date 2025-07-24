from i10b8compiler import *

# This program display number > 100

load_c(reg0, 5)
load_c(reg1, 40, alias='my_alias')
load_c(reg2, 100)
addr(reg0, reg1)
subr(reg2, reg0)
load_c(reg3, get_alias('end')) # aliases can be declarated in any part of program before compile_vmem()
jump_r(reg3, negative=True) # jump to the end if number in reg0 > 100
jump_c(get_alias('my_alias')) # jump to function that contain alias 'my_alias'

halt(reg0, alias='end')

compile_vmem('i10-b8')