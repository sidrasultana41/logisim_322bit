addi $s0, $zero, 1  #s0 = 0x1 (+,+)
addiu $s1, $zero, 2 #s1 = 0x2 (+,+)
addu $s2, $s0, $s1  #s2 = 0x3 (+,+)
add $s0,$s2,$s1     #s0 = 0x5 (+,+)

addi $s0, $s1, -3  #s0 = 0xFFFFFFFF (+,-)
addiu $s2, $s0, -4 #s2 = 0xFFFFFFFB (+,-)
addu $s0, $s1, $s2 #s0 = 0xFFFFFFFD (+,-)
add $s1, $s1, $s2  #s1 = 0xFFFFFFFD (+,-)

addi $s1, $s0, -5  #s1 = 0xFFFFFFF8 (-,-)
addiu $s0, $s2, -6 #s0 = 0xFFFFFFF5 (-,-)
addu $s2, $s0, $s1 #s2 = 0xFFFFFFED (-,-)
add $s0, $s1, $s2  #s0 = 0xFFFFFFE5 (-,-)