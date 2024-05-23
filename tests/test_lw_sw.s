addi $s0, $zero, 0x2004

addi $s1, $zero, 5

sw $s1, 0($s0)
sw $s1, 4($s0)

lw $s2, 0($s0)

addi $s2, $s1, 5

sw $s2, 4($s0)
sw $s2, 0($s0)

sw $zero, 0($s0)
sw $zero, 4($s0)
