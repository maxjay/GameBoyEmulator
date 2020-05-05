from binary import Bin
from binary import Bin16
from memory import *

# ALU will handle all arthimetic 
# Returns answer, sets flags automatically
class ALU():
	def __init__(self, F):
		self.F = F
		#	7	Zero
		#	6	Subtraction
		#	5	Half carry/borrow
		#	4	Overflow/underflow

	def __setattr__(self, name, value):
		if name in dir(self):
			if isinstance(value, Bin):
				super().__getattribute__(name).array = value.array
			else:
				super().__setattr__(name, value)
		else:
			super().__setattr__(name, value)

	def __getattribute__(self, name):
		return super().__getattribute__(name)

	def overflowing_add(self, a, b, c=0):
		self.F[6] = 0 
		temp = Bin16() if isinstance(a, Bin16) else Bin()
		checks = [11,15] if isinstance(a, Bin16) else [3,7]
		for i in range(checks[1]+1):
			temp[i], c = Bin.fullAdder(a[i], b[i], c)
			if i == checks[0]:
				self.F[5] = c
			if i == checks[1]:
				self.F[4] = c
		self.F[7] = 1 if temp.toDecimal() == 0 else 0
		return  temp

	def ADD(self, x, y):	#ADD x,y
		return self.overflowing_add(x, y)

	def ADC(self, x, y,):	#ADC x,y
		return self.overflowing_add(x,y,self.F[4])

