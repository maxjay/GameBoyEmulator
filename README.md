"# GameBoyEmulator written in Python" 

This is a program to emulate the DMG Gameboy...

CPU Design:
The cpu utilises a fetch-decode-execution loop style.
	-	An instruction is fetched from the memory at the address of the program counter
	-	The program counter is then incremented
	-	Instruction is decoded
	-	Instruction is executed


CPU Registers:
REGISTER		PURPOSE			16Bit
A				ACCUMULATOR		AF
F				STATUS FLAGS	AF
B				GP REGISTER		BC
C				COUNTER			BC
D				GP REGISTER		DE
E				GP REGISTER		DE
H				POINTER			HL
L				POINTER			HL
SP				STACK POINTER	-
PC				PROGRAM COUNTER	-

Flags:
FLAG			BIT POS			DESC
Z				7				ZERO FLAG (IF RESULT == 0: 1)
S				6				SUBTRACTION FLAG (IF OP == SUB: 1)				
H				5				HALF CARRY FLAG (IF CARRY FROM BIT 3 TO 4: 1)
C				4				CARRY FLAG (IF CARRY FROM BIT 7: 1) [OVERFLOW]



Memory Config:
	-	0x000 - 0x7FFF		: Program Data
		-	0x000 - 0x0FF	: Destination Address for RTS instructions and interrupts
		-	0x100 - 0x14F	: ROM area for storing data such as name of game
		-	0x150			: Starting address of user program
	-	0x8000 - 0x9FFF		: RAM for LCD display (8KBytes VRAM)
	-	0xA000 - 0xBFFF		: External expansion RAM
	-	0xC000 - 0xDFFF		: Work RAM area (8KB RAM)
	-	0xFE00 - 0xFFFF		: Internal CPU RAM
		-	0xFE00 - 0xFE9F	: OAM-RAM (Display data for 40 objects)
		-	0xFF00 - 0xFF7F	: Port Registers/Control Registers/Sound Registers
		-	0xFF80 - 0xFFFE	: CPU working and stack RAM (127 bytes RAM)

Register Config:
USE				REGISTER			ADDRESS
PORT/MODE		P1					0xFF00	
				SB					0xFF01
				SC					0xFF02
				DIV					0xFF04
				TIMA				0xFF05
				TMA					0xFF06
				TAC					0xFF07
INTERRUPT FLAG	IF					0xFF0F	
				IE					0xFFFF
				IME					------
LCD DISPLAY		LCDC				0xFF40
				STAT				0xFF41
				SCY					0xFF42
				SCX					0xFF43
				LY					0xFF44
				LYC					0xFF45
				DMA					0xFF46
				BGP					0xFF47
				OBP0				0xFF48
				OBP1				0xFF49
				WY					0xFF4A
				WX					0xFF4B
				OAM					0xFE00 - 0xFE9F
SOUND			NR X X				0xFF10 - 0xFF26
				WAVEFORM RAM		0xFF30 - 0xFF3F


Subjectively, Python doesn't have a nice builtin binary library. So I'll write on myself
Binary will be sorted as an 8 bit array of 1 and 0 in Big Endian:

INDEX |	7 | 6 | 5 | 4 | 3 | 2 | 1 | 0
=====================================
VALUE | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0

However will be displayed and interrupted (outside of class methods) as strings:
"111001010"

This is because leading zeros are not stored in python and thus 00001111 becomes 1111

All functions that return a result, excluding decimal and hex conversions, will return
a class of itself. If a specific bit is requested, a binary class representing that bit
is returned. 

This library is extended to 16 bit with the class Bin16()
