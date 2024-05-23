j first

fourth:
add $s1, $s0, $s1
jal fifth
j last

second:
addiu $s1, $s0, 6
jr $ra

fifth:
add $s1, $s0, $s1
jr $ra

first:
addi $s0, $zero, 5
jal second

third:
add $s1, $s0, $s1
j fourth

last:
addi $s1,$s1,-26
addi $s0,$s0,-5