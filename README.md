# mima_emu

This is a simple emulator for mima code.

To use it just paste your instructions inside the asm variable. You can use any seperator you like between the instructions.

asm = 	""" LDC 0,
			STV y,
			LABEL while,
			LDC 0,
			NOT,
			ADD x,
			JMN end,
			LDC 0,
			NOT,
			ADD x,
			AND x,
			STV x,
			LDC 1,
			ADD y,
			STV y,
			JMP while,
			LABEL end,
			HALT"""

You only need to change the label naming from "loop:" to "LABEL loop".
The memory is stored in a dictionary. You can add your own addresses and values.

memory = Memory({
	'addr1':	12345,
	'y':		0,
	'add42':	42,
	})


The instruction set is not complete!
Supported are the following:
AND, LDC, ADD, LDV, STV, EQL, NOT, JMP, JMN, HALT
