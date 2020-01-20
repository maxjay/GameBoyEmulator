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

	def __setitem__(self, key, value):
		return self.store(key, value)

	def __getitem__(self, key):
		return self.load(key)

	def store(self, register, bin):
		if len(register) == 1:
			self.register[register] = bin
		else:
			if type(bin) == Bin16:
				self.register[register[0]] = bin.to8Bin()[0]
				self.register[register[1]] = bin.to8Bin()[1]
			else:
				self.register[register[0]] = Bin()
				self.register[register[1]] = bin

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

	def decode(self, ins):
		print(ins.toHex())
		if ins.toHex() == "31":
			ins2 = self.fetch()
			ins3 = self.fetch()
			self.stackPointer = Bin16(ins3, ins2)
		elif ins.toHex() == "AF":
			self.register["A"] = self.register["A"] ^ self.register["A"]
			self.register["F"][7] = 1 if self.register["A"] == Bin() else 0
			#I FORGOT THE FLAGS
		elif ins.toHex() == "21":
			ins2 = self.fetch()
			ins3 = self.fetch()
			self.register["HL"] = Bin16(ins3, ins2)
		elif ins.toHex() == "32":
			self.register["HL"] = self.register["A"]
			self.register["HL"] += -1
		elif ins.toHex() == "CB":
			ins2 = self.fetch()
			if ins2.toHex() == "7C": #test bit 7 in register C
				self.register["F"][7] = 1 if self.register["C"][7] == 0 else 0
				self.register["F"][5] = 1
			else:
				print("CB", ins2.toHex())
		elif ins.toHex() == "20":
			ins2 = self.fetch()
			if not self.register["F"][7]:
				self.programCounter += ins2
		elif ins.toHex() == "0E":
			ins2 = self.fetch()
			self.register["C"] = ins2
		elif ins.toHex() == "3E":
			ins2 = self.fetch()
			self.register["A"] = ins2
		elif ins.toHex() == "E2":
			self.memoryBus[Bin16.fromHex("FF00") + self.register["C"]] = self.register["A"]
		elif ins.toHex() == "0C":
			self.register["C"] += 1
		elif ins.toHex() == "77":
			self.register["HL"] = Bin16(Bin(), self.register["A"])
		elif ins.toHex() == "E0":
			ins2 = self.fetch()
			self.memoryBus[Bin16.fromHex("FF00") + ins2] = self.register["A"]
		elif ins.toHex() == "11":
			ins2 = self.fetch()
			ins3 = self.fetch()
			self.register["DE"] = Bin16(ins3, ins2)
		elif ins.toHex() == "1A":
			self.register["A"] = self.memoryBus[self.register["DE"]]
		elif ins.toHex() == "CD":
			pass
		else:
			exit()

	def execute(self):
		pass

	def boot(self):
		while self.programCounter != Bin16.fromHex("0100"):
			ins = self.fetch()
			self.decode(ins)
		print(self.programCounter, self.programCounter.toHex())
