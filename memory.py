from binary import Bin
from binary import Bin16

class Memory():
	def __init__(self):
		self.memory = [Bin()] * 65536

	def __getitem__(self, key):
		if isinstance(key, Bin16):
			return self.memory[key.toDecimal()]
		else:
			return self.memory[key]

	def __setitem__(self, key, value):
		if isinstance(key, Bin16):
			self.memory[key.toDecimal()] = value
		else:
			self.memory[key] = value
		return self.memory

	def getROM(self):
		temp = Memory()
		temp.memory = self.memory[:32767+1]
		return temp

	def load(self, file):
		with open(file, "rb") as file:
			byte = file.read(1)
			counter = 0
			while len(byte) != 0:
				byte = Bin.fromDecimal(ord(byte))
				self.memory[counter] = byte
				counter += 1
				byte = file.read(1)

class MemoryBus(Memory):
	def __init__(self, memory):
		self.memory = memory

if __name__ == "__main__":
	a = Memory()
	a.loadROM("game.gb")
	a.getROM()
