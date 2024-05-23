addi $s0, $zero, 1
addi $s1, $zero, 1

beq $s0, $s1, one 	#should branch to one
bne $s0, $s1, wrong #this should not branch

one:
addi $s0, $s0, 1
beq $s0, $s1, wrong	#this should not branch
bne $s0, $s1, two  	#should branch to two

three:
j finish

two: 
addi $s1, $s1, 1
beq $s0, $s1, three	#should branch backwards to three
bne $s0, $s1, wrong #this should not branch

wrong: 
addi $s0, $zero, -1
addi $s1, $zero, -1
addi $s2, $zero, -1

finish:
