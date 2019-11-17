from binary import Bin
from memory import MemoryBus

class CPU:
	def __init__(self):
		self.registers = {'A': Bin("000000000"),
						  'B': Bin("000000000"),
						  'C': Bin("000000000"),
						  'D': Bin("000000000"),
						  'E': Bin("000000000"),
						  'F': Bin("000000000"),
						  'H': Bin("000000000"),
						  'L': Bin("000000000")}
		self.programCounter = Bin("0000000000000000")
		self.stackPointer = Bin.hexToBin("FFFE")
		self.updateFlagRegisters()
		self.bus = MemoryBus()

	def updateFlagRegisters(self):
		self.flagRegister = self.registers["F"]
		self.zeroFlag = self.registers["F"][7]
		self.opFlag = self.registers["F"][6]
		self.halfCarryFlag = self.registers["F"][5]
		self.carryFlag = self.registers["F"][4]

	def setZeroFlag(self, bit):
		self.registers["F"][7] = bit
		self.updateFlagRegisters()

	def setOpFlag(self, bit):
		self.registers["F"][6] = bit
		self.updateFlagRegisters()

	def setHalfCarryFlag(self, bit):
		self.registers["F"][5] = bit
		self.updateFlagRegisters()

	def setCarryFlag(self, bit):
		self.registers["F"][4] = bit
		self.updateFlagRegisters()

	def set_AF(self, bin_):
		self.registers["A"] = bin_[:8]
		self.registers["F"] = bin_[8:]
		self.updateFlagRegisters()

	def set_BC(self, bin_):
		self.registers["B"] = bin_[:8]
		self.registers["C"] = bin_[8:]

	def set_DE(self, bin_):
		self.registers["D"] = bin_[:8]
		self.registers["E"] = bin_[8:]

	def set_HL(self, bin_):
		self.registers["H"] = bin_[:8]
		self.registers["L"] = bin_[8:]

	def get_AF(self):
		return (self.registers["A"] << 8) + self.registers["F"]

	def get_BC(self):
		return (self.registers["B"] << 8) + self.registers["C"]

	def get_DE(self):
		return (self.registers["D"] << 8) + self.registers["E"]

	def get_HL(self):
		return (self.registers["H"] << 8) + self.registers["L"]

	def execute(self, instruction, instruction2=None):
		pass
