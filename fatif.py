'''
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
			self.write(self.HL, self.H)
		elif opcode == "75":	#LD (HL),L
			self.write(self.HL, self.L)
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
			self.write(self.fetch16(), self.A)
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
			x = self.memoryBus[Bin16.fromHex("C000")]
			b = self.read(self.HL)
			c = 1
			self.A = b
			self.HL += 1
		elif opcode == "22":	#LDI (HL),A
			self.write(self.HL, self.A)
			self.HL += 1
		elif opcode == "E0":	#LDH (n),A
			self.write(self.fetch(), self.A)
		elif opcode == "F0":	#LDH A,(n)
			self.A = self.read(self.fetch())
		#16 BIT LOADS
		elif opcode == "01":	#LD BC,nn
			self.BC = self.fetch16()
		elif opcode == "11":	#LD DE,nn
			self.DE = self.fetch16()
		elif opcode == "21":	#LD HL,nn
			n = self.fetch16()
			self.HL = n
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
		elif opcode == "97":	#SUB A,A
			self.A = self.ALU.SUB(self.A, self.A)
		elif opcode == "90":	#SUB A,B
			self.A = self.ALU.SUB(self.A, self.B)
		elif opcode == "91":	#SUB A,C
			self.A = self.ALU.SUB(self.A, self.C)
		elif opcode == "92":	#SUB A,D
			self.A = self.ALU.SUB(self.A, self.D)
		elif opcode == "93":	#SUB A,E
			self.A = self.ALU.SUB(self.A, self.E)
		elif opcode == "94":	#SUB A,H
			self.A = self.ALU.SUB(self.A, self.H)
		elif opcode == "95":	#SUB A,l
			self.A = self.ALU.SUB(self.A, self.L)
		elif opcode == "96":	#SUB A,(HL)
			self.A = self.ALU.SUB(self.A, self.read(self.HL))
		elif opcode == "D6":	#SUB A,n
			self.A = self.ALU.SUB(self.A, self.fetch())
		elif opcode == "9F":	#SBC A,A
			self.A = self.ALU.SBC(self.A, self.A)
		elif opcode == "98":	#SBC A,B
			self.A = self.ALU.SBC(self.A, self.B)
		elif opcode == "99":	#SBC A,C
			self.A = self.ALU.SBC(self.A, self.C)
		elif opcode == "9A":	#SBC A,D
			self.A = self.ALU.SBC(self.A, self.D)
		elif opcode == "9B":	#SBC A,E
			self.A = self.ALU.SBC(self.A, self.E)
		elif opcode == "9C":	#SBC A,H
			self.A = self.ALU.SBC(self.A, self.H)
		elif opcode == "9D":	#SBC A,L
			self.A = self.ALU.SBC(self.A, self.L)
		elif opcode == "9E":	#SBC A,(HL)
			self.A = self.ALU.SBC(self.A, self.read(self.HL))
		elif opcode == "A7":	#AND A,A	
			self.A = self.ALU.AND(self.A, self.A)
		elif opcode == "A0":	#AND A,B
			self.A = self.ALU.AND(self.A, self.B)
		elif opcode == "A1":	#AND A,C
			self.A = self.ALU.AND(self.A, self.C)
		elif opcode == "A2":	#AND A,D
			self.A = self.ALU.AND(self.A, self.D)
		elif opcode == "A3":	#AND A,E
			self.A = self.ALU.AND(self.A, self.E)
		elif opcode == "A4":	#AND A,H
			self.A = self.ALU.AND(self.A, self.H)
		elif opcode == "A5":	#AND A,L
			self.A = self.ALU.AND(self.A, self.L)
		elif opcode == "A6":	#AND A,(HL)
			self.A = self.ALU.AND(self.A, self.read(self.HL))
		elif opcode == "E6":	#AND A,n
			self.A = self.ALU.AND(self.A, self.fetch())
		elif opcode == "B7":	#OR A,A
			self.A = self.ALU.OR(self.A, self.A)
		elif opcode == "B0":	#OR A,B
			self.A = self.ALU.OR(self.A, self.B)
		elif opcode == "B1":	#OR A,C
			self.A = self.ALU.OR(self.A, self.C)
		elif opcode == "B2":	#OR A,D
			self.A = self.ALU.OR(self.A, self.D)
		elif opcode == "B3":	#OR A,E
			self.A = self.ALU.OR(self.A, self.E)
		elif opcode == "B4":	#OR A,H
			self.A = self.ALU.OR(self.A, self.H)
		elif opcode == "B5":	#OR A,L
			self.A = self.ALU.OR(self.A, self.L)
		elif opcode == "B6":	#OR A,(HL)
			self.A = self.ALU.OR(self.A, self.read(self.HL))
		elif opcode == "F6":	#OR A,n
			self.A = self.ALU.OR(self.A, self.fetch())
		elif opcode == "AF":	#XOR A,A
			self.A = self.ALU.XOR(self.A, self.A)
		elif opcode == "A8":	#XOR A,B
			self.A = self.ALU.XOR(self.A, self.B)
		elif opcode == "A9":	#XOR A,C
			self.A = self.ALU.XOR(self.A, self.C)
		elif opcode == "AA":	#XOR A,D
			self.A = self.ALU.XOR(self.A, self.D)
		elif opcode == "AB":	#XOR A,E
			self.A = self.ALU.XOR(self.A, self.E)
		elif opcode == "AC":	#XOR A,H
			self.A = self.ALU.XOR(self.A, self.H)
		elif opcode == "AD":	#XOR A,L
			self.A = self.ALU.XOR(self.A, self.L)
		elif opcode == "AE":	#XOR A,(HL)
			self.A = self.ALU.XOR(self.A, self.read(self.HL))
		elif opcode == "EE":	#XOR A,n
			self.A = self.ALU.XOR(self.A, self.fetch())
		elif opcode == "BF":	#CP A,A
			self.ALU.CP(self.A, self.A)
		elif opcode == "B8":	#CP A,B
			self.ALU.CP(self.A, self.B)
		elif opcode == "B9":	#CP A,C
			self.ALU.CP(self.A, self.C)
		elif opcode == "BA":	#CP A,D
			self.ALU.CP(self.A, self.D)
		elif opcode == "BB":	#CP A,E
			self.ALU.CP(self.A, self.E)
		elif opcode == "BC":	#CP A,H
			self.ALU.CP(self.A, self.H)
		elif opcode == "BD":	#CP A,L
			self.ALU.CP(self.A, self.L)
		elif opcode == "BE":	#CP A,(HL)
			self.ALU.CP(self.A, self.read(self.HL))
		elif opcode == "FE":	#CP A,n
			self.ALU.CP(self.A, self.fetch())
		elif opcode == "3C":	#INC A
			self.A = self.ALU.INC(self.A)
		elif opcode == "04":	#INC B
			self.B = self.ALU.INC(self.B)
		elif opcode == "0C":	#INC C
			self.C = self.ALU.INC(self.C)
		elif opcode == "14":	#INC D
			self.D = self.ALU.INC(self.D)
		elif opcode == "1C":	#INC E
			self.E = self.ALU.INC(self.E)
		elif opcode == "24":	#INC H
			self.H = self.ALU.INC(self.H)
		elif opcode == "2C":	#INC L
			self.L = self.ALU.INC(self.L)
		elif opcode == "34":	#INC (HL)
			self.write(self.read(self.HL), self.ALU.INC(self.read(self.HL)))
		elif opcode == "3D":	#DEC A
			self.A = self.ALU.DEC(self.A)
		elif opcode == "05":	#DEC B
			self.B = self.ALU.DEC(self.B)
		elif opcode == "0D":	#DEC C
			self.C = self.ALU.DEC(self.C)
		elif opcode == "15":	#DEC D
			self.D = self.ALU.DEC(self.D)
		elif opcode == "1D":	#DEC E
			self.E = self.ALU.DEC(self.E)
		elif opcode == "25":	#DEC H
			self.H = self.ALU.DEC(self.H)
		elif opcode == "2D":	#DEC L
			self.L = self.ALU.DEC(self.L)
		elif opcode == "35":	#DEC (HL)
			self.write(self.read(self.HL), self.ALU.DEC(self.read(self.HL)))
		#16 bit arithmetic
		elif opcode == "09":	#ADD HL, BC
			self.HL = self.ALU.ADD_HL(self.HL, self.BC)
		elif opcode == "19":	#ADD HL, DE
			self.HL = self.ALU.ADD_HL(self.HL, self.DE)
		elif opcode == "29":	#ADD HL, HL
			self.HL = self.ALU.ADD_HL(self.HL, self.HL)
		elif opcode == "39":	#ADD HL, SP
			self.HL = self.ALU.ADD_HL(self.HL, self.stackPointer)
		elif opcode == "E8":	#ADD SP,#
			self.stackPointer = self.ALU.ADD_SP(self.stackPointer, self.fetch())
		elif opcode == "03":	#INC BC
			self.BC = self.ALU.INC(self.BC)
		elif opcode == "13":	#INC DE
			self.DE = self.ALU.INC(self.DE)
		elif opcode == "23":	#INC HL
			self.HL = self.ALU.INC(self.HL)
		elif opcode == "33":	#INC SP
			self.stackPointer = self.ALU.INC(self.stackPointer)
		elif opcode == "0B":	#DEC BC
			self.BC = self.ALU.DEC(self.BC)
		elif opcode == "1B":	#DEC DE
			self.DE = self.ALU.DEC(self.BC)
		elif opcode == "2B":	#DEC HL
			self.HL = self.ALU.DEC(self.BC)
		elif opcode == "3B":	#DEC SP
			self.stackPointer = self.ALU.DEC(self.stackPointer)
		#MISC
		elif opcode == "27":	#DAA
			self.A = self.ALU.DAA(self.A)
		elif opcode == "3F":	#CCF
			self.ALU.CCF()
		elif opcode == "37":	#SCF
			self.ALU.SCF()
		elif opcode == "00":	#NOP
			pass
		elif opcode == "76":	#HALT CPU TODO
			pass
		elif opcode == "10":	#HALT CPU AND LCD TODO
			if self.fetch() == "00":
				pass
		elif opcode == "F3":	#DI	TODO
			pass
		elif opcode == "FB":	#EI TODO
			pass
		#rotates and shifts
		elif opcode == "07":	#RLCA
			a = self.A[7]
			self.A = self.A << 1
			self.A[0] = a
			self.F[4] = a
			self.F[7] = self.F[6] = self.F[5] = 0
		elif opcode == "17":	#RLA
			a = self.A[7]
			self.A = self.A << 1
			self.A[0] = self.F[4]
			self.F[4] = a
			self.F[7] = self.F[6] = self.F[5] = 0
		elif opcode == "0F":	#RRCA
			a = self.A[0]
			self.A = self.A >> 1
			self.A[7] = a
			self.F[4] = a
			self.F[7] = self.F[6] = self.F[5] = 0
		elif opcode == "1F":	#RRA
			a = self.A[0]
			self.A = self.A >> 1
			self.A[7] = self.F[4]
			self.F[4] = a
			self.F[7] = self.F[6] = self.F[5] = 0
		#jump codes
		elif opcode == "C3":	#JP nn
			self.programCounter = self.fetch16()
		elif opcode == "C2":	#JP NZ, nn
			if not self.F[7]:
				self.programCounter = self.fetch16()
		elif opcode == "CA":	#JP Z, nn
			if self.F[7]:
				self.programCounter = self.fetch16()
		elif opcode == "D2":	#JP NC, nn
			if not self.F[4]:
				self.programCounter = self.fetch16()
		elif opcode == "DA":	#JP C,nn
			if self.F[4]:
				self.programCounter = self.fetch16()
		elif opcode == "E9":	#JP (hl)
			self.programCounter = self.read(self.HL)
		elif opcode == "18":	#JR n
			n = self.fetch()
			self.programCounter = self.ALU.ADD_E(n, self.programCounter)
		elif opcode == "20":	#JR NZ,*
			if not self.F[7]:
				n = self.fetch()
				self.programCounter = self.ALU.ADD_E(n, self.programCounter)
		elif opcode == "28":	#JR Z,*
			if self.F[7]:
				n = self.fetch()
				self.programCounter = self.ALU.ADD_E(n, self.programCounter)
		elif opcode == "30":	#JR NC,*
			if not self.F[4]:
				n = self.fetch()
				self.programCounter = self.ALU.ADD_E(n, self.programCounter)
		elif opcode == "38":	#JR C,*
			if self.F[4]:
				n = self.fetch()
				self.programCounter = self.ALU.ADD_E(n, self.programCounter)
		#CALLS
		elif opcode == "CD":	#CALL, nn
			nn = self.fetch16()
			self.stackPointer -= 1
			self.write(self.stackPointer, self.programCounter.to8Bin()[1])
			self.stackPointer -= 1
			self.write(self.stackPointer, self.programCounter.to8Bin()[0])
		elif opcode == "C4":	#CALL NZ, nn
			if not self.F[7]:
				nn = self.fetch16()
				self.stackPointer -= 1
				self.write(self.stackPointer, self.programCounter.to8Bin()[1])
				self.stackPointer -= 1
				self.write(self.stackPointer, self.programCounter.to8Bin()[0])
		elif opcode == "CC":	#CALL Z, nn
			if self.F[7]:
				nn = self.fetch16()
				self.stackPointer -= 1
				self.write(self.stackPointer, self.programCounter.to8Bin()[1])
				self.stackPointer -= 1
				self.write(self.stackPointer, self.programCounter.to8Bin()[0])
		elif opcode == "D4":	#CALL NC, nn
			if not self.F[4]:
				nn = self.fetch16()
				self.stackPointer -= 1
				self.write(self.stackPointer, self.programCounter.to8Bin()[1])
				self.stackPointer -= 1
				self.write(self.stackPointer, self.programCounter.to8Bin()[0])
		elif opcode == "DC":	#CALL C, nn
			if self.F[4]:
				nn = self.fetch16()
				self.stackPointer -= 1
				self.write(self.stackPointer, self.programCounter.to8Bin()[1])
				self.stackPointer -= 1
				self.write(self.stackPointer, self.programCounter.to8Bin()[0])
		#RESTARTS
		elif opcode == "CB":
			arg = self.fetch()
			#MISC
			if arg == "37":			#SWAP A
				self.A = self.ALU.SWAP(self.A)
			elif arg == "30":		#SWAP B
				self.B = self.ALU.SWAP(self.B)
			elif arg == "31":		#SWAP C
				self.C = self.ALU.SWAP(self.C)
			elif arg == "32":		#SWAP D
				self.D = self.ALU.SWAP(self.D)
			elif arg == "33":		#SWAP E
				self.E = self.ALU.SWAP(self.E)
			elif arg == "34":		#SWAP H
				self.H = self.ALU.SWAP(self.H)
			elif arg == "35":		#SWAP L
				self.L = self.ALU.SWAP(self.L)
			elif arg == "36":		#SWAP (HL)
				add = self.fetch()
				self.write(add, self.ALU.SWAP(add))
			#rotates and shit
			elif arg == "07":		#RLC A
				self.RLC(self.A)
			elif arg == "00":		#RLC B
				self.RLC(self.B)
			elif arg == "01":		#RLC C
				self.RLC(self.C)
			elif arg == "02":		#RLC D
				self.RLC(self.D)
			elif arg == "03":		#RLC E
				self.RLC(self.E)
			elif arg == "04":		#RLC H
				self.RLC(self.H)
			elif arg == "05":		#RLC L
				self.RLC(self.L)
			elif arg == "06":		#RLC (HL)
				self.write(self.HL, self.RLC(self.read(self.HL)))
			elif arg == "17":		#RL A
				self.RL(self.A)
			elif arg == "10":		#RL B
				self.RL(self.B)
			elif arg == "11":		#RL C
				self.RL(self.C)
			elif arg == "12":		#RL D
				self.RL(self.D)
			elif arg == "13":		#RL E
				self.RL(self.E)
			elif arg == "14":		#RL H
				self.RL(self.H)
			elif arg == "15":		#RL L
				self.RL(self.L)
			elif arg == "16":		#RL (HL)
				self.write(self.HL, self.RL(self.read(self.HL)))
			elif arg == "0F":		#RRC A
				self.RRC(self.A)
			elif arg == "08":		#RRC B
				self.RRC(self.B)
			elif arg == "09":		#RRC C
				self.RRC(self.C)
			elif arg == "0A":		#RRC D
				self.RRC(self.D)
			elif arg == "0B":		#RRC E
				self.RRC(self.E)
			elif arg == "0C":		#RRC H
				self.RRC(self.H)
			elif arg == "0D":		#RRC L
				self.RRC(self.L)
			elif arg == "0E":		#RRC (HL)
				self.write(self.HL, self.RRC(self.read(self.HL)))
			elif arg == "1F":		#RR A
				self.RR(self.A)
			elif arg == "18":		#RR B
				self.RR(self.B)
			elif arg == "19":		#RR C
				self.RR(self.C)
			elif arg == "1A":		#RR D
				self.RR(self.D)
			elif arg == "1B":		#RR E
				self.RR(self.E)
			elif arg == "1C":		#RR H
				self.RR(self.H)
			elif arg == "1D":		#RR L
				self.RR(self.L)
			elif arg == "1E":		#RR (HL)
				self.write(self.HL, self.RR(self.read(self.HL)))
			elif arg == "27":		#SLA A
				self.SLA(self.A)
			elif arg == "20":		#SLA B
				self.SLA(self.B)
			elif arg == "21":		#SLA C
				self.SLA(self.C)
			elif arg == "22":		#SLA D
				self.SLA(self.D)
			elif arg == "23":		#SLA E
				self.SLA(self.E)
			elif arg == "24":		#SLA H
				self.SLA(self.H)
			elif arg == "25":		#SLA L
				self.SLA(self.L)
			elif arg == "26":		#SLA (HL)
				self.write(self.HL, self.SLA(self.read(self.HL)))
			elif arg == "2F":		#SRA A
				self.SRA(self.A)
			elif arg == "28":		#SRA B
				self.SRA(self.B)
			elif arg == "29":		#SRA C
				self.SRA(self.C)
			elif arg == "2A":		#SRA D
				self.SRA(self.D)
			elif arg == "2B":		#SRA E
				self.SRA(self.E)
			elif arg == "2C":		#SRA H
				self.SRA(self.H)
			elif arg == "2D":		#SRA L
				self.SRA(self.L)
			elif arg == "2E":		#SRA (HL)
				self.write(self.HL, self.SRA(self.read(self.HL)))
			elif arg == "3F":		#SRL A
				self.SRL(self.A)
			elif arg == "38":		#SRL B
				self.SRL(self.B)
			elif arg == "39":		#SRL C
				self.SRL(self.C)
			elif arg == "3A":		#SRL D
				self.SRL(self.D)
			elif arg == "3B":		#SRL E
				self.SRL(self.E)
			elif arg == "3C":		#SRL H
				self.SRL(self.H)
			elif arg == "3D":		#SRL L
				self.SRL(self.L)
			elif arg == "3E":		#SRL (HL)
				self.write(self.HL, self.SRL(self.read(self.HL)))
			#BIT STUFF
			elif arg == "40":		#BIT 0,B
				self.BIT(0, self.B)
			elif arg == "41":		#BIT 0,C
				self.BIT(0, self.C)
			elif arg == "42":		#BIT 0,D
				self.BIT(0, self.D)
			elif arg == "43":		#BIT 0,E
				self.BIT(0, self.E)
			elif arg == "44":		#BIT 0,H
				self.BIT(0, self.H)
			elif arg == "45":		#BIT 0,L
				self.BIT(0, self.L)
			elif arg == "46":		#BIT 0,(HL)
				self.BIT(0, self.read(self.HL))
			elif arg == "47":		#BIT 0,A
				self.BIT(0, self.A)
			elif arg == "48":		#BIT 1,B
				self.BIT(1, self.B)
			elif arg == "49":		#BIT 1,C
				self.BIT(1, self.C)
			elif arg == "4A":		#BIT 1,D
				self.BIT(1, self.D)
			elif arg == "4B":		#BIT 1,E
				self.BIT(1, self.E)
			elif arg == "4C":		#BIT 1,H
				self.BIT(1, self.H)
			elif arg == "4D":		#BIT 1,L
				self.BIT(1, self.L)
			elif arg == "4E":		#BIT 1,(HL)
				self.BIT(1, self.read(self.HL))
			elif arg == "4F":		#BIT 1,A
				self.BIT(1, self.A)
			elif arg == "50":		#BIT 2,B
				self.BIT(2, self.B)
			elif arg == "51":		#BIT 2,C
				self.BIT(2, self.C)
			elif arg == "52":		#BIT 2,D
				self.BIT(2, self.D)
			elif arg == "53":		#BIT 2,E
				self.BIT(2, self.E)
			elif arg == "54":		#BIT 2,H
				self.BIT(2, self.H)
			elif arg == "55":		#BIT 2,L
				self.BIT(2, self.L)
			elif arg == "56":		#BIT 2,(HL)
				self.BIT(2, self.read(self.HL))
			elif arg == "57":		#BIT 2,A
				self.BIT(2, self.A)
			elif arg == "58":		#BIT 3,B
				self.BIT(3, self.B)
			elif arg == "59":		#BIT 3,C
				self.BIT(3, self.C)
			elif arg == "5A":		#BIT 3,D
				self.BIT(3, self.D)
			elif arg == "5B":		#BIT 3,E
				self.BIT(3, self.E)
			elif arg == "5C":		#BIT 3,H
				self.BIT(3, self.H)
			elif arg == "5D":		#BIT 3,L
				self.BIT(3, self.L)
			elif arg == "5E":		#BIT 3,(HL)
				self.BIT(3, self.read(self.HL))
			elif arg == "5F":		#BIT 3,A
				self.BIT(3, self.A)
			elif arg == "60":		#BIT 4,B
				self.BIT(4, self.B)
			elif arg == "61":		#BIT 4,C
				self.BIT(4, self.C)
			elif arg == "62":		#BIT 4,D
				self.BIT(4, self.D)
			elif arg == "63":		#BIT 4,E
				self.BIT(4, self.E)
			elif arg == "64":		#BIT 4,H
				self.BIT(4, self.H)
			elif arg == "65":		#BIT 4,L
				self.BIT(4, self.L)
			elif arg == "66":		#BIT 4,(HL)
				self.BIT(4, self.read(self.HL))
			elif arg == "67":		#BIT 4,A
				self.BIT(4, self.A)
			elif arg == "68":		#BIT 5,B
				self.BIT(5, self.B)
			elif arg == "69":		#BIT 5,C
				self.BIT(5, self.C)
			elif arg == "6A":		#BIT 5,D
				self.BIT(5, self.D)
			elif arg == "6B":		#BIT 5,E
				self.BIT(5, self.E)
			elif arg == "6C":		#BIT 5,H
				self.BIT(5, self.H)
			elif arg == "6D":		#BIT 5,L
				self.BIT(5, self.L)
			elif arg == "6E":		#BIT 5,(HL)
				self.BIT(5, self.read(self.HL))
			elif arg == "6F":		#BIT 6,A
				self.BIT(6, self.A)
			elif arg == "70":		#BIT 6,B
				self.BIT(6, self.B)
			elif arg == "71":		#BIT 6,C
				self.BIT(6, self.C)
			elif arg == "72":		#BIT 6,D
				self.BIT(6, self.D)
			elif arg == "73":		#BIT 6,E
				self.BIT(6, self.E)
			elif arg == "74":		#BIT 6,H
				self.BIT(6, self.H)
			elif arg == "75":		#BIT 6,L
				self.BIT(6, self.L)
			elif arg == "76":		#BIT 6,(HL)
				self.BIT(6, self.read(self.HL))
			elif arg == "77":		#BIT 6,A
				self.BIT(6, self.A)
			elif arg == "78":		#BIT 7,B
				self.BIT(7, self.B)
			elif arg == "79":		#BIT 7,C
				self.BIT(7, self.C)
			elif arg == "7A":		#BIT 7,D
				self.BIT(7, self.D)
			elif arg == "7B":		#BIT 7,E
				self.BIT(7, self.E)
			elif arg == "7C":		#BIT 7,H
				self.BIT(7, self.H)
			elif arg == "7D":		#BIT 7,L
				self.BIT(7, self.L)
			elif arg == "7E":		#BIT 7,(HL)
				self.BIT(7, self.read(self.HL))
			elif arg == "7F":		#BIT 7,A
				self.BIT(7, self.A)
			elif arg == "80":		#RES 0,B
				self.RES(0, self.B)
			elif arg == "81":		#RES 0,C
				self.RES(0, self.C)
			elif arg == "82":		#RES 0,D
				self.RES(0, self.D)
			elif arg == "83":		#RES 0,E
				self.RES(0, self.E)
			elif arg == "84":		#RES 0,H
				self.RES(0, self.H)
			elif arg == "85":		#RES 0,L
				self.RES(0, self.L)
			elif arg == "86":		#RES 0,(HL)
				self.write(self.HL, self.RES(0, self.read(self.HL)))
			elif arg == "87":		#RES 0,A
				self.RES(0, self.A)
			elif arg == "88":		#RES 1,B
				self.RES(1, self.B)
			elif arg == "89":		#RES 1,C
				self.RES(1, self.C)
			elif arg == "8A":		#RES 1,D
				self.RES(1, self.D)
			elif arg == "8B":		#RES 1,E
				self.RES(1, self.E)
			elif arg == "8C":		#RES 1,H
				self.RES(1, self.H)
			elif arg == "8D":		#RES 1,L
				self.RES(1, self.L)
			elif arg == "8E":		#RES 1,HL
				self.write(self.HL, self.RES(1, self.read(self.HL)))
			elif arg == "8F":		#RES 1,A
				self.RES(1, self.A)
			elif arg == "90":		#RES 2,B
				self.RES(2, self.B)
			elif arg == "91":		#RES 2,C
				self.RES(2, self.C)
			elif arg == "92":		#RES 2,D
				self.RES(2, self.D)
			elif arg == "93":		#RES 2,E
				self.RES(2, self.E)
			elif arg == "94":		#RES 2,H
				self.RES(2, self.H)
			elif arg == "95":		#RES 2,L
				self.RES(2, self.L)
			elif arg == "96":		#RES 2,(HL)
				self.write(self.HL, self.RES(2, self.read(self.HL)))
			elif arg == "97":		#RES 2,A
				self.RES(2, self.A)
			elif arg == "98":		#RES 3,B
				self.RES(3, self.B)
			elif arg == "99":		#RES 3,C
				self.RES(3, self.C)
			elif arg == "9A":		#RES 3,D
				self.RES(3, self.D)
			elif arg == "9B":		#RES 3,E
				self.RES(3, self.E)
			elif arg == "9C":		#RES 3,H
				self.RES(3, self.H)
			elif arg == "9D":		#RES 3,L
				self.RES(3, self.L)
			elif arg == "9E":		#RES 3,HL
				self.write(self.HL, self.RES(3, self.read(self.HL)))
			elif arg == "9F":		#RES 3,A
				self.RES(3, self.A)
			elif arg == "A0":		#RES 4,B
				self.RES(4, self.B)
			elif arg == "A1":		#RES 4,C
				self.RES(4, self.C)
			elif arg == "A2":		#RES 4,D
				self.RES(4, self.D)
			elif arg == "A3":		#RES 4,E
				self.RES(4, self.E)
			elif arg == "A4":		#RES 4,H
				self.RES(4, self.H)
			elif arg == "A5":		#RES 4,L
				self.RES(4, self.L)
			elif arg == "A6":		#RES 4,(HL)
				self.write(self.HL, self.RES(4, self.read(self.HL)))
			elif arg == "A7":		#RES 4,A
				self.RES(4, self.A)
			elif arg == "A8":		#RES 5,B
				self.RES(5, self.B)
			elif arg == "A9":		#RES 5,C
				self.RES(5, self.C)
			elif arg == "AA":		#RES 5,D
				self.RES(5, self.D)
			elif arg == "AB":		#RES 5,E
				self.RES(5, self.E)
			elif arg == "AC":		#RES 5,H
				self.RES(5, self.H)
			elif arg == "AD":		#RES 5,L
				self.RES(5, self.L)
			elif arg == "AE":		#RES 5,HL
				self.write(self.HL, self.RES(5, self.read(self.HL)))
			elif arg == "AF":		#RES 5,A
				self.RES(5, self.A)
			elif arg == "B0":		#RES 6,B
				self.RES(6, self.B)
			elif arg == "B1":		#RES 6,C
				self.RES(6, self.C)
			elif arg == "B2":		#RES 6,D
				self.RES(6, self.D)
			elif arg == "B3":		#RES 6,E
				self.RES(6, self.E)
			elif arg == "B4":		#RES 6,H
				self.RES(6, self.H)
			elif arg == "B5":		#RES 6,L
				self.RES(6, self.L)
			elif arg == "B6":		#RES 6,(HL)
				self.write(self.HL, self.RES(6, self.read(self.HL)))
			elif arg == "B7":		#RES 6,A
				self.RES(6, self.A)
			elif arg == "B8":		#RES 7,B
				self.RES(7, self.B)
			elif arg == "B9":		#RES 7,C
				self.RES(7, self.C)
			elif arg == "BA":		#RES 7,D
				self.RES(7, self.D)
			elif arg == "BB":		#RES 7,E
				self.RES(7, self.E)
			elif arg == "BC":		#RES 7,H
				self.RES(7, self.H)
			elif arg == "BD":		#RES 7,L
				self.RES(7, self.L)
			elif arg == "BE":		#RES 7,HL
				self.write(self.HL, self.RES(7, self.read(self.HL)))
			elif arg == "BF":		#RES 7,A
				self.RES(7, self.A)
			elif arg == "C0":		#SET 0,B
				self.SET(0, self.B)
			elif arg == "C1":		#SET 0,C
				self.SET(0, self.C)
			elif arg == "C2":		#SET 0,D
				self.SET(0, self.D)
			elif arg == "C3":		#SET 0,E
				self.SET(0, self.E)
			elif arg == "C4":		#SET 0,H
				self.SET(0, self.H)
			elif arg == "C5":		#SET 0,L
				self.SET(0, self.L)
			elif arg == "C6":		#SET 0,(HL)
				self.write(self.HL, self.SET(0, self.read(self.HL)))
			elif arg == "C7":		#SET 0,A
				self.SET(0, self.A)
			elif arg == "C8":		#SET 1,B
				self.SET(1, self.B)
			elif arg == "C9":		#SET 1,C
				self.SET(1, self.C)
			elif arg == "CA":		#SET 1,D
				self.SET(1, self.D)
			elif arg == "CB":		#SET 1,E
				self.SET(1, self.E)
			elif arg == "CC":		#SET 1,H
				self.SET(1, self.H)
			elif arg == "CD":		#SET 1,L
				self.SET(1, self.L)
			elif arg == "CE":		#SET 1,(HL)
				self.write(self.HL, self.SET(1, self.read(self.HL)))
			elif arg == "CF":		#SET 1,A
				self.SET(1, self.A)
			elif arg == "D0":		#SET 2,B
				self.SET(2, self.B)
			elif arg == "D1":		#SET 2,C
				self.SET(2, self.C)
			elif arg == "D2":		#SET 2,D
				self.SET(2, self.D)
			elif arg == "D3":		#SET 2,E
				self.SET(2, self.E)
			elif arg == "D4":		#SET 2,H
				self.SET(2, self.H)
			elif arg == "D5":		#SET 2,L
				self.SET(2, self.L)
			elif arg == "D6":		#SET 2,(HL)
				self.write(self.HL, self.SET(2, self.read(self.HL)))
			elif arg == "D7":		#SET 2,A
				self.SET(2, self.A)
			elif arg == "D8":		#SET 3,B
				self.SET(3, self.B)
			elif arg == "D9":		#SET 3,C
				self.SET(3, self.C)
			elif arg == "DA":		#SET 3,D
				self.SET(3, self.D)
			elif arg == "DB":		#SET 3,E
				self.SET(3, self.E)
			elif arg == "DC":		#SET 3,H
				self.SET(3, self.H)
			elif arg == "DD":		#SET 3,L
				self.SET(3, self.L)
			elif arg == "DE":		#SET 3,(HL)
				self.write(self.HL, self.SET(3, self.read(self.HL)))
			elif arg == "DF":		#SET 3,A
				self.SET(3, self.A)
			elif arg == "E0":		#SET 4,B
				self.SET(4, self.B)
			elif arg == "E1":		#SET 4,C
				self.SET(4, self.C)
			elif arg == "E2":		#SET 4,D
				self.SET(4, self.D)
			elif arg == "E3":		#SET 4,E
				self.SET(4, self.E)
			elif arg == "E4":		#SET 4,H
				self.SET(4, self.H)
			elif arg == "E5":		#SET 4,L
				self.SET(4, self.L)
			elif arg == "E6":		#SET 4,(HL)
				self.write(self.HL, self.SET(4, self.read(self.HL)))
			elif arg == "E7":		#SET 4,A
				self.SET(4, self.A)
			elif arg == "E8":		#SET 5,B
				self.SET(5, self.B)
			elif arg == "E9":		#SET 5,C
				self.SET(5, self.C)
			elif arg == "EA":		#SET 5,D
				self.SET(5, self.D)
			elif arg == "EB":		#SET 5,E
				self.SET(5, self.E)
			elif arg == "EC":		#SET 5,H
				self.SET(5, self.H)
			elif arg == "ED":		#SET 5,L
				self.SET(5, self.L)
			elif arg == "EE":		#SET 5,(HL)
				self.write(self.HL, self.SET(5, self.read(self.HL)))
			elif arg == "EF":		#SET 5,A
				self.SET(5, self.A)
			elif arg == "F0":		#SET 6,B
				self.SET(6, self.B)
			elif arg == "F1":		#SET 6,C
				self.SET(6, self.C)
			elif arg == "F2":		#SET 6,D
				self.SET(6, self.D)
			elif arg == "F3":		#SET 6,E
				self.SET(6, self.E)
			elif arg == "F4":		#SET 6,H
				self.SET(6, self.H)
			elif arg == "F5":		#SET 6,L
				self.SET(6, self.L)
			elif arg == "F6":		#SET 6,(HL)
				self.write(self.HL, self.SET(6, self.read(self.HL)))
			elif arg == "F7":		#SET 6,A
				self.SET(6, self.A)
			elif arg == "F8":		#SET 7,B
				self.SET(7, self.B)
			elif arg == "F9":		#SET 7,C
				self.SET(7, self.C)
			elif arg == "FA":		#SET 7,D
				self.SET(7, self.D)
			elif arg == "FB":		#SET 7,E
				self.SET(7, self.E)
			elif arg == "FC":		#SET 7,H
				self.SET(7, self.H)
			elif arg == "FD":		#SET 7,L
				self.SET(7, self.L)
			elif arg == "FE":		#SET 7,(HL)
				self.write(self.HL, self.SET(7, self.read(self.HL)))
			elif arg == "FF":		#SET 7,A
				self.SET(7, self.A)
		else:
			("UNKNOWN OPCODE: {0}".format(opcode))
'''