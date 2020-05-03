from binary import Bin
from binary import Bin16
from memory import *

class CPU():
	programCounter = Bin16.fromHex("0000")
	A = Bin.fromHex("00")
	B = Bin.fromHex("00")
	C = Bin.fromHex("00")
	D = Bin.fromHex("00")
	E = Bin.fromHex("00")
	F = Bin.fromHex("00")
	H = Bin.fromHex("00")
	L = Bin.fromHex("00")

	def __setattr__(self, name, value):
		if isinstance(value, Bin):
			super().__getattribute__(name).array = value.array
		elif isinstance(value, Bin16):
			a,b = value.array[0], value.array[1]
			if name == "AF":
				self.__setattr__("A", a)
				self.__setattr__("F", b)
			elif name == "BC":
				self.__setattr__("B", a)
				self.__setattr__("C", b)
			elif name == "DE":
				self.__setattr__("D", a)
				self.__setattr__("E", b)
			elif name == "HL":
				self.__setattr__("H", a)
				self.__setattr__("L", b)

	def __getattribute__(self, name):
		if name == "AF":
			return Bin16(super().__getattribute__("A"), super().__getattribute__("F"))
		elif name == "BC":
			return Bin16(super().__getattribute__("B"), super().__getattribute__("C"))
		elif name == "DE":
			return Bin16(super().__getattribute__("D"), super().__getattribute__("E"))
		elif name == "HL":
			return Bin16(super().__getattribute__("H"), super().__getattribute__("L"))
		return super().__getattribute__(name)

	def __init__(self, Memory=None):
		self.memoryBus = Memory

	def reg(self, key):
		return self.register[key]

	def read(self, address):
		if isinstance(address, Bin):
			address = Bin16(Bin.fromHex("FF"), address)
		return self.memoryBus[address]

	def write(self, address, value):
		if isinstance(address, Bin):
			address = Bin16(Bin.fromHex("FF"), address)
		self.memoryBus[address] = value

	def fetch(self):
		instru = self.memoryBus[self.programCounter]
		self.programCounter += 1
		return instru

	def fetch16(self):
		least = self.fetch()
		most = self.fetch()
		return Bin16(most, least)

	def execute(self, opcode):
		print(opcode)
		#8 bit opcodes
		if opcode == "06":	#LOAD n into B
			self.A = self.fetch()
		elif opcode == "0E":	#LOAD n into C
			self.C = self.fetch()
		elif opcode == "16":	#LOAD n into D
			self.D = self.fetch()
		elif opcode == "1E":	#LOAD n into E
			self.E = self.fetch()
		elif opcode == "26":	#LOAD n into H
			self.H = self.fetch()
		elif opcode == "2E":	#LOAD n into L
			self.L = self.fetch()
		elif opcode == "78":	#LOAD into A data from absolute address in B
			self.A = self.read(self.B)
		elif opcode == "79":	#LOAD into A data from absolute address in C
			self.A = self.read(self.C)
		elif opcode == "7A":	#LOAD into A data from absolute address in D
			self.A = self.read(self.D)
		elif opcode == "7B":	#LOAD into A data from absolute address in E
			self.A = self.read(self.E)
		elif opcode == "7C":	#LOAD into A data from absolute address in H
			self.A = self.H
		elif opcode == "7D":	#LOAD into A data from absolute address in L
			self.A = self.L
		elif opcode == "7E":	#LOAD into A data from absolute address in HL
			self.A = self.HL
		elif opcode == "7F":	#LOAD into A data from absolute address in A
			self.A = self.A
		elif opcode == "40":	#LOAD into B data from absolute address in B
			self.B = self.B
		elif opcode == "41":	#LOAD into B data from absolute address in C
			self.B = self.C
		elif opcode == "42":	#LOAD into B data from absolute address in D
			self.B = self.D
		elif opcode == "43":	#LOAD into B data from absolute address in E
			self.B = self.E
		elif opcode == "44":	#LOAD into B data from absolute address in H
			self.B = self.H
		elif opcode == "45":	#LOAD into B data from absolute address in L
			self.B = self.L
		elif opcode == "46":	#LOAD into B data from absolute address in HL
			self.B = self.read(self.HL)
		elif opcode == "47":	#LOAD into B data from absolute address in A
			self.B = self.read(self.A)
		elif opcode == "48":	#LOAD into C data from absolute address in B
			self.C = self.read(self.B)
		elif opcode == "49":	#LOAD into C data from absolute address in C
			self.C = self.read(self.C)
		elif opcode == "4A":	#LOAD into C data from absolute address in D
			self.C = self.read(self.D)
		elif opcode == "4B":	#LOAD into C data from absolute address in E
			self.C = self.read(self.E)
		elif opcode == "4C":	#LOAD into C data from absolute address in H
			self.C = self.read(self.H)
		elif opcode == "4D":	#LOAD into C data from absolute address in L
			self.C = self.read(self.L)
		elif opcode == "4E":	#LOAD into C data from absolute address in HL
			self.C = self.read(self.HL)
		elif opcode == "4F":	#LOAD into C data from absolute address in A
			self.C = self.read(self.A)
		elif opcode == "50":	#LOAD into D data from absolute address in B
			self.D = self.read(self.B)
		elif opcode == "51":	#LOAD into D data from absolute address in C
			self.D = self.read(self.C)
		elif opcode == "52":	#LOAD into D data from absolute address in D
			self.D = self.read(self.D)
		elif opcode == "53":	#LOAD into D data from absolute address in E
			self.D = self.read(self.E)
		elif opcode == "54":	#LOAD into D data from absolute address in H
			self.D = self.read(self.H)
		elif opcode == "55":	#LOAD into D data from absolute address in L
			self.D = self.read(self.L)
		elif opcode == "56":	#LOAD into D data from absolute address in HL
			self.D = self.read(self.HL)
		elif opcode == "57":	#LOAD into D data from absolute address in A
			self.D = self.read(self.A)
		elif opcode == "58":	#LOAD into E data from absolute address in B
			self.E = self.read(self.B)
		elif opcode == "59":	#LOAD into E data from absolute address in C
			self.E = self.read(self.C)
		elif opcode == "5A":	#LOAD into E data from absolute address in D
			self.E = self.read(self.D)
		elif opcode == "5B":	#LOAD into E data from absolute address in E
			self.E = self.read(self.E)
		elif opcode == "5C":	#LOAD into E data from absolute address in H
			self.E = self.read(self.H)
		elif opcode == "5D":	#LOAD into E data from absolute address in L
			self.E = self.read(self.L)
		elif opcode == "5E":	#LOAD into E data from absolute address in HL
			self.E = self.read(self.HL)
		elif opcode == "5F":	#LOAD into E data from absolute address in A
			self.E = self.read(self.A)
		elif opcode == "60":	#LOAD into H data from absolute address in B
			self.H = self.read(self.B)
		elif opcode == "61":	#LOAD into H data from absolute address in C
			self.H = self.read(self.C)
		elif opcode == "62":	#LOAD into H data from absolute address in D
			self.H = self.read(self.D)
		elif opcode == "63":	#LOAD into H data from absolute address in E
			self.H = self.read(self.E)
		elif opcode == "64":	#LOAD into H data from absolute address in H
			self.H = self.read(self.H)
		elif opcode == "65":	#LOAD into H data from absolute address in L
			self.H = self.read(self.L)
		elif opcode == "66":	#LOAD into H data from absolute address in HL
			self.H = self.read(self.HL)
		elif opcode == "67":	#LOAD into H data from absolute address in A
			self.H = self.read(self.A)
		elif opcode == "68":	#LOAD into L data from absolute address in B
			self.L = self.read(self.B)
		elif opcode == "69":	#LOAD into L data from absolute address in C
			self.L = self.read(self.C)
		elif opcode == "6A":	#LOAD into L data from absolute address in D
			self.L = self.read(self.D)
		elif opcode == "6B":	#LOAD into L data from absolute address in E
			self.L = self.read(self.E)
		elif opcode == "6C":	#LOAD into L data from absolute address in H
			self.L = self.read(self.H)
		elif opcode == "6D":	#LOAD into L data from absolute address in L
			self.L = self.read(self.L)
		elif opcode == "6E":	#LOAD into L data from absolute address in HL
			self.L = self.read(self.HL)
		elif opcode == "6F":	#LOAD into L data from absolute address in A
			self.L = self.read(self.A)
		elif opcode == "70":	#LOAD into address specified by HL, data from B
			self.write(self.HL, self.B)
		elif opcode == "71":	#LOAD into address specified by HL, data from C
			self.write(self.HL, self.C)
		elif opcode == "72":	#LOAD into address specified by HL, data from D
			self.write(self.HL, self.D)
		elif opcode == "73":	#LOAD into address specified by HL, data from E
			self.write(self.HL, self.E)
		elif opcode == "74":	#LOAD into address specified by HL, data from H
			self.write(self.HL, self.H)
		elif opcode == "75":	#LOAD into address specified by HL, data from L
			self.write(self.HL, self.L)
		elif opcode == "36":	#LOAD into address specified by HL, data from n
			self.write(self.HL, self.fetch())
		elif opcode == "0A":	#LOAD into A data from absolute address in BC
			self.A = self.read(self.BC)
		elif opcode == "1A":	#LOAD into A data from absolute address in DE
			self.A = self.read(self.DE)
		elif opcode == "7E":	#LOAD into A data from absolute address in HL
			self.A = self.read(self.HL)
		elif opcode == "FA":	#LOAD into A data from absolute address in nn
			self.A = self.read(self.fetch16())
		elif opcode == "3E":	#LOAD into A data from absolute address in n
			self.A = self.read(self.fetch())
		elif opcode == "02":	#LOAD into address specified by BC, data from A
			self.write(self.BC, self.A)
		elif opcode == "12": 	#LOAD into address specified by DE, data from A
			self.write(self.DE, self.A)
		elif opcode == "77":	#LOAD into address specified by HL, data from A
			self.write(self.HL, self.A)
		elif opcode == "EA":	#LOAD into address specified by nn, data from A
			self.write(self.fetch16(), self.A)

	def boot(self):
		while self.programCounter != Bin16.fromHex("0100"):
			ins = self.fetch()
			self.decode(ins)
		print(self.programCounter, self.programCounter.toHex())