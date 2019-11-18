from binary import Bin
from memory import MemoryBus

class UnknownInstruction(Exception):
	def __init__(self, instruction, address):
		self.code = "Unknown Instruction: {0}     Address: {1}".format(instruction, address.toHex())

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
		self.programCounter = Bin.hexToBin("0100")
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

	def pushToStack(self, bin_):
		self.bus[self.stackPointer] = bin_
		self.stackPointer += 1

	def execute(self, instruction):
		hexCode = instruction.toHex()
		if hexCode == "00":
			self.programCounter += 1
		elif hexCode == "C3":
			in2	= self.bus[self.programCounter + 1]
			in3 = self.bus[self.programCounter + 2]
			jumpTo = (in3 << 8) + in2
			self.programCounter = jumpTo
		elif hexCode == "0C":
			self.registers["C"] += 1
			self.programCounter += 1
		elif hexCode == "02":
			self.set_BC(self.registers["A"])
			self.programCounter += 1
		elif hexCode == "CD":
			in2 = self.bus[self.programCounter + 1]
			in3 = self.bus[self.programCounter + 2]
			callTo = (in3 << 8) + in2
			self.pushToStack(callTo)
			self.programCounter = callTo
		elif hexCode == "AF":
			self.registers["A"] = self.registers["A"] ^ self.registers["A"]
			self.programCounter += 1
		elif hexCode == "21":
			in2 = self.bus[self.programCounter + 1]
			in3 = self.bus[self.programCounter + 2]
			self.set_HL((in3 << 8) + in2)
			self.programCounter += 3
		elif hexCode == "0E":
			in2 = self.bus[self.programCounter + 1]
			self.registers["C"] = in2
			self.programCounter += 2
		elif hexCode == "06":
			in2 = self.bus[self.programCounter + 1]
			self.registers["B"]	= in2
			self.programCounter += 2
		elif hexCode == "32":
			self.set_HL(self.registers["A"])
			self.zeroFlag = Bin("1") if self.get_HL - 1 == Bin("0") else Bin("0")
			#Add subtract method, get carry for half nibble?
		else:
			raise UnknownInstruction(hexCode, self.programCounter)

	def step(self):
		byte = self.bus[self.programCounter]
		self.execute(byte)
