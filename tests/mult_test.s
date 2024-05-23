ori $s0, $zero 50
ori $s1, $zero 200

mult $s0, $s1
mflo $s2

mult $s0, $s2
mflo $s2

mult $s1, $s2
mflo $s2

mult $s1, $s2
mfhi $s1
mflo $s2

add $s0, $zero, -20

mult $s1,$s0
mfhi $s1
mflo $s2
