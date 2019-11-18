from cpu import CPU
from binary import Bin

gameboy = CPU()
gameboy.bus.loadROM("game.gb")
steps = 0
try:
	while True:
		gameboy.step()
		steps += 1
except Exception as e:
	print(e)
	print(e.code, "Steps: {0}".format(steps))
