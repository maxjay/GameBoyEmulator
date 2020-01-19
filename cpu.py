from binary import Bin
from binary import Bin16

class Instruction(): #Maybe?
	def __init__(self, opcode, arg1=None, arg2=None):
		self.opcode = opcode
		self.arg1 = arg1
		self.arg2 = arg2

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
	def __init__(self, Memory):
		self.register = Register()
		self.programCounter = Bin16.fromHex("0000")
		self.stackPointer = Bin16.fromHex("0000")
		self.memoryBus = Memory

	def load(self, register):
		return self.register.load(register)

	def store(self, register, bin):
		return self.register.store(register, bin)

	def fetch(self):
		instru = self.memoryBus[self.programCounter]
		self.programCounter += 1
		return instru

	def execute(self):
		pass

	def boot(self):
		while self.programCounter != Bin16.fromDecimal(100):
			print(self.fetch().toHex())
