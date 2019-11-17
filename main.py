from cpu import CPU
from binary import Bin

gameboy = CPU()
with open("game.gb", "rb") as game:
	byte = game.read(1)
	while byte != "":
		byte = Bin(' '.join(format(ord(x), 'b') for x in byte), 8)
		if byte.toHex() == "CB":
			byte2 = game.read(1)
			byte2 = Bin(' '.join(format(ord(x), 'b') for x in byte2), 8)
			gameboy.execute(byte, byte2)
		else:
			gameboy.execute(byte)
		byte = game.read(1)
