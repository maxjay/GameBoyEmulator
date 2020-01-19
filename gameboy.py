from cpu import CPU
from memory import Memory, MemoryBus

class GameBoy():
	def __init__(self):
		self.memory = Memory()
		self.cpu = CPU(self.memory)

	def boot(self):
		self.memory.load("boot.bin")
		self.cpu.boot()
