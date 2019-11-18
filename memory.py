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

	def loadROM(self, file):
		with open(file, "rb") as file:
			byte = file.read(1)
			counter = 0
			while byte != "":
				byte = Bin(" ".join(format(ord(x), 'b') for x in byte), 8)
				self.memory[counter] = byte
				counter += 1
				byte = file.read(1)
