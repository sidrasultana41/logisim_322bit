# Simple IO
It writes 1 to 0x00007F00 and 0x00007F04 to turn on 2 LEDs
Uses lw, sw instructions
Please open:
simple_io.s
simple_io.circ

# Extra Credit for Project 2-2

This interesting IO converts 32-bit binary numbers to hex
and displays them on eight Hex Digit Displays.
Please open:
extra_hex_io.s
extra_hex_io.circ

This interesting IO reads ASCII characters (bits 0-6) from $s0
and displays corresponding characters on a screen.
Please open:
extra_tty_io.s
extra_tty_io.circ
