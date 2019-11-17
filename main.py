from cpu import CPU
from binary import Bin

with open("game.gb", "rb") as game:
	byte = game.read(1)
	while byte != "":
		byte = Bin(' '.join(format(ord(x), 'b') for x in byte), 8)
		print(byte)
		byte = game.read(1)
