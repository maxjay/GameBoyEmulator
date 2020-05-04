from cpu import CPU
from memory import Memory, MemoryBus

class GameBoy():
	def __init__(self):
		self.memory = Memory()
		self.cpu = CPU(self.memory)

	def boot(self):
		self.memory.load("04-op r,imm.gb")
		self.cpu.debug()

if __name__ == "__main__":
	a = GameBoy()
	a.boot()