class CPU():
	programCounter = Bin16.fromHex("0100")
	stackPointer = Bin16.fromHex("FFFE")
	A = Bin.fromHex("11")
	B = Bin.fromHex("00")
	C = Bin.fromHex("00")
	D = Bin.fromHex("FF")
	E = Bin.fromHex("56")
	F = Bin.fromHex("80")
	H = Bin.fromHex("00")
	L = Bin.fromHex("0D")

	def __setattr__(self, name, value):
		if isinstance(value, Memory):
			super().__setattr__(name, value)
		elif isinstance(value, ALU):
			super().__setattr__(name, value)
		elif isinstance(value, Bin):
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
			elif name == "stackPointer":
				super().__getattribute__(name).array = value.array
			elif name == "programCounter":
				super().__getattribute__(name).array = value.array

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
		self.ALU = ALU(self.F)
		self.memoryBus = Memory

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
		#8 bit opcodes
		#8 BIT LOAD INSTRUCTIONS	
		if opcode == "06":		#LD B,N
			self.B = self.fetch()
		elif opcode == "0E":	#LD C,N
			self.C = self.fetch()
		elif opcode == "16":	#LD D,N
			self.D = self.fetch()
		elif opcode == "1E":	#LD E,N
			self.E = self.fetch()
		elif opcode == "26":	#LD H,N
			self.H = self.fetch()
		elif opcode == "2E":	#LD L,N
			self.L = self.fetch()
		elif opcode == "7F":	#LD A,A
			self.A = self.A
		elif opcode == "78":	#LD A,B
			self.A = self.B
		elif opcode == "79":	#LD A,C
			self.A = self.C
		elif opcode == "7A":	#LD A,D
			self.A = self.D
		elif opcode == "7B":	#LD A,E
			self.A = self.E
		elif opcode == "7C":	#LD A,H
			self.A = self.H
		elif opcode == "7D":	#LD A,L
			self.A = self.H
		elif opcode == "40":	#LD B,B
			self.B = self.B
		elif opcode == "41":	#LD B,C
			self.B = self.C
		elif opcode == "42":	#LD B,D
			self.B = self.D
		elif opcode == "43":	#LD B,E
			self.B = self.E
		elif opcode == "44":	#LD B,H
			self.B = self.H
		elif opcode == "45":	#LD B,L
			self.B = self.L
		elif opcode == "46":	#LD B,(HL)
			self.B = self.read(self.HL) 
		elif opcode == "47":	#LD B,A
			self.B = self.A
		elif opcode == "48":	#LD C,B
			self.C = self.B
		elif opcode == "49":	#LD C,C
			self.C = self.C
		elif opcode == "4A":	#LD C,D
			self.C = self.D
		elif opcode == "4B":	#LD C,E
			self.C = self.E
		elif opcode == "4C":	#lD C,H
			self.C = self.H
		elif opcode == "4D":	#LD C,L
			self.C = self.L
		elif opcode == "4E":	#LD C,(HL)
			self.C = self.read(self.HL)
		elif opcode == "4F":	#LD C,A
			self.C = self.A
		elif opcode == "50":	#LD D,B
			self.D = self.B
		elif opcode == "51":	#LD D,C
			self.D = self.C
		elif opcode == "52":	#LD D,D
			self.D = self.D
		elif opcode == "53":	#LD D,E
			self.D = self.E
		elif opcode == "54":	#lD D,H
			self.D = self.H
		elif opcode == "55":	#LD D,L
			self.D = self.L
		elif opcode == "56":	#LD D,(HL)
			self.D = self.read(self.HL)
		elif opcode == "57":	#LD D,A
			self.D = self.A
		elif opcode == "58":	#LD E,B
			self.E = self.B
		elif opcode == "59":	#LD E,C
			self.E = self.C
		elif opcode == "5A":	#LD E,D
			self.E = self.D
		elif opcode == "5B":	#LD E,E
			self.E = self.E
		elif opcode == "5C":	#lD E,H
			self.E = self.H
		elif opcode == "5D":	#LD E,L
			self.E = self.L
		elif opcode == "5E":	#LD E,(HL)
			self.E = self.read(self.HL)
		elif opcode == "5F":	#LD E,A
			self.E = self.A
		elif opcode == "60":	#LD H,B
			self.H = self.B
		elif opcode == "61":	#LD H,C
			self.H = self.C
		elif opcode == "62":	#LD H,D
			self.H = self.D
		elif opcode == "63":	#LD H,E
			self.H = self.E
		elif opcode == "64":	#lD H,H
			self.H = self.H
		elif opcode == "65":	#LD H,L
			self.H = self.L
		elif opcode == "66":	#LD H,(HL)
			self.H = self.read(self.HL)
		elif opcode == "67":	#LD H,A
			self.H = self.A
		elif opcode == "68":	#LD L,B
			self.L = self.B
		elif opcode == "69":	#LD L,C
			self.L = self.C
		elif opcode == "6A":	#LD L,D
			self.L = self.D
		elif opcode == "6B":	#LD L,E
			self.L = self.E
		elif opcode == "6C":	#lD L,H
			self.L = self.H
		elif opcode == "6D":	#LD L,L
			self.L = self.L
		elif opcode == "6E":	#LD L,(HL)
			self.L = self.read(self.HL)
		elif opcode == "6F":	#LD L,A
			self.L = self.A
		elif opcode == "70":	#LD (HL),B
			self.write(self.HL, self.B)
		elif opcode == "71":	#LD (HL),C
			self.write(self.HL, self.C)
		elif opcode == "72":	#LD (HL),D
			self.write(self.HL, self.D)
		elif opcode == "73":	#LD (HL),E
			self.write(self.HL, self.E)
		elif opcode == "74":	#LD (HL),H
			self.write(self.HL, self.E)
		elif opcode == "75":	#LD (HL),L
			self.write(self.HL, self.E)
		elif opcode == "76":	#LD (HL),n
			self.write(self.HL, self.fetch())
		elif opcode == "0A":	#LD A,(BC)
			self.A = self.read(self.BC)
		elif opcode == "1A":	#LD A,(DE)
			self.A = self.read(self.DE)
		elif opcode == "7E":	#LD A,(HL)
			self.A = self.read(self.HL)
		elif opcode == "FA":	#LD A,(nn)
			self.A = self.read(self.fetch16())
		elif opcode == "3E":	#LD A,n
			self.A = self.fetch()
		elif opcode == "02":	#LD (BC),A
			self.write(self.BC, self.A)
		elif opcode == "12":	#LD (DE),A
			self.write(self.DE, self.A)
		elif opcode == "77":	#LD (HL),A
			self.write(self.HL, self.A)
		elif opcode == "EA":	#LD (nn),A
			self.write(self.fetch16, self.A)
		elif opcode == "F2":	#LD A,(C)
			self.A = self.read(self.C)
		elif opcode == "E2":	#LD (C),A
			self.write(self.C, self.A)
		elif opcode == "3A":	#LDD A,(HL)
			self.A = self.read(self.HL)
			self.HL -= 1
		elif opcode == "32":	#LDD (HL),A
			self.write(self.HL, self.A)
			self.HL -= 1
		elif opcode == "2A":	#LDI A,(HL)
			self.A = self.read(self.HL)
			self.HL += 1
		elif opcode == "22":	#LDI (HL),A
			self.write(self.HL, self.A)
			self.HL += 1
		elif opcode == "E0":	#LDH (n),A
			self.write(self.fetch(), self.A)
		elif opcode == "F0":	#LDH A,(n)
			self.A = self.read(self.n)
		#16 BIT LOADS
		elif opcode == "01":	#LD BC,nn
			self.BC = self.fetch16()
		elif opcode == "11":	#LD DE,nn
			self.DE = self.fetch16()
		elif opcode == "21":	#LD HL,nn
			self.HL = self.fetch16()
		elif opcode == "31":	#LD SP,nn
			self.stackPointer = self.fetch16()
		elif opcode == "F9":	#LD SP,HL
			self.stackPointer = self.HL
		elif opcode == "F8":	#LDHL SP,n
			a = self.stackPointer
			b = self.fetch()
			self.HL, self.F[4] = Bin.overflowing_add(a,b)
			self.HL = self.read(self.HL)
			self.F[7]= 0
			self.F[6]= 0
			self.F[5]= Bin.halfcarry(a, b)
		elif opcode == "08":	#LD (nn),SP
			self.write(self.fetch16(), self.stackPointer)
		elif opcode == "F5":	#PUSH AF
			self.stackPointer -= 1
			self.write(self.stackPointer, self.A)
			self.stackPointer -= 1
			self.write(self.stackPointer, self.F)
		elif opcode == "C5":	#PUSH BC
			self.stackPointer -= 1
			self.write(self.stackPointer, self.B)
			self.stackPointer -= 1
			self.write(self.stackPointer, self.C)
		elif opcode == "D5":	#PUSH DE
			self.stackPointer -= 1
			self.write(self.stackPointer, self.D)
			self.stackPointer -= 1
			self.write(self.stackPointer, self.E)
		elif opcode == "E5":	#PUSH HL
			self.stackPointer -= 1
			self.write(self.stackPointer, self.H)
			self.stackPointer -= 1
			self.write(self.stackPointer, self.L)
		elif opcode == "F1":	#POP AF
			self.F = self.read(self.stackPointer)
			self.stackPointer += 1
			self.A = self.read(self.stackPointer)
			self.stackPointer += 1
		elif opcode == "C1":	#POP BC
			self.C = self.read(self.stackPointer)
			self.stackPointer += 1
			self.B = self.read(self.stackPointer)
			self.stackPointer += 1
		elif opcode == "D1":	#POP DE
			self.E = self.read(self.stackPointer)
			self.stackPointer += 1
			self.D = self.read(self.stackPointer)
			self.stackPointer += 1
		elif opcode == "E1":	#POP HL
			self.L = self.read(self.stackPointer)
			self.stackPointer += 1
			self.H = self.read(self.stackPointer)
			self.stackPointer += 1
		#8 BIT ALU
		elif opcode == "87":	#ADD A,A
			self.A = self.ALU.ADD(self.A, self.A)
		elif opcode == "80":	#ADD A,B
			self.A = self.ALU.ADD(self.A, self.B)
		elif opcode == "81":	#ADD A,C
			self.A = self.ALU.ADD(self.A, self.C)
		elif opcode == "82":	#ADD A,D
			self.A = self.ALU.ADD(self.A, self.D)
		elif opcode == "83":	#ADD A,E
			self.A = self.ALU.ADD(self.A, self.E)
		elif opcode == "84":	#ADD A,H
			self.A = self.ALU.ADD(self.A, self.H)
		elif opcode == "85":	#ADD A,L
			self.A = self.ALU.ADD(self.A, self.L)
		elif opcode == "86":	#ADD A,(HL)
			self.A = self.ALU.ADD(self.A, self.read(self.HL))
		elif opcode == "C6":	#ADD A,n
			self.A = self.ALU.ADD(self.A, self.fetch())
		elif opcode == "8F":	#ADC A,A
			self.A = self.ALU.ADC(self.A, self.A)
		elif opcode == "88":	#ADC A,B
			self.A = self.ALU.ADC(self.A, self.B)
		elif opcode == "89":	#ADC A,C
			self.A = self.ALU.ADC(self.A, self.C)
		elif opcode == "8A":	#ADC A,D
			self.A = self.ALU.ADC(self.A, self.D)
		elif opcode == "8B":	#ADC A,E
			self.A = self.ALU.ADC(self.A, self.E)
		elif opcode == "8C":	#ADC A,H
			self.A = self.ALU.ADC(self.A, self.H)
		elif opcode == "8D":	#ADC A,L
			self.A = self.ALU.ADC(self.A, self.L)
		elif opcode == "8E":	#ADC A,(HL)
			self.A = self.ALU.ADC(self.A, self.read(self.HL))
		elif opcode == "CE":	#ADC A,n
			self.A = self.ALU.ADC(self.A, self.fetch())
		else:
			pass

	def debug(self):
		while True:
			print("AF: {0}\nBC: {1}\nDE: {2}\nHL: {3}\nStack Pointer: {4}\nProgram Counter: {5}".format(self.AF.toHex(), self.BC.toHex(), self.DE.toHex(), self.HL.toHex(), self.stackPointer.toHex(), self.programCounter.toHex()))
			print("Program Counter at: {0}\tInstruction: {1}".format(self.programCounter.toHex(), self.memoryBus[self.programCounter].toHex()))
			self.execute(self.fetch())
			input()

	def run(self):
		while True:
			print("Program Counter at: {0}\tInstruction: {1}".format(self.programCounter.toHex(), self.memoryBus[self.programCounter].toHex()))
			self.execute(self.fetch())
			#if (self.memoryBus[Bin16.fromHex("FF02")] == Bin.fromHex("81")):
			#	print("Y")

	#def boot(self):
	#	while self.programCounter != Bin16.fromHex("0100"):
	#		ins = self.fetch()
	#		self.decode(ins)
	#	print(self.programCounter, self.programCounter.toHex())