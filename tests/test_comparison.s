addi $s0, $zero, 1
addi $s1, $zero, -2
#signed set less than tests
slt $s2, $s0, $s1
slt $s2, $s1, $s0
#unsigned set less than tests
sltu $s2, $s1, $s0
sltu $s2, $s0, $s1
#unsigned set less than immediate tests
sltiu $s2, $s0, 0
sltiu $s2, $s1, 0
sltiu $s2, $s0, 2
sltiu $s2, $s1, 2
sltiu $s2, $s0, -3
sltiu $s2, $s1, -3
#signed set less than immediate tests
slti $s2, $s0, 0
slti $s2, $s1, 0
slti $s2, $s0, 2
slti $s2, $s1, 2
slti $s2, $s0, -3
slti $s2, $s1, -3