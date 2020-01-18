from binary import Bin
from binary import Bin16

class Register():
	def __init__(self):
		self.register = {"A": Bin.fromHex("00"),
						"B": Bin.fromHex("00"),
						"C": Bin.fromHex("00"),
						"D": Bin.fromHex("00"),
						"E": Bin.fromHex("00"),
						"F": Bin.fromHex("00"),
						"H": Bin.fromHex("00"),
						"L": Bin.fromHex("00")}

	def store(self, register, bin):
		if len(register) == 1:
			self.register[register] = bin
		else:
			self.register[register[0]] = bin.to8Bin()[0]
			self.register[register[1]] = bin.to8Bin()[1]


	def load(self, register):
		if len(register) == 1:
			return self.register[register]
		return Bin16(self.register[register[0]], self.register[register[1]])

class CPU():
	def __init__(self):
		self.register = Register()
		self.programCounter = Bin16.fromHex("0100")
		self.stackPointer = Bin16.fromHex("FFFE")

