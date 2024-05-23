# iotest.s
# writes 1 to 0x00007F00 and 0x00007F04 to turn on 2 LEDs

addiu $t0, $zero, 1
addiu $t1, $zero, 0x00007F00

sw $t0, 0($t1)
sw $t0, 4($t1)

lw $s0, 0($t1)
lw $s1, 4($t1)
