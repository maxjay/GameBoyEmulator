from memory import Memory
from binary import Bin16, Bin

class GPU():
	def __init__(self):
		self.memory = Memory()
		self.memory.load("a.dump")
		self.tile0 = self.memory[Bin16.fromHex("8000").toDecimal():Bin16.fromHex("8FFF").toDecimal()]
		self.tile1 = self.memory[Bin16.fromHex("8FFF").toDecimal():Bin16.fromHex("9FFF").toDecimal()]
		self.tileMap0 = self.memory[Bin16.fromHex("9800").toDecimal():Bin16.fromHex("9BFF").toDecimal()]
		self.tileMap1 = self.memory[Bin16.fromHex("9C00").toDecimal():Bin16.fromHex("9FFF").toDecimal()]
