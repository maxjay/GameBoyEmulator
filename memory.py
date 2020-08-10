from binary import Bin
from binary import Bin16
import numpy

class Memory():
	def __init__(self):
		self.memory = [Bin() for i in range(65536)]

	def __getitem__(self, key):
		if isinstance(key, Bin16):
			return self.memory[key.toDecimal()]
		else:
			if isinstance(key, str):
				return self.memory[Bin16.fromHex(key).toDecimal()]
			else:
				return self.memory[key]

	def __setitem__(self, key, value):
		if isinstance(key, Bin16):
			self.memory[key.toDecimal()].array = value.array
		else:
			self.memory[key].array = value.array

	def load(self, file):
		with open(file, "rb") as file:
			byte = file.read(1)
			counter = 0
			while len(byte) != 0:
				byte = Bin.fromDecimal(ord(byte))
				self.memory[counter] = byte
				counter += 1
				byte = file.read(1)

	def saveDump(self):
		with open("dump.hex", "wb+") as file:
			file.write(bytearray([i.toDecimal() for i in self.memory]))

class MemoryBus(Memory):
	def __init__(self, memory):
		self.memory = memory

if __name__ == "__main__":
	a = Memory()
	a.loadROM("game.gb")
	a.getROM()
