from binary import Bin
from binary import Bin16
from memory import Memory

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

						#[7,6,5,4]		#[7,6,5,4]
	def flagUpdate(self, flagsToAffect, flags):
		for i in range(4):
			if flagsToAffect[i]:
				self.F[7-i] = flags[i]

	def add(self, a, b, flagsToAffect, c=0):
		flagRegister = [0,0,0,0]
		n, temp, half, carry = 8, Bin(), 3, 7
		if isinstance(a, Bin16) or isinstance(b, Bin16):
			n, temp, half, carry = 16, Bin16(), 11, 15
		for i in range(8):
			temp[i], c = Bin.fullAdder(a[i], b[i], c)
			if i == half:
				flagRegister[2] = c
			elif i == carry:
				flagRegister[3] = c
		if temp.toDecimal() == 0:
			flagRegister[0] = 1
		self.flagUpdate(flagsToAffect, flagRegister)
		return temp

	def sub(self, a, b, flagsToAffect, B=0):
		flagRegister = [0,1,0,0]
		n, temp, half, carry = 8, Bin(), 3, 7
		if isinstance(a, Bin16) or isinstance(b, Bin16):
			n, temp, half, carry = 16, Bin16(), 11, 15
		for i in range(8):
			temp[i], B = Bin.fullSubber(a[i], b[i], B)
			if i == half:
				flagRegister[2] = B
			elif i == carry:
				flagRegister[3] = B
		if temp.toDecimal() == 0:
			flagRegister[0] = 1
		self.flagUpdate(flagsToAffect, flagRegister)
		return temp

	def ADD(self, x, y):	#ADD x,y
		return self.add(x, y, [1,1,1,1])

	def ADC(self, x, y):	#ADC x,y
		return self.add(x, y, [1,1,1,1], self.F[4])

	def SUB(self, x, y):	#SUB x,y
		return self.sub(x, y, [1,1,1,1])

	def SBC(self, x, y):	#SBC x,y
		return self.sub(x, y, [1,1,1,1], self.F[4])

	def AND(self, x, y):
		self.F[7] = 1 if  x & y == Bin("00000000") else 0
		self.F[6] = 0
		self.F[5] = 1
		self.F[4] = 0
		return x & y

	def OR(self, x, y):
		self.F[7] = 1 if x | y == Bin("00000000") else 0
		self.F[6] = 0
		self.F[5] = 0
		self.F[4] = 0
		return x | y

	def XOR(self, x, y):
		self.F[7] = 1 if x | y == Bin("00000000") else 0
		self.F[6] = 0
		self.F[5] = 0
		self.F[4] = 0
		return x | y

	def CP(self, x, y):
		return self.SUB(x, y)

	def INC(self, x):
		if isinstance(x, Bin16):
			return self.add(x, Bin.fromDecimal(1), [0,0,0,0])
		return self.add(x, Bin.fromDecimal(1), [1,1,1,0])

	def DEC(self, x):
		if isinstance(x, Bin16):
			return self.sub(x, Bin.fromDecimal(1), [0,0,0,0])
		return self.sub(x, Bin.fromDecimal(1), [1,1,1,0])

	def ADD_HL(self, x, y):
		return self.add(x, y, [0,1,1,1])

	def ADD_SP(self, x, y):
		a = self.add(x, y, [0,1,1,1])
		self.F[7] = 0
		return a

	def SWAP(self, x):
		temp = Bin()
		for i in range(4):
			temp[7-i] = x[3-i]
			temp[4-i] = x[7-i]
		if temp.toDecimal() == 0:
			self.F[7] = 0
		self.F[6] = self.F[5] = self.F[4] = 0
		return temp

	def DAA(self, x):
		if self.F[6]:
			if self.F[4] or x > Bin("99"):
				x = x + Bin("60")
				self.F[4] = 1
			if self.F[5] or (x & Bin("0F") > Bin("09")):
				x = x + Bin("06")
		else:
			if self.F[4]:
				x = x - Bin("60")
			if self.F[5]:
				x = x - Bin("06")
		self.F[7] = 1 if x == Bin("00000000") else 0
		self.F[5] = 0
		return x

	def CCF(self):
		self.F[6] = self.F[5] = 0
		self.F[4] = 0 if self.F[4] else 1

	def SCF(self):
		self.F[4] = 1
		self.F[6] = self.F[5] = 0

	def ADD_E(self, n, big):
		if n[7]:
			a = Bin16(Bin("FF"), n)
			return big - (~a+1)
		else:
			return big + n

