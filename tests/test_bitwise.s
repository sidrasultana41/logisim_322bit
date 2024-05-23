addi $s0, $zero, 0
addi $s1, $s0, 1

and $s2, $s0, $s1

bne $s2, 0, wrong

or $s2, $s0, $s1

beq $s2, 0, wrong

andi $s2, $s1, 1

beq $s2, 0, wrong

ori $s2, $s0, 0

bne $s2, 0, wrong

beq $s2, 0, finish

wrong:

addi $s0, $zero, -1
addi $s1, $zero, -1
addi $s2, $zero, -1

finish:
