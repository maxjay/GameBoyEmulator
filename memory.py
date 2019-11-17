from binary import Bin

class MemoryBus():
	def __init__(self):
		self.memory = [Bin("0", 8)] * 65536

	def __getitem__(self, key):
		if isinstance(key, Bin):
			return self.memory[key.toDec()]
		else:
			return self.memory[key]

	def __setitem__(self, key, value):
		if isinstance(key, Bin):
			self.memory[key.toDec()] = value
		else:
			self.memory[key] = value
		return self.memory
