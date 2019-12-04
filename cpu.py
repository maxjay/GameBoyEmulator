from binary import Bin
from memory import MemoryBus

class UnknownInstruction(Exception):
	def __init__(self, instruction, address):
		self.code = "Unknown Instruction: {0}     Address: {1}".format(instruction, address.toHex())

class CPU:
	def __init__(self):
		self.registers = {'A': Bin.hexToBin("01"),
						  'B': Bin.hexToBin("00"),
						  'C': Bin.hexToBin("13"),
						  'D': Bin.hexToBin("00"),
						  'E': Bin.hexToBin("D8"),
						  'F': Bin.hexToBin("B0"),
						  'H': Bin.hexToBin("01"),
						  'L': Bin.hexToBin("4D")}
		self.programCounter = Bin.hexToBin("0100")
		self.stackPointer = Bin.hexToBin("FFFE")
		self.updateFlagRegisters()
		self.bus = MemoryBus()

	def updateFlagRegisters(self):
		self.zeroFlag = self.registers["F"][7]
		self.opFlag = self.registers["F"][6]
		self.halfCarryFlag = self.registers["F"][5]
		self.carryFlag = self.registers["F"][4]
		self.flagRegister = self.registers["F"]

	def setZeroFlag(self, bit):
		self.registers["F"][8] = bit
		self.updateFlagRegisters()

	def setOpFlag(self, bit):
		self.registers["F"][7] = bit
		self.updateFlagRegisters()

	def setHalfCarryFlag(self, bit):
		self.registers["F"][6] = bit
		self.updateFlagRegisters()

	def setCarryFlag(self, bit):
		self.registers["F"][5] = bit
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
			self.setZeroFlag(Bin("1") if self.registers["A"] == Bin("0", 8) else Bin("0"))
			self.setOpFlag(Bin("0"))
			self.setCarryFlag(Bin("0"))
			self.setHalfCarryFlag(Bin("0"))
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
			self.setOpFlag(Bin("1"))
			self.setZeroFlag(Bin("1") if (self.get_HL()) == Bin("0", 16) else Bin("0"))
			self.setHalfCarryFlag(Bin("1") if ((self.get_HL() & Bin.hexToBin("0F")) - (Bin("1") & Bin.hexToBin("0F")))[15] == "1" else Bin ("0"))
			self.set_HL(self.get_HL() - 1)
			self.programCounter += 1
		elif hexCode == "2A":
			self.registers["A"] = self.get_HL()
			self.set_HL(self.get_HL() + 1)
			self.programCounter += 1
		elif hexCode == "05":
			self.setOpFlag(Bin("1"))
			self.setZeroFlag(Bin("1") if (self.registers["B"] - 1) == Bin("0", 8) else Bin("0"))
			self.setHalfCarryFlag(Bin("1") if ((self.registers["B"] & Bin.hexToBin("0F")) - (Bin("1") & Bin.hexToBin("0F")))[7] == "1" else Bin("0"))
			self.registers["B"] = self.registers["B"] - 1
			self.programCounter += 1
		elif hexCode == "20":
			in2 = self.bus[self.programCounter + 1]
			self.programCounter += 2
			if self.zeroFlag == Bin("0"):
				self.programCounter = Bin.signedAdd(self.programCounter, in2)
			else:
				self.programCounter += 2
		elif hexCode == "1D":
			self.setOpFlag(Bin("1"))
			self.setZeroFlag(Bin("1") if (self.registers["E"] - 1) == Bin("0", 8) else Bin("0"))
			self.setHalfCarryFlag(Bin("1") if ((self.registers["E"] & Bin.hexToBin("0F")) - (Bin("1") & Bin.hexToBin("0F")))[7] == "1" else Bin("0"))
			self.registers["E"] = self.registers["E"] - 1
			self.programCounter += 1
		elif hexCode == "0D":
			self.setOpFlag(Bin("1"))
			self.setZeroFlag(Bin("1") if (self.registers["C"] - 1) == Bin("0", 8) else Bin("0"))
			self.setHalfCarryFlag(Bin("1") if ((self.registers["C"] & Bin.hexToBin("0F")) - (Bin("1") & Bin.hexToBin("0F")))[7] == "1" else Bin("0"))
			self.registers["C"] = self.registers["C"] - 1
			self.programCounter += 1
		elif hexCode == "3E":
			in2 = self.bus[self.programCounter + 1]
			self.registers["A"] = in2
			self.programCounter += 2
		elif hexCode == "F3":
			#DisableInterrupts
			self.programCounter += 1
		elif hexCode == "E0":
			in2 = self.bus[self.programCounter + 1]
			self.bus[in2 + Bin.hexToBin("FF00")] = self.registers["A"]
			self.programCounter += 2
		elif hexCode == "F0":
			self.registers["A"] = self.bus[self.programCounter + 1]
			self.programCounter += 2
		elif hexCode == "FE":
			in2 = self.bus[self.programCounter + 1]
			self.setZeroFlag(Bin("1") if (self.registers["A"] == in2) else Bin("0"))
			self.setOpFlag(Bin("1"))
			self.setHalfCarryFlag(Bin("1") if ((self.registers["A"] & Bin.hexToBin("0F")) - (in2 & Bin.hexToBin("0F")))[7] == "1" else Bin("0"))
			self.setCarryFlag(Bin("1") if in2 > self.registers["A"] else Bin("0"))
			self.programCounter += 2
		elif hexCode == "36":
			in2 = self.bus[self.programCounter + 1]
			self.set_HL(in2)
			self.programCounter += 2
		elif hexCode == "EA":
			in2 = self.bus[self.programCounter + 1]
			in3 = self.bus[self.programCounter + 2]
			into = (in3 << 8) + in2
			self.bus[into] = self.registers["A"]
			self.programCounter += 3
		elif hexCode == "31":
			in2 = self.bus[self.programCounter + 1]
			in3 = self.bus[self.programCounter + 2]
			into = (in3 << 8) + in2
			self.stackPointer = into
			self.programCounter += 3
		elif hexCode == "21":
			in2 = self.bus[self.programCounter + 1]
			in3 = self.bus[self.programCounter + 2]
			into = (in3 << 8) + in2
			self.set_HL(into)
			self.programCounter += 3
		elif hexCode == "11":
			in2 = self.bus[self.programCounter + 1]
			in3 = self.bus[self.programCounter + 2]
			into = (in3 << 8) + in2
			self.set_DE(into)
			self.programCounter += 3
		elif hexCode == "01":
			in2 = self.bus[self.programCounter + 1]
			in3 = self.bus[self.programCounter + 2]
			into = (in3 << 8) + in2
			self.set_BC(into)
			self.programCounter += 3
		elif hexCode == "E2":
			into = Bin.hexToBin("FF00") + self.registers["C"]
			self.bus[into] = self.registers["A"]
			self.programCounter += 1
		elif hexCode == "F2":
			into = Bin.hexToBin("FF00") + self.registers["C"]
			self.registers["A"] = into
			self.programCounter += 1
		else:
			raise UnknownInstruction(hexCode, self.programCounter)

	def step(self):
		byte = self.bus[self.programCounter]
		print("Executing: {0}\tPC: {1}\tFlag Registers: {2}".format(byte.toHex(), self.programCounter.toHex(),self.flagRegister))
		self.execute(byte)