class CPU():
	def __init__(self):
		super().__setattr__("A", Bin("11"))
		super().__setattr__("B", Bin("00"))
		super().__setattr__("C", Bin("00"))
		super().__setattr__("D", Bin("FF"))
		super().__setattr__("E", Bin("56"))
		super().__setattr__("F", Bin("80"))
		super().__setattr__("H", Bin("00"))
		super().__setattr__("L", Bin("0D"))
		super().__setattr__("programCounter", Bin16.fromHex("0100"))
		super().__setattr__("stackPointer", Bin16.fromHex("FFFE"))
		super().__setattr__("memoryBus", Memory())
		super().__setattr__("ALU", ALU(self.F))
		super().__setattr__("opcodes", {
			"06": self.LDrn_B,
			"0E": self.LDrn_C,
			"16": self.LDrn_D,
			"1E": self.LDrn_E,
			"26": self.LDrn_H,
			"2E": self.LDrn_L,
			"7F": self.LDrr_AA,
			"78": self.LDrr_AB,
			"79": self.LDrr_AC,
			"7A": self.LDrr_AD,
			"7B": self.LDrr_AE,
			"7C": self.LDrr_AH,
			"7D": self.LDrr_AL,
			"40": self.LDrr_BB,
			"41": self.LDrr_BC,
			"42": self.LDrr_BD,
			"43": self.LDrr_BE,
			"44": self.LDrr_BH,
			"45": self.LDrr_BL,
			"46": self.LDrHL_B,
			"47": self.LDrr_BA,
			"48": self.LDrr_CB,
			"49": self.LDrr_CC,
			"4A": self.LDrr_CD,
			"4B": self.LDrr_CE,
			"4C": self.LDrr_CH,
			"4D": self.LDrr_CL,
			"4E": self.LDrHL_C,
			"4F": self.LDrr_CA,
			"50": self.LDrr_DB,
			"51": self.LDrr_DC,
			"52": self.LDrr_DD,
			"53": self.LDrr_DE,
			"54": self.LDrr_DH,
			"55": self.LDrr_DL,
			"56": self.LDrHL_D,
			"57": self.LDrr_DA,
			"58": self.LDrr_EB,
			"59": self.LDrr_EC,
			"5A": self.LDrr_ED,
			"5B": self.LDrr_EE,
			"5C": self.LDrr_EH,
			"5D": self.LDrr_EL,
			"5E": self.LDrHL_E,
			"5F": self.LDrr_EA,
			"60": self.LDrr_HB,
			"61": self.LDrr_HC,
			"62": self.LDrr_HD,
			"63": self.LDrr_HE,
			"64": self.LDrr_HH,
			"65": self.LDrr_HL,
			"66": self.LDrHL_H,
			"67": self.LDrr_HA,
			"68": self.LDrr_LB,
			"69": self.LDrr_LL,
			"6A": self.LDrr_LD,
			"6B": self.LDrr_LE,
			"6L": self.LDrr_LH,
			"6D": self.LDrr_LL,
			"6E": self.LDrHL_L,
			"6F": self.LDrr_LA,
			"70": self.LDHLr_B,
			"71": self.LDHLr_C,
			"72": self.LDHLr_D,
			"73": self.LDHLr_E,
			"74": self.LDHLr_H,
			"75": self.LDHLr_L,
			"76": self.LDHLr_n,
			"0A": self.LDrBC_A,
			"1A": self.LDrDE_A,
			"7E": self.LDrHL_A,
			"FA": self.LDrNN_A,
			"3E": self.LDrN_A,
			"02": self.LDBCr_A,
			"12": self.LDDEr_A,
			"77": self.LDHLr_A,
			"EA": self.LDNNr_A,
			"F2": self.LDrC_A,
			"E2": self.LDAr_C,
			"3A": self.LDDrHL_A,
			"32": self.LDHLr_A,
			"2A": self.LDIrHL_A,
			"22": self.LDIHLr_A,
			"E0": self.LDHnr_A,
			"F0": self.LDHrn_A,
			"01": self.LDnnrr_BC,
			"11": self.LDnnrr_DE,
			"21": self.LDnnrr_HL,
			"31": self.LDnnSP,
			"F9": self.LDrrSD_HL,
			"F8": self.LDHLnr_SP,
			"08": self.LDSPnn,
			"F5": self.PUSH_AF,
			"C5": self.PUSH_BC,
			"D5": self.PUSH_DE,
			"E5": self.PUSH_HL,
			"F1": self.POP_AF,
			"C1": self.POP_BC,
			"D1": self.POP_DE,
			"E1": self.POP_HL,
			"87": self.ADDr_A,
			"80": self.ADDr_B,
			"81": self.ADDr_C,
			"82": self.ADDr_D,
			"83": self.ADDr_E,
			"84": self.ADDr_H,
			"85": self.ADDr_L,
			"86": self.ADDr_HL,
			"C6": self.ADDrn,
			"8F": self.ADCr_A,
			"88": self.ADCr_B,
			"89": self.ADCr_C,
			"8A": self.ADCr_D,
			"8B": self.ADCr_E,
			"8C": self.ADCr_H,
			"8D": self.ADCr_L,
			"8E": self.ADCr_HL,
			"CE": self.ADCrn,
			"97": self.SUBr_A,
			"90": self.SUBr_B,
			"91": self.SUBr_C,
			"92": self.SUBr_D,
			"93": self.SUBr_E,
			"94": self.SUBr_H,
			"95": self.SUBr_L,
			"96": self.SUBr_HL,
			"D6": self.SUBrn,
			"9F": self.SBCr_A,
			"99": self.SBCr_B,
			"99": self.SBCr_C,
			"9A": self.SBCr_D,
			"9B": self.SBCr_E,
			"9D": self.SBCr_H,
			"9D": self.SBCr_L,
			"9E": self.SBCr_HL,
			"A7": self.ANDr_A,
			"A0": self.ANDr_B,
			"A1": self.ANDr_C,
			"A2": self.ANDr_D,
			"A3": self.ANDr_E,
			"A4": self.ANDr_H,
			"A5": self.ANDr_L,
			"A6": self.ANDr_HL,
			"E6": self.ANDrn,
			"B7": self.ORr_A,
			"B0": self.ORr_B,
			"B1": self.ORr_C,
			"B2": self.ORr_D,
			"B3": self.ORr_E,
			"B4": self.ORr_H,
			"B5": self.ORr_L,
			"B6": self.ORr_HL,
			"F6": self.ORrn,
			"AF": self.XORr_A,
			"A8": self.XORr_B,
			"A9": self.XORr_C,
			"AA": self.XORr_D,
			"AB": self.XORr_E,
			"AC": self.XORr_H,
			"AD": self.XORr_L,
			"AE": self.XORr_HL,
			"EE": self.XORrn,
			"BF": self.CPr_A,
			"B8": self.CPr_B,
			"B9": self.CPr_C,
			"BA": self.CPr_D,
			"BB": self.CPr_E,
			"BC": self.CPr_H,
			"BD": self.CPr_L,
			"BE": self.CPr_HL,
			"FE": self.CPrn,
			"3C": self.INC_A,
			"04": self.INC_B,
			"0C": self.INC_C,
			"14": self.INC_D,
			"1C": self.INC_E,
			"24": self.INC_H,
			"2C": self.INC_L,
			"34": self.INC_HL,
			"3D": self.DEC_A,
			"05": self.DEC_B,
			"0D": self.DEC_C,
			"15": self.DEC_D,
			"1D": self.DEC_E,
			"25": self.DEC_H,
			"2D": self.DEC_L,
			"35": self.DEC_HL,
			"09": self.ADDHLBC,
			"19": self.ADDHLDE,
			"29": self.ADDHLHL,
			"39": self.ADDHLSP,
			"E8": self.ADDSPnn,
			"03": self.INC_BC,
			"13": self.INC_DE,
			"23": self.INC_HL,
			"33": self.INC_SP,
			"0B": self.DEC_BC,
			"1B": self.DEC_DE,
			"2B": self.DEC_HL,
			"3B": self.DEC_SP,
			"27": self.DAA,
			"3F": self.CCF,
			"37": self.SCF,
			"00": self.testShit,
			"76": self.testShit,
			"10": self.fetch,
			"F3": self.testShit,
			"FB": self.testShit,
			"07": self.RLCA,
			"17": self.RLA,
			"0F": self.RRCA,
			"1F": self.RRA,
			"C3": self.JPnn,
			"C2": self.JPnn_NZ,
			"CA": self.JPnn_Z,
			"D2": self.JPnn_NC,
			"DA": self.JPnn_C,
			"E9": self.JP_HL,
			"18": self.JRnn,
			"20": self.JRnn_NZ,
			"28": self.JRnn_Z,
			"30": self.JRnn_NC,
			"38": self.JRnn_C,
			"CD": self.CALLnn,
			"C4": self.CALLnn_NZ,
			"CC": self.CALLnn_Z,
			"D4": self.CALLnn_NC,
			"DC": self.CALLnn_C,
			"C7": self.RST_00,
			"CF": self.RST_08,
			"D7": self.RST_10,
			"DF": self.RST_18,
			"E7": self.RST_20,
			"EF": self.RST_28,
			"F7": self.RST_30,
			"FF": self.RST_38
		})
		super().__setattr__("CBopcodes", {
			"37": self.SWAP_A,
			"30": self.SWAP_B,
			"31": self.SWAP_C,
			"32": self.SWAP_D,
			"33": self.SWAP_E,
			"34": self.SWAP_H,
			"35": self.SWAP_L,
			"36": self.SWAP_HL,
			"07": self.RLC_A,
			"00": self.RLC_B,
			"01": self.RLC_C,
			"02": self.RLC_D,
			"03": self.RLC_E,
			"04": self.RLC_H,
			"05": self.RLC_L,
			"06": self.RLC_HL,
			"17": self.RL_A,
			"10": self.RL_B,
			"11": self.RL_C,
			"12": self.RL_D,
			"13": self.RL_E,
			"14": self.RL_H,
			"15": self.RL_L,
			"16": self.RL_HL,
			"0F": self.RRC_A,
			"08": self.RRC_B,
			"09": self.RRC_C,
			"0A": self.RRC_D,
			"0B": self.RRC_E,
			"0C": self.RRC_H,
			"0D": self.RRC_L,
			"0E": self.RRC_HL,
			"1F": self.RR_A,
			"18": self.RR_B,
			"19": self.RR_C,
			"1A": self.RR_D,
			"1B": self.RR_E,
			"1C": self.RR_H,
			"1D": self.RR_L,
			"1E": self.RR_HL,
			"27": self.SLA_A,
			"20": self.SLA_B,
			"21": self.SLA_C,
			"22": self.SLA_D,
			"23": self.SLA_E,
			"24": self.SLA_H,
			"25": self.SLA_L,
			"26": self.SLA_HL,
			"2F": self.SRA_A,
			"28": self.SRA_B,
			"29": self.SRA_C,
			"2A": self.SRA_D,
			"2B": self.SRA_E,
			"2C": self.SRA_H,
			"2D": self.SRA_L,
			"2E": self.SRA_HL,
			"3F": self.SRL_A,
			"38": self.SRL_B,
			"39": self.SRL_C,
			"3A": self.SRL_D,
			"3B": self.SRL_E,
			"3C": self.SRL_H,
			"3D": self.SRL_L,
			"3E": self.SRL_HL,
			"40": self.BIT0_B,
			"41": self.BIT0_C,
			"42": self.BIT0_D,
			"43": self.BIT0_E,
			"44": self.BIT0_H,
			"45": self.BIT0_L,
			"46": self.BIT0_HL,
			"47": self.BIT0_A,
			"48": self.BIT1_B,
			"49": self.BIT1_C,
			"4A": self.BIT1_D,
			"4B": self.BIT1_E,
			"4C": self.BIT1_H,
			"4D": self.BIT1_L,
			"4E": self.BIT1_HL,
			"4F": self.BIT1_A,
			"40": self.BIT0_B,
			"41": self.BIT0_C,
			"42": self.BIT0_D,
			"43": self.BIT0_E,
			"44": self.BIT0_H,
			"45": self.BIT0_L,
			"46": self.BIT0_HL,
			"47": self.BIT0_A,
			"48": self.BIT1_B,
			"49": self.BIT1_C,
			"4A": self.BIT1_D,
			"4B": self.BIT1_E,
			"4C": self.BIT1_H,
			"4D": self.BIT1_L,
			"4E": self.BIT1_HL,
			"4F": self.BIT1_A,
			"50": self.BIT2_B,
			"51": self.BIT2_C,
			"52": self.BIT2_D,
			"53": self.BIT2_E,
			"55": self.BIT2_H,
			"55": self.BIT2_L,
			"56": self.BIT2_HL,
			"57": self.BIT2_A,
			"58": self.BIT3_B,
			"59": self.BIT3_C,
			"5A": self.BIT3_D,
			"5B": self.BIT3_E,
			"5C": self.BIT3_H,
			"5D": self.BIT3_L,
			"5E": self.BIT3_HL,
			"5F": self.BIT3_A,
			"60": self.BIT4_B,
			"61": self.BIT4_C,
			"62": self.BIT4_D,
			"63": self.BIT4_E,
			"65": self.BIT4_H,
			"65": self.BIT4_L,
			"66": self.BIT4_HL,
			"67": self.BIT4_A,
			"68": self.BIT5_B,
			"69": self.BIT5_C,
			"6A": self.BIT5_D,
			"6B": self.BIT5_E,
			"6C": self.BIT5_H,
			"6D": self.BIT5_L,
			"6E": self.BIT5_HL,
			"6F": self.BIT5_A,
			"70": self.BIT6_B,
			"71": self.BIT6_C,
			"72": self.BIT6_D,
			"73": self.BIT6_E,
			"75": self.BIT6_H,
			"75": self.BIT6_L,
			"76": self.BIT6_HL,
			"77": self.BIT6_A,
			"78": self.BIT7_B,
			"79": self.BIT7_C,
			"7A": self.BIT7_D,
			"7B": self.BIT7_E,
			"7C": self.BIT7_H,
			"7D": self.BIT7_L,
			"7E": self.BIT7_HL,
			"7F": self.BIT7_A,
			"80": self.RES0_B,
			"81": self.RES0_C,
			"82": self.RES0_D,
			"83": self.RES0_E,
			"84": self.RES0_H,
			"85": self.RES0_L,
			"86": self.RES0_HL,
			"87": self.RES0_A,
			"88": self.RES1_B,
			"89": self.RES1_C,
			"8A": self.RES1_D,
			"8B": self.RES1_E,
			"8C": self.RES1_H,
			"8D": self.RES1_L,
			"8E": self.RES1_HL,
			"8F": self.RES1_A,
			"90": self.RES2_B,
			"91": self.RES2_C,
			"92": self.RES2_D,
			"93": self.RES2_E,
			"94": self.RES2_H,
			"95": self.RES2_L,
			"96": self.RES2_HL,
			"97": self.RES2_A,
			"98": self.RES3_B,
			"99": self.RES3_C,
			"9A": self.RES3_D,
			"9B": self.RES3_E,
			"9C": self.RES3_H,
			"9D": self.RES3_L,
			"9E": self.RES3_HL,
			"9F": self.RES3_A,
			"A0": self.RES4_B,
			"A1": self.RES4_C,
			"A2": self.RES4_D,
			"A3": self.RES4_E,
			"A4": self.RES4_H,
			"A5": self.RES4_L,
			"A6": self.RES4_HL,
			"A7": self.RES4_A,
			"AA": self.RES5_B,
			"A9": self.RES5_C,
			"AA": self.RES5_D,
			"AB": self.RES5_E,
			"AC": self.RES5_H,
			"AD": self.RES5_L,
			"AE": self.RES5_HL,
			"AF": self.RES5_A,
			"B0": self.RES6_B,
			"B1": self.RES6_C,
			"B2": self.RES6_D,
			"B3": self.RES6_E,
			"B4": self.RES6_H,
			"B5": self.RES6_L,
			"B6": self.RES6_HL,
			"B7": self.RES6_A,
			"B8": self.RES7_B,
			"B9": self.RES7_C,
			"BA": self.RES7_D,
			"BB": self.RES7_E,
			"BC": self.RES7_H,
			"BD": self.RES7_L,
			"BE": self.RES7_HL,
			"BF": self.RES7_A,
			"C0": self.SET0_B,
			"C1": self.SET0_C,
			"C2": self.SET0_D,
			"C3": self.SET0_E,
			"C4": self.SET0_H,
			"C5": self.SET0_L,
			"C6": self.SET0_HL,
			"C7": self.SET0_A,
			"C8": self.SET1_B,
			"C9": self.SET1_C,
			"CA": self.SET1_D,
			"CB": self.SET1_E,
			"CC": self.SET1_H,
			"CD": self.SET1_L,
			"CE": self.SET1_HL,
			"CF": self.SET1_A,
			"D0": self.SET2_B,
			"D1": self.SET2_C,
			"D2": self.SET2_D,
			"D3": self.SET2_E,
			"D4": self.SET2_H,
			"D5": self.SET2_L,
			"D6": self.SET2_HL,
			"D7": self.SET2_A,
			"D8": self.SET3_B,
			"D9": self.SET3_C,
			"DA": self.SET3_D,
			"DB": self.SET3_E,
			"DC": self.SET3_H,
			"DD": self.SET3_L,
			"DE": self.SET3_HL,
			"DF": self.SET3_A,
			"E0": self.SET4_B,
			"E1": self.SET4_C,
			"E2": self.SET4_D,
			"E3": self.SET4_E,
			"E4": self.SET4_H,
			"E5": self.SET4_L,
			"E6": self.SET4_HL,
			"E7": self.SET4_A,
			"E8": self.SET5_B,
			"E9": self.SET5_C,
			"EA": self.SET5_D,
			"EB": self.SET5_E,
			"EC": self.SET5_H,
			"ED": self.SET5_L,
			"EE": self.SET5_HL,
			"EF": self.SET5_A,
			"F0": self.SET6_B,
			"F1": self.SET6_C,
			"F2": self.SET6_D,
			"F3": self.SET6_E,
			"F4": self.SET6_H,
			"F5": self.SET6_L,
			"F6": self.SET6_HL,
			"F7": self.SET6_A,
			"F8": self.SET7_B,
			"F9": self.SET7_C,
			"FA": self.SET7_D,
			"FB": self.SET7_E,
			"FC": self.SET7_H,
			"FD": self.SET7_L,
			"FE": self.SET7_HL,
			"FF": self.SET7_A,
		})

	def __setattr__(self, name, value):
		if name in ["AF", "BC", "DE", "HL"]:
			a,b = value.array[0], value.array[1]
			self.__dict__[name[0]].array = a.array
			self.__dict__[name[1]].array = b.array
		else:
			self.__dict__[name].array = value.array

	def __getattribute__(self, name):
		if name == "AF":
			return Bin16(self.A, self.F)
		elif name == "BC":
			return Bin16(self.B, self.C)
		elif name == "DE":
			return Bin16(self.D, self.E)
		elif name == "HL":
			return Bin16(self.H, self.L)
		return super().__getattribute__(name)

	def read(self, address):
		if isinstance(address, Bin):
			address = Bin16(Bin.fromHex("FF"), address)
		a = self.memoryBus[address]
		return a

	def load(self, file):
		self.memoryBus.load(file)

	def write(self, address, value):
		if address.toHex() == "FF02" and value.toHex() == "81":
			print(self.read(Bin16.fromHex("FF01")))
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

	def LDrn_B(self): self.B = self.fetch()
	def LDrn_C(self): self.C = self.fetch()
	def LDrn_D(self): self.D = self.fetch()
	def LDrn_E(self): self.E = self.fetch()
	def LDrn_H(self): self.H = self.fetch()
	def LDrn_L(self): self.L = self.fetch()
	def LDrr_AA(self): self.A = self.A
	def LDrr_AB(self): self.A = self.B
	def LDrr_AC(self): self.A = self.C
	def LDrr_AD(self): self.A = self.D
	def LDrr_AE(self): self.A = self.E
	def LDrr_AH(self): self.A = self.H
	def LDrr_AL(self): self.A = self.L
	def LDrr_BA(self): self.B = self.A
	def LDrr_BB(self): self.B = self.B
	def LDrr_BC(self): self.B = self.C
	def LDrr_BD(self): self.B = self.D
	def LDrr_BE(self): self.B = self.E
	def LDrr_BH(self): self.B = self.H
	def LDrr_BL(self): self.B = self.L
	def LDrr_CA(self): self.C = self.A
	def LDrr_CB(self): self.C = self.B
	def LDrr_CC(self): self.C = self.C
	def LDrr_CD(self): self.C = self.D
	def LDrr_CE(self): self.C = self.E
	def LDrr_CH(self): self.C = self.H
	def LDrr_CL(self): self.C = self.L
	def LDrr_DA(self): self.D = self.A
	def LDrr_DB(self): self.D = self.B
	def LDrr_DC(self): self.D = self.C
	def LDrr_DD(self): self.D = self.D
	def LDrr_DE(self): self.D = self.E
	def LDrr_DH(self): self.D = self.H
	def LDrr_DL(self): self.D = self.L
	def LDrr_EA(self): self.E = self.A
	def LDrr_EB(self): self.E = self.B
	def LDrr_EC(self): self.E = self.C
	def LDrr_ED(self): self.E = self.D
	def LDrr_EE(self): self.E = self.E
	def LDrr_EH(self): self.E = self.H
	def LDrr_EL(self): self.E = self.L
	def LDrr_HA(self): self.H = self.A
	def LDrr_HB(self): self.H = self.B
	def LDrr_HC(self): self.H = self.C
	def LDrr_HD(self): self.H = self.D
	def LDrr_HE(self): self.H = self.E
	def LDrr_HH(self): self.H = self.H
	def LDrr_HL(self): self.H = self.L
	def LDrr_LA(self): self.L = self.A
	def LDrr_LB(self): self.L = self.B
	def LDrr_LC(self): self.L = self.C
	def LDrr_LD(self): self.L = self.D
	def LDrr_LE(self): self.L = self.E
	def LDrr_LH(self): self.L = self.H
	def LDrr_LL(self): self.L = self.L
	def LDrHL_B(self): self.B = self.read(self.HL)
	def LDrHL_C(self): self.C = self.read(self.HL)
	def LDrHL_D(self): self.D = self.read(self.HL)
	def LDrHL_E(self): self.E = self.read(self.HL)
	def LDrHL_F(self): self.F = self.read(self.HL)
	def LDrHL_H(self): self.H = self.read(self.HL)
	def LDrHL_L(self): self.L = self.read(self.HL)
	def LDHLr_B(self): self.write(self.HL, self.B)
	def LDHLr_C(self): self.write(self.HL, self.C)
	def LDHLr_D(self): self.write(self.HL, self.D)
	def LDHLr_E(self): self.write(self.HL, self.E)
	def LDHLr_F(self): self.write(self.HL, self.F)
	def LDHLr_H(self): self.write(self.HL, self.H)
	def LDHLr_L(self): self.write(self.HL, self.L)
	def LDHLr_n(self): self.write(self.HL, self.fetch())
	def LDrBC_A(self): self.A = self.read(self.BC)
	def LDrDE_A(self): self.A = self.read(self.DE)
	def LDrHL_A(self): self.A = self.read(self.HL)
	def LDrNN_A(self): self.A = self.read(self.fetch16())
	def LDrN_A(self): self.A = self.fetch()
	def LDBCr_A(self): self.write(self.BC, self.A)
	def LDDEr_A(self): self.write(self.DE, self.A)
	def LDHLr_A(self): self.write(self.HL, self.A)
	def LDNNr_A(self): self.write(self.fetch16(), self.A)
	def LDrC_A(self): self.A = self.read(self.C)
	def LDAr_C(self): self.write(self.C, self.A)
	def LDDrHL_A(self):
		self.A = self.read(self.HL)
		self.HL -= 1
	def LDDHLr_A(self):
		self.write(self.HL, self.A)
		self.HL -= 1
	def LDIrHL_A(self):
		self.A = self.read(self.HL)
		self.HL += 1
	def LDIHLr_A(self):
		self.write(self.HL, self.A)
		self.HL += 1
	def LDHnr_A(self): self.write(self.fetch(), self.A)
	def LDHrn_A(self): self.A = self.read(self.fetch())

	#16 bit loads
	def LDnnrr_BC(self): self.BC = self.fetch16()
	def LDnnrr_DE(self): self.DE = self.fetch16()
	def LDnnrr_HL(self): self.HL = self.fetch16()
	def LDnnSP(self): self.stackPointer = self.fetch16()
	def LDrrSD_HL(self): self.stackPointer = self.HL
	def LDHLnr_SP(self): #fix name
		self.HL = self.ALU.add(self.stackPointer, self.fetch(), [0,0,1,1])
	def LDSPnn(self): self.write(self.fetch16(), self.stackPointer)
	def PUSH_AF(self):
		self.stackPointer -= 1
		self.write(self.stackPointer, self.A)
		self.stackPointer -= 1
		self.write(self.stackPointer, self.F)
	def PUSH_BC(self):	#PUSH BC
		self.stackPointer -= 1
		self.write(self.stackPointer, self.B)
		self.stackPointer -= 1
		self.write(self.stackPointer, self.C)
	def PUSH_DE(self):	#PUSH DE
		self.stackPointer -= 1
		self.write(self.stackPointer, self.D)
		self.stackPointer -= 1
		self.write(self.stackPointer, self.E)
	def PUSH_HL(self):	#PUSH HL
		self.stackPointer -= 1
		self.write(self.stackPointer, self.H)
		self.stackPointer -= 1
		self.write(self.stackPointer, self.L)
	def POP_AF(self):	#POP AF
		self.F = self.read(self.stackPointer)
		self.stackPointer += 1
		self.A = self.read(self.stackPointer)
		self.stackPointer += 1
	def POP_BC(self):	#POP BC
		self.C = self.read(self.stackPointer)
		self.stackPointer += 1
		self.B = self.read(self.stackPointer)
		self.stackPointer += 1
	def POP_DE(self):	#POP DE
		self.E = self.read(self.stackPointer)
		self.stackPointer += 1
		self.D = self.read(self.stackPointer)
		self.stackPointer += 1
	def POP_HL(self):	#POP HL
		self.L = self.read(self.stackPointer)
		self.stackPointer += 1
		self.H = self.read(self.stackPointer)
		self.stackPointer += 1

	#8 bit alu
	def ADDr_A(self): self.A = self.ALU.ADD(self.A, self.A)
	def ADDr_B(self): self.A = self.ALU.ADD(self.A, self.B)
	def ADDr_C(self): self.A = self.ALU.ADD(self.A, self.C)
	def ADDr_D(self): self.A = self.ALU.ADD(self.A, self.D)
	def ADDr_E(self): self.A = self.ALU.ADD(self.A, self.E)
	def ADDr_H(self): self.A = self.ALU.ADD(self.A, self.H)
	def ADDr_L(self): self.A = self.ALU.ADD(self.A, self.L)
	def ADDr_HL(self): self.A = self.ALU.ADD(self.A, self.read(self.HL))
	def ADDrn(self): self.A = self.ALU.ADD(self.A, self.fetch())
	def ADCr_A(self): self.A = self.ALU.ADC(self.A, self.A)
	def ADCr_B(self): self.A = self.ALU.ADC(self.A, self.B)
	def ADCr_C(self): self.A = self.ALU.ADC(self.A, self.C)
	def ADCr_D(self): self.A = self.ALU.ADC(self.A, self.D)
	def ADCr_E(self): self.A = self.ALU.ADC(self.A, self.E)
	def ADCr_F(self): self.A = self.ALU.ADC(self.A, self.F)
	def ADCr_H(self): self.A = self.ALU.ADC(self.A, self.H)
	def ADCr_L(self): self.A = self.ALU.ADC(self.A, self.L)
	def ADCr_HL(self): self.A = self.ALU.ADC(self.A, self.read(self.HL))
	def ADCrn(self): self.A = self.ALU.ADC(self.A, self.fetch())
	def SUBr_A(self): self.A = self.ALU.SUB(self.A, self.A)
	def SUBr_B(self): self.A = self.ALU.SUB(self.A, self.B)
	def SUBr_C(self): self.A = self.ALU.SUB(self.A, self.C)
	def SUBr_D(self): self.A = self.ALU.SUB(self.A, self.D)
	def SUBr_E(self): self.A = self.ALU.SUB(self.A, self.E)
	def SUBr_F(self): self.A = self.ALU.SUB(self.A, self.F)
	def SUBr_H(self): self.A = self.ALU.SUB(self.A, self.H)
	def SUBr_L(self): self.A = self.ALU.SUB(self.A, self.L)
	def SUBr_HL(self): self.A = self.ALU.SUB(self.A, self.read(self.HL))
	def SUBrn(self): self.A = self.ALU.SUB(self.A, self.fetch())
	def SBCr_A(self): self.A = self.ALU.SBC(self.A, self.A)
	def SBCr_B(self): self.A = self.ALU.SBC(self.A, self.B)
	def SBCr_C(self): self.A = self.ALU.SBC(self.A, self.C)
	def SBCr_D(self): self.A = self.ALU.SBC(self.A, self.D)
	def SBCr_E(self): self.A = self.ALU.SBC(self.A, self.E)
	def SBCr_F(self): self.A = self.ALU.SBC(self.A, self.F)
	def SBCr_H(self): self.A = self.ALU.SBC(self.A, self.H)
	def SBCr_L(self): self.A = self.ALU.SBC(self.A, self.L)
	def SBCr_HL(self): self.A = self.ALU.SBC(self.A, self.read(self.HL))
	def SBCrn(self): self.A = self.ALU.SBC(self.A, self.fetch())
	def ANDr_A(self): self.A = self.ALU.AND(self.A, self.A)
	def ANDr_B(self): self.A = self.ALU.AND(self.A, self.B)
	def ANDr_C(self): self.A = self.ALU.AND(self.A, self.C)
	def ANDr_D(self): self.A = self.ALU.AND(self.A, self.D)
	def ANDr_E(self): self.A = self.ALU.AND(self.A, self.E)
	def ANDr_F(self): self.A = self.ALU.AND(self.A, self.F)
	def ANDr_H(self): self.A = self.ALU.AND(self.A, self.H)
	def ANDr_L(self): self.A = self.ALU.AND(self.A, self.L)
	def ANDr_HL(self): self.A = self.ALU.AND(self.A, self.read(self.HL))
	def ANDrn(self): self.A = self.ALU.AND(self.A, self.fetch())
	def ORr_A(self): self.A = self.ALU.OR(self.A, self.A)
	def ORr_B(self): self.A = self.ALU.OR(self.A, self.B)
	def ORr_C(self): self.A = self.ALU.OR(self.A, self.C)
	def ORr_D(self): self.A = self.ALU.OR(self.A, self.D)
	def ORr_E(self): self.A = self.ALU.OR(self.A, self.E)
	def ORr_F(self): self.A = self.ALU.OR(self.A, self.F)
	def ORr_H(self): self.A = self.ALU.OR(self.A, self.H)
	def ORr_L(self): self.A = self.ALU.OR(self.A, self.L)
	def ORr_HL(self): self.A = self.ALU.OR(self.A, self.read(self.HL))
	def ORrn(self): self.A = self.ALU.OR(self.A, self.fetch())
	def XORr_A(self): self.A = self.ALU.XOR(self.A, self.A)
	def XORr_B(self): self.A = self.ALU.XOR(self.A, self.B)
	def XORr_C(self): self.A = self.ALU.XOR(self.A, self.C)
	def XORr_D(self): self.A = self.ALU.XOR(self.A, self.D)
	def XORr_E(self): self.A = self.ALU.XOR(self.A, self.E)
	def XORr_F(self): self.A = self.ALU.XOR(self.A, self.F)
	def XORr_H(self): self.A = self.ALU.XOR(self.A, self.H)
	def XORr_L(self): self.A = self.ALU.XOR(self.A, self.L)
	def XORr_HL(self): self.A = self.ALU.XOR(self.A, self.read(self.HL))
	def XORrn(self): self.A = self.ALU.XOR(self.A, self.fetch())
	def CPr_A(self): self.A = self.ALU.CP(self.A, self.A)
	def CPr_B(self): self.A = self.ALU.CP(self.A, self.B)
	def CPr_C(self): self.A = self.ALU.CP(self.A, self.C)
	def CPr_D(self): self.A = self.ALU.CP(self.A, self.D)
	def CPr_E(self): self.A = self.ALU.CP(self.A, self.E)
	def CPr_F(self): self.A = self.ALU.CP(self.A, self.F)
	def CPr_H(self): self.A = self.ALU.CP(self.A, self.H)
	def CPr_L(self): self.A = self.ALU.CP(self.A, self.L)
	def CPr_HL(self): self.A = self.ALU.CP(self.A, self.read(self.HL))
	def CPrn(self): self.A = self.ALU.CP(self.A, self.fetch())
	def INC_A(self): self.A = self.ALU.INC(self.A)
	def INC_B(self): self.A = self.ALU.INC(self.A)
	def INC_C(self): self.A = self.ALU.INC(self.A)
	def INC_D(self): self.A = self.ALU.INC(self.A)
	def INC_E(self): self.A = self.ALU.INC(self.A)
	def INC_F(self): self.A = self.ALU.INC(self.A)
	def INC_H(self): self.A = self.ALU.INC(self.A)
	def INC_L(self): self.A = self.ALU.INC(self.A)
	def INC_HL(self): self.write(self.read(self.HL), self.ALU.INC(self.read(self.HL)))
	def DEC_A(self): self.A = self.ALU.DEC(self.A)
	def DEC_B(self): self.A = self.ALU.DEC(self.A)
	def DEC_C(self): self.A = self.ALU.DEC(self.A)
	def DEC_D(self): self.A = self.ALU.DEC(self.A)
	def DEC_E(self): self.A = self.ALU.DEC(self.A)
	def DEC_F(self): self.A = self.ALU.DEC(self.A)
	def DEC_H(self): self.A = self.ALU.DEC(self.A)
	def DEC_L(self): self.A = self.ALU.DEC(self.A)
	def DEC_HL(self): self.write(self.read(self.HL), self.ALU.DEC(self.read(self.HL)))

	#16 bit alu shit
	def ADDHLBC(self): self.HL = self.ALU.ADD_HL(self.HL, self.BC)
	def ADDHLDE(self): self.HL = self.ALU.ADD_HL(self.HL, self.DE)
	def ADDHLHL(self): self.HL = self.ALU.ADD_HL(self.HL, self.HL)
	def ADDHLSP(self): self.HL = self.ALU.ADD_HL(self.HL, self.stackPointer)
	def ADDSPnn(self): self.stackPointer = self.ALU.ADD_SP(self.stackPointer, self.fetch())
	def INC_BC(self): self.BC = self.ALU.INC(self.BC)
	def INC_DE(self): self.DE = self.ALU.INC(self.DE)
	def INC_HL(self): self.HL = self.ALU.INC(self.HL)
	def INC_SP(self): self.stackPointer = self.ALU.INC(self.stackPointer)
	def DEC_BC(self): self.BC = self.ALU.DEC(self.BC)
	def DEC_DE(self): self.DE = self.ALU.DEC(self.DE)
	def DEC_HL(self): self.HL = self.ALU.DEC(self.HL)
	def DEC_SP(self): self.stackPointer = self.ALU.DEC(self.stackPointer)

	#Misc shit
	def DAA(self): self.A = self.ALU.DAA(self.A)
	def CCF(self): self.ALU.CCF()
	def SCF(self): self.ALU.SCF()
	def testShit(self): pass

	#rotates and shit
	def RLCA(self):
		a = self.A[7]
		self.A = self.A << 1
		self.A[0] = a
		self.F[4] = a
		self.F[7] = self.F[6] = self.F[5] = 0
	def RLA(self):
		a = self.A[7]
		self.A = self.A << 1
		self.A[0] = self.F[4]
		self.F[4] = a
		self.F[7] = self.F[6] = self.F[5] = 0
	def RRCA(self):
		a = self.A[0]
		self.A = self.A >> 1
		self.A[7] = a
		self.F[4] = a
		self.F[7] = self.F[6] = self.F[5] = 0
	def RRA(self):
		a = self.A[0]
		self.A = self.A >> 1
		self.A[7] = self.F[4]
		self.F[4] = a
		self.F[7] = self.F[6] = self.F[5] = 0

	#jumps and shit
	def JPnn(self): self.programCounter = self.fetch16()
	def JPnn_NZ(self):
		if not self.F[7]:
			self.programCounter = self.fetch16()
	def JPnn_Z(self):
		if self.F[7]:
			self.programCounter = self.fetch16()
	def JPnn_NC(self):
		if not self.F[4]:
			self.programCounter = self.fetch16()
	def JPnn_C(self):
		if self.F[4]:
			self.programCounter = self.fetch16()
	def JP_HL(self): self.programCounter = self.read(self.HL)
	def JRnn(self): self.programCounter = self.ALU.ADD_E(self.fetch(), self.programCounter)
	def JRnn_NZ(self):
		if not self.F[7]:
			self.programCounter = self.ALU.ADD_E(self.fetch(), self.programCounter)	
	def JRnn_Z(self):
		if self.F[7]:
			self.programCounter = self.ALU.ADD_E(self.fetch(), self.programCounter)
	def JRnn_NC(self):
		if not self.F[4]:
			self.programCounter = self.ALU.ADD_E(self.fetch(), self.programCounter)	
	def JRnn_C(self):
		if self.F[4]:
			self.programCounter = self.ALU.ADD_E(self.fetch(), self.programCounter)	

	#calls and shit
	def CALLnn(self):
		nn = self.fetch16()
		self.stackPointer -= 1
		self.write(self.stackPointer, self.programCounter.to8Bin()[1])
		self.stackPointer -= 1
		self.write(self.stackPointer, self.programCounter.to8Bin()[0])
	def CALLnn_NZ(self):
		if not self.F[7]:
			nn = self.fetch16()
			self.stackPointer -= 1
			self.write(self.stackPointer, self.programCounter.to8Bin()[1])
			self.stackPointer -= 1
			self.write(self.stackPointer, self.programCounter.to8Bin()[0])
	def CALLnn_Z(self):
		if not self.F[7]:
			nn = self.fetch16()
			self.stackPointer -= 1
			self.write(self.stackPointer, self.programCounter.to8Bin()[1])
			self.stackPointer -= 1
			self.write(self.stackPointer, self.programCounter.to8Bin()[0])
	def CALLnn_NC(self):
		if not self.F[4]:
			nn = self.fetch16()
			self.stackPointer -= 1
			self.write(self.stackPointer, self.programCounter.to8Bin()[1])
			self.stackPointer -= 1
			self.write(self.stackPointer, self.programCounter.to8Bin()[0])
	def CALLnn_C(self):
		if not self.F[4]:
			nn = self.fetch16()
			self.stackPointer -= 1
			self.write(self.stackPointer, self.programCounter.to8Bin()[1])
			self.stackPointer -= 1
			self.write(self.stackPointer, self.programCounter.to8Bin()[0])

	#resets and shit
	def RST_00(self): self.stackPointer = Bin16.fromHex("0000")
	def RST_08(self): self.stackPointer = Bin16.fromHex("0008")
	def RST_10(self): self.stackPointer = Bin16.fromHex("0010")
	def RST_18(self): self.stackPointer = Bin16.fromHex("0018")
	def RST_20(self): self.stackPointer = Bin16.fromHex("0020")
	def RST_28(self): self.stackPointer = Bin16.fromHex("0028")
	def RST_30(self): self.stackPointer = Bin16.fromHex("0030")
	def RST_38(self): self.stackPointer = Bin16.fromHex("0038")

	#swaps and shit
	def SWAP_A(self): self.A = self.ALU.SWAP(self.A)
	def SWAP_B(self): self.B = self.ALU.SWAP(self.B)
	def SWAP_C(self): self.C = self.ALU.SWAP(self.C)
	def SWAP_D(self): self.D = self.ALU.SWAP(self.D)
	def SWAP_E(self): self.E = self.ALU.SWAP(self.E)
	def SWAP_H(self): self.H = self.ALU.SWAP(self.H)
	def SWAP_L(self): self.L = self.ALU.SWAP(self.L)
	def SWAP_HL(self): 
		add = self.fetch()
		Self.write(add, self.ALU.SWAP(add))
	def RLC_A(self): self.RLC(self.A)
	def RLC_B(self): self.RLC(self.B)
	def RLC_C(self): self.RLC(self.C)
	def RLC_D(self): self.RLC(self.D)
	def RLC_E(self): self.RLC(self.E)
	def RLC_H(self): self.RLC(self.H)
	def RLC_L(self): self.RLC(self.L)
	def RLC_HL(self): self.write(self.HL, self.RLC(self.read(self.HL)))
	def RL_A(self): self.RL(self.A)
	def RL_B(self): self.RL(self.B)
	def RL_C(self): self.RL(self.C)
	def RL_D(self): self.RL(self.D)
	def RL_E(self): self.RL(self.E)
	def RL_H(self): self.RL(self.H)
	def RL_L(self): self.RL(self.L)
	def RL_HL(self): self.write(self.HL, self.RL(self.read(self.HL)))
	def RRC_A(self): self.RRC(self.A)
	def RRC_B(self): self.RRC(self.B)
	def RRC_C(self): self.RRC(self.C)
	def RRC_D(self): self.RRC(self.D)
	def RRC_E(self): self.RRC(self.E)
	def RRC_H(self): self.RRC(self.H)
	def RRC_L(self): self.RRC(self.L)
	def RRC_HL(self): self.write(self.HL, self.RRC(self.read(self.HL)))
	def RR_A(self): self.RR(self.A)
	def RR_B(self): self.RR(self.B)
	def RR_C(self): self.RR(self.C)
	def RR_D(self): self.RR(self.D)
	def RR_E(self): self.RR(self.E)
	def RR_H(self): self.RR(self.H)
	def RR_L(self): self.RR(self.L)
	def RR_HL(self): self.write(self.HL, self.RR(self.read(self.HL)))
	def SLA_A(self): self.SLA(self.A)
	def SLA_B(self): self.SLA(self.B)
	def SLA_C(self): self.SLA(self.C)
	def SLA_D(self): self.SLA(self.D)
	def SLA_E(self): self.SLA(self.E)
	def SLA_H(self): self.SLA(self.H)
	def SLA_L(self): self.SLA(self.L)
	def SLA_HL(self): self.write(self.HL, self.SLA(self.read(self.HL)))
	def SRA_A(self): self.SRA(self.A)
	def SRA_B(self): self.SRA(self.B)
	def SRA_C(self): self.SRA(self.C)
	def SRA_D(self): self.SRA(self.D)
	def SRA_E(self): self.SRA(self.E)
	def SRA_H(self): self.SRA(self.H)
	def SRA_L(self): self.SRA(self.L)
	def SRA_HL(self): self.write(self.HL, self.SRA(self.read(self.HL)))
	def SRL_A(self): self.SRL(self.A)
	def SRL_B(self): self.SRL(self.B)
	def SRL_C(self): self.SRL(self.C)
	def SRL_D(self): self.SRL(self.D)
	def SRL_E(self): self.SRL(self.E)
	def SRL_H(self): self.SRL(self.H)
	def SRL_L(self): self.SRL(self.L)
	def SRL_HL(self): self.write(self.HL, self.SRL(self.read(self.HL)))

	#bit shit
	def BIT0_B(self): self.BIT(0, self.B)
	def BIT0_C(self): self.BIT(0, self.C)
	def BIT0_D(self): self.BIT(0, self.D)
	def BIT0_E(self): self.BIT(0, self.E)
	def BIT0_H(self): self.BIT(0, self.H)
	def BIT0_L(self): self.BIT(0, self.L)
	def BIT0_HL(self): self.BIT(0, self.read(self.HL))
	def BIT0_A(self): self.BIT(0, self.A)
	def BIT1_B(self): self.BIT(1, self.B)
	def BIT1_C(self): self.BIT(1, self.C)
	def BIT1_D(self): self.BIT(1, self.D)
	def BIT1_E(self): self.BIT(1, self.E)
	def BIT1_H(self): self.BIT(1, self.H)
	def BIT1_L(self): self.BIT(1, self.L)
	def BIT1_HL(self): self.BIT(1, self.read(self.HL))
	def BIT1_A(self): self.BIT(1, self.A)
	def BIT2_B(self): self.BIT(2, self.B)
	def BIT2_C(self): self.BIT(2, self.C)
	def BIT2_D(self): self.BIT(2, self.D)
	def BIT2_E(self): self.BIT(2, self.E)
	def BIT2_H(self): self.BIT(2, self.H)
	def BIT2_L(self): self.BIT(2, self.L)
	def BIT2_HL(self): self.BIT(2, self.read(self.HL))
	def BIT2_A(self): self.BIT(2, self.A)
	def BIT3_B(self): self.BIT(3, self.B)
	def BIT3_C(self): self.BIT(3, self.C)
	def BIT3_D(self): self.BIT(3, self.D)
	def BIT3_E(self): self.BIT(3, self.E)
	def BIT3_H(self): self.BIT(3, self.H)
	def BIT3_L(self): self.BIT(3, self.L)
	def BIT3_HL(self): self.BIT(3, self.read(self.HL))
	def BIT3_A(self): self.BIT(3, self.A)
	def BIT4_B(self): self.BIT(4, self.B)
	def BIT4_C(self): self.BIT(4, self.C)
	def BIT4_D(self): self.BIT(4, self.D)
	def BIT4_E(self): self.BIT(4, self.E)
	def BIT4_H(self): self.BIT(4, self.H)
	def BIT4_L(self): self.BIT(4, self.L)
	def BIT4_HL(self): self.BIT(4, self.read(self.HL))
	def BIT4_A(self): self.BIT(4, self.A)
	def BIT5_B(self): self.BIT(5, self.B)
	def BIT5_C(self): self.BIT(5, self.C)
	def BIT5_D(self): self.BIT(5, self.D)
	def BIT5_E(self): self.BIT(5, self.E)
	def BIT5_H(self): self.BIT(5, self.H)
	def BIT5_L(self): self.BIT(5, self.L)
	def BIT5_HL(self): self.BIT(5, self.read(self.HL))
	def BIT5_A(self): self.BIT(5, self.A)
	def BIT6_B(self): self.BIT(6, self.B)
	def BIT6_C(self): self.BIT(6, self.C)
	def BIT6_D(self): self.BIT(6, self.D)
	def BIT6_E(self): self.BIT(6, self.E)
	def BIT6_H(self): self.BIT(6, self.H)
	def BIT6_L(self): self.BIT(6, self.L)
	def BIT6_HL(self): self.BIT(6, self.read(self.HL))
	def BIT6_A(self): self.BIT(6, self.A)
	def BIT7_B(self): self.BIT(7, self.B)
	def BIT7_C(self): self.BIT(7, self.C)
	def BIT7_D(self): self.BIT(7, self.D)
	def BIT7_E(self): self.BIT(7, self.E)
	def BIT7_H(self): self.BIT(7, self.H)
	def BIT7_L(self): self.BIT(7, self.L)
	def BIT7_HL(self): self.BIT(7, self.read(self.HL))
	def BIT7_A(self): self.BIT(7, self.A)

	#res shit
	def RES0_B(self): self.RES(0, self.B)
	def RES0_C(self): self.RES(0, self.C)
	def RES0_D(self): self.RES(0, self.D)
	def RES0_E(self): self.RES(0, self.E)
	def RES0_H(self): self.RES(0, self.H)
	def RES0_L(self): self.RES(0, self.L)
	def RES0_HL(self): self.write(self.HL, self.RES(0, self.read(self.HL)))
	def RES0_A(self): self.RES(0, self.A)
	def RES1_B(self): self.RES(1, self.B)
	def RES1_C(self): self.RES(1, self.C)
	def RES1_D(self): self.RES(1, self.D)
	def RES1_E(self): self.RES(1, self.E)
	def RES1_H(self): self.RES(1, self.H)
	def RES1_L(self): self.RES(1, self.L)
	def RES1_HL(self): self.write(self.HL, self.RES(1, self.read(self.HL)))
	def RES1_A(self): self.RES(1, self.A)
	def RES2_B(self): self.RES(2, self.B)
	def RES2_C(self): self.RES(2, self.C)
	def RES2_D(self): self.RES(2, self.D)
	def RES2_E(self): self.RES(2, self.E)
	def RES2_H(self): self.RES(2, self.H)
	def RES2_L(self): self.RES(2, self.L)
	def RES2_HL(self): self.write(self.HL, self.RES(2, self.read(self.HL)))
	def RES2_A(self): self.RES(2, self.A)
	def RES3_B(self): self.RES(3, self.B)
	def RES3_C(self): self.RES(3, self.C)
	def RES3_D(self): self.RES(3, self.D)
	def RES3_E(self): self.RES(3, self.E)
	def RES3_H(self): self.RES(3, self.H)
	def RES3_L(self): self.RES(3, self.L)
	def RES3_HL(self): self.write(self.HL, self.RES(3, self.read(self.HL)))
	def RES3_A(self): self.RES(3, self.A)
	def RES4_B(self): self.RES(4, self.B)
	def RES4_C(self): self.RES(4, self.C)
	def RES4_D(self): self.RES(4, self.D)
	def RES4_E(self): self.RES(4, self.E)
	def RES4_H(self): self.RES(4, self.H)
	def RES4_L(self): self.RES(4, self.L)
	def RES4_HL(self): self.write(self.HL, self.RES(4, self.read(self.HL)))
	def RES4_A(self): self.RES(4, self.A)
	def RES5_B(self): self.RES(5, self.B)
	def RES5_C(self): self.RES(5, self.C)
	def RES5_D(self): self.RES(5, self.D)
	def RES5_E(self): self.RES(5, self.E)
	def RES5_H(self): self.RES(5, self.H)
	def RES5_L(self): self.RES(5, self.L)
	def RES5_HL(self): self.write(self.HL, self.RES(5, self.read(self.HL)))
	def RES5_A(self): self.RES(5, self.A)
	def RES6_B(self): self.RES(6, self.B)
	def RES6_C(self): self.RES(6, self.C)
	def RES6_D(self): self.RES(6, self.D)
	def RES6_E(self): self.RES(6, self.E)
	def RES6_H(self): self.RES(6, self.H)
	def RES6_L(self): self.RES(6, self.L)
	def RES6_HL(self): self.write(self.HL, self.RES(6, self.read(self.HL)))
	def RES6_A(self): self.RES(6, self.A)
	def RES7_B(self): self.RES(7, self.B)
	def RES7_C(self): self.RES(7, self.C)
	def RES7_D(self): self.RES(7, self.D)
	def RES7_E(self): self.RES(7, self.E)
	def RES7_H(self): self.RES(7, self.H)
	def RES7_L(self): self.RES(7, self.L)
	def RES7_HL(self): self.write(self.HL, self.RES(7, self.read(self.HL)))
	def RES7_A(self): self.RES(7, self.A)

	#set shit
	def SET0_B(self): self.SET(0, self.B)
	def SET0_C(self): self.SET(0, self.C)
	def SET0_D(self): self.SET(0, self.D)
	def SET0_E(self): self.SET(0, self.E)
	def SET0_H(self): self.SET(0, self.H)
	def SET0_L(self): self.SET(0, self.L)
	def SET0_HL(self): self.write(self.HL, self.SET(0, self.read(self.HL)))
	def SET0_A(self): self.SET(0, self.A)
	def SET1_B(self): self.SET(1, self.B)
	def SET1_C(self): self.SET(1, self.C)
	def SET1_D(self): self.SET(1, self.D)
	def SET1_E(self): self.SET(1, self.E)
	def SET1_H(self): self.SET(1, self.H)
	def SET1_L(self): self.SET(1, self.L)
	def SET1_HL(self): self.write(self.HL, self.SET(1, self.read(self.HL)))
	def SET1_A(self): self.SET(1, self.A)
	def SET2_B(self): self.SET(2, self.B)
	def SET2_C(self): self.SET(2, self.C)
	def SET2_D(self): self.SET(2, self.D)
	def SET2_E(self): self.SET(2, self.E)
	def SET2_H(self): self.SET(2, self.H)
	def SET2_L(self): self.SET(2, self.L)
	def SET2_HL(self): self.write(self.HL, self.SET(2, self.read(self.HL)))
	def SET2_A(self): self.SET(2, self.A)
	def SET3_B(self): self.SET(3, self.B)
	def SET3_C(self): self.SET(3, self.C)
	def SET3_D(self): self.SET(3, self.D)
	def SET3_E(self): self.SET(3, self.E)
	def SET3_H(self): self.SET(3, self.H)
	def SET3_L(self): self.SET(3, self.L)
	def SET3_HL(self): self.write(self.HL, self.SET(3, self.read(self.HL)))
	def SET3_A(self): self.SET(3, self.A)
	def SET4_B(self): self.SET(4, self.B)
	def SET4_C(self): self.SET(4, self.C)
	def SET4_D(self): self.SET(4, self.D)
	def SET4_E(self): self.SET(4, self.E)
	def SET4_H(self): self.SET(4, self.H)
	def SET4_L(self): self.SET(4, self.L)
	def SET4_HL(self): self.write(self.HL, self.SET(4, self.read(self.HL)))
	def SET4_A(self): self.SET(4, self.A)
	def SET5_B(self): self.SET(5, self.B)
	def SET5_C(self): self.SET(5, self.C)
	def SET5_D(self): self.SET(5, self.D)
	def SET5_E(self): self.SET(5, self.E)
	def SET5_H(self): self.SET(5, self.H)
	def SET5_L(self): self.SET(5, self.L)
	def SET5_HL(self): self.write(self.HL, self.SET(5, self.read(self.HL)))
	def SET5_A(self): self.SET(5, self.A)
	def SET6_B(self): self.SET(6, self.B)
	def SET6_C(self): self.SET(6, self.C)
	def SET6_D(self): self.SET(6, self.D)
	def SET6_E(self): self.SET(6, self.E)
	def SET6_H(self): self.SET(6, self.H)
	def SET6_L(self): self.SET(6, self.L)
	def SET6_HL(self): self.write(self.HL, self.SET(6, self.read(self.HL)))
	def SET6_A(self): self.SET(6, self.A)
	def SET7_B(self): self.SET(7, self.B)
	def SET7_C(self): self.SET(7, self.C)
	def SET7_D(self): self.SET(7, self.D)
	def SET7_E(self): self.SET(7, self.E)
	def SET7_H(self): self.SET(7, self.H)
	def SET7_L(self): self.SET(7, self.L)
	def SET7_HL(self): self.write(self.HL, self.SET(7, self.read(self.HL)))
	def SET7_A(self): self.SET(7, self.A)

	def execute(self, opcode):
		opcode = opcode.toHex()
		if opcode == "CB":
			self.CBopcodes[self.fetch()]()
		else:
			self.opcodes[opcode]()
		
	def SET(self, b, reg):
		reg[b] = 1
		return reg

	def	RES(self, b, reg):
		reg[b] = 0
		return reg
	
	def BIT(self, b, reg):
		self.F[7] = 0 if reg[b] else 1
		self.F[6] = 0
		self.F[5] = 1
	
	def SRL(self, reg):
		self.F[4] = reg[0]
		reg = reg >> 1
		self.F[7] = 1 if reg == Bin("00") else 0
		self.F[6] = self.F[5] = 0
		return reg

	def SRA(self, reg):
		a = reg[7]
		self.F[4] = reg[0]
		reg = reg >> 1
		reg[7] = a
		self.F[7] = 1 if reg == Bin("00") else 0
		self.F[6] = self.F[5] = 0
		return reg

	def SLA(self, reg):
		self.F[4] = reg[7]
		reg = reg << 1
		return reg

	def RLC(self, reg):
		a = reg[7]
		reg = reg << 1
		reg[0] = a
		self.F[4] = a
		self.F[7] = 1 if reg == Bin("00") else 0
		self.F[6] = self.F[5] = 0
		return reg

	def RL(self, reg):
		a = reg[7]
		reg = reg << 1
		reg[0] = self.F[4]
		self.F[4] = a
		self.F[7] = 1 if reg == Bin("00") else 0
		self.F[6] = self.F[5] = 0
		return reg

	def RRC(self, reg):
		a = reg[0]
		reg = reg >> 1
		reg[7] = a
		self.F[4] = a
		self.F[7] = 1 if reg == Bin("00") else 0
		self.F[6] = self.F[5] = 0
		return reg

	def RR(self, reg):
		a = reg[0]
		reg = reg >> 1
		reg[7] = self.F[4]
		self.F[4] = a
		self.F[7] = 1 if reg == Bin("00") else 0
		self.F[6] = self.F[5] = 0
		return reg

	def debug(self, autoRunToAddress="CC5F"):
		counter = 0
		breakPoint = False
		while True:
			#print(counter)
			if self.programCounter.toHex() == autoRunToAddress:
				#print("saving")
				#self.memoryBus.saveDump()
				exit()
			if breakPoint:
				print("AF: {0}\nBC: {1}\nDE: {2}\nHL: {3}\nSP: {4}\nPC: {5}".format(self.AF.toHex(), self.BC.toHex(), self.DE.toHex(), self.HL.toHex(), self.stackPointer.toHex(), self.programCounter.toHex()))
				print("Program Counter at: {0}\tInstruction: {1}\n".format(self.programCounter.toHex(), self.memoryBus[self.programCounter].toHex()))
				#print("Stack: {0}, {1}, {2}".format(self.memoryBus["C000"].toHex(), self.memoryBus["C001"].toHex(), self.memoryBus["C002"].toHex()))
				input()
			ins = self.fetch()
			self.execute(ins)
			counter += 1

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
	#apparently binary is fucked

if __name__ == "__main__":
	cpu = CPU()
	cpu.load("06-ld r,r.gb")
	cpu.debug()