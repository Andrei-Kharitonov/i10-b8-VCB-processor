# 10i-8b processor
10i-8b is my simple custom 8 bit processor developed in game **Virtual Circuit Board**.
It has 255 byte of memory, 4 registers and 10 simple instructions.
There is also simple compiler written on python that can convert instructions into VCB Vmem file for uploading in the game.
I developed this processor to better understand how it works almost without any knowledge, so it can't do a lot of things. But I had a lot of fun by doing this.
![i10-b8-processor.png](/img/i10-b8-processor.png)

## Processor cycle
Each 128 ticks counter increments and send signal to fetch next instruction from memory. Instruction writes down into instruction register (IR). Then instruction and its arguments decode and executes.

## Instructions
List of available instructions and arguments they take.
* ```[00]``` mean this 2 bit can take different values
* ```--``` mean this 2 bit doesn't affect at the instruction

```
idle       NA
0000       ----

addr       reg       reg
0001       [00]      [00]

subr       reg       reg
0010       [00]      [00]

jump_c     const
0011       [0000]

jump_r     reg       flags_[d/o/n/z]
0100       [00]      [00]

setr_c     reg       const
0101       [00]      [00]

load_c     reg       const
0110       [00]--    [00000000]

load_m     reg       mem
0111       [00]--    [00000000]

save_m     reg       mem
1000       [00]--    [00000000]

incr       reg       neg
1001       [00]      [0]-

halt       reg       input
1111       [00]      [0]-
```

## Instructions decscription
**```idle()```** - do nothing, but needs for propper processor work

**```addr(register_1, register_2)```** - take 2 register addresses as arguments, then write sum of their values in register_1

**```subr(register_1, register_2)```** - take 2 register addresses as arguments, then subtract vaulue of register_2 from value of register_1 and write result in register_1

**```jump_c(number)```** - set current memory address to a 4 bit number + 1 in argument

**```jump_r(register, [overflow, negative, zero])```** - set current memory address to a vaule of register + 1. Contain facultative condition flags: overflow - make jump_r only if result of last math operation cause overflow; negative - make jump_r only if result of last math operation was negative; zero - make jump_r only if result of last math operation was zero.

**```set_c(register, number)```** - set 2 bit number in register (mostly used to set value of reg to 0 or 1)

**```load_c(register, number)```** - load number in register

**```load_m(register, memory_address)```** - load number from memory cell location at memory_address

**```save_m(register, memory_address)```** - save value of register to memory cell location at memory_address

**```incr(register, [negative])```** - increment value of register. If contain flag negative - decrement.

**```halt(register, [input_flag])```** - stops program execution and display value of register untill "continue" button press. If has input_flag - doesn't display value. Instead of this it write value from input when "continue" button pressed into register.

### 2 byte instructions
Instructions **load_c**, **load_m** and **save_m** take up 2 byte. This is detailed explanation of how it works.

Fetch and Execute **load_c**:
1. load instruction and decode
2. send signal: write disable IR, counter++
3. write enable register
4. write data into register during fetch
5. write disable register
6. write enable IR

Fetch and Execute **load_m** and **save_m**:
1. load instruction and decode
2. send signal: write enable AR, write disable IR, counter++ 
3. write data into AR during fetch
4. write disable AR, write enable IR
5. read enable AR
6. read/write enable memory 
7. write/read enable register
8. read/write disable memory 
9. write/read disable register
10. disable read AR

## Compiler
To use compiler create .py file and importing all from i10b8compiler.py
``` py
from i10b8compiler import *
```
Use imported functions to write programs. For example:
``` py
load_c(reg0, 25) # load 25 in register 0
halt(reg0) # display 25
```
Write ```compile_vmem('i10-b8')``` at the end of program and run this file to compile binary file .vcbmem.
To enable external .vcbmem files in VCB project open Vmem editor in the game and click on the arrows at left bottom corner.