#!/usr/bin/python3

class Bin():
	def __init__(self, value=None):
		self.array = [0,0,0,0,0,0,0,0]
		if value != None:
			if type(value) == str:
				if len(value) == 8:
					self.array = [0 if i == "0" else 1 for i in value]
				elif len(value) == 2:
					self.array = Bin.fromHex(value).array
			elif type(value) == list:
				self.array = value

	def __repr__(self):
		return self.__str__()

	def __getitem__(self, index):
		if type(index) == int:
			return self.array[7-index]

	def __setitem__(self, index, val):
		if type(index) == int:
			self.array[7-index] = val
		return self

	def __str__(self):
		return "".join([str(i) for i in self.array])

	def __eq__(self, other):
		if isinstance(other, str):
			return self.array == Bin.fromHex(other).array
		return self.array == other.array

	def __xor__(self, other):
		return Bin([1 if self.array[i] != other.array[i] else 0 for i in range(8)])

	def __and__(self, other):
		return Bin([1 if self.array[i] == other.array[i] == 1 else 0 for i in range(8)])

	def __or__(self, other):
		return Bin([1 if (self.array[i] == 1) or (other.array[i] == 1) else 0 for i in range(8)])

	def __invert__(self):
		return Bin([0 if i == 1 else 1 for i in self.array])

	def __lshift__(self, a):
		for i in range(a):
			self.array.pop(0)
			self.array.append(0)
		return self

	def __rshift__(self, a):
		for i in range(a):
			self.array.pop()
			self.array.insert(0, 0)
		return self

	def __add__(self, other):
		if type(other) == int:
			other = Bin.fromDecimal(other)
		elif type(other) == str:
			if len(other) == 8:
				other = Bin(other)
			elif len(other) == 2:
				other = Bin.fromHex(other)
		temp = Bin()
		C = 0
		for i in range(8):
			temp[i], C = self.fullAdder(self[i], other[i], C)
		return temp

	def __sub__(self, other):
		if type(other) == int:
			other = Bin.fromDecimal(other)
		elif type(other) == str:
			if len(other) == 8:
				other = Bin(other)
			elif len(other) == 2:
				other = Bin.fromHex(other)
		other = ~other + Bin("00000001")
		return self.__add__(other)

	def toDecimal(self):
		return sum([2**i if self[i] == 1 else 0 for i in range(8)])

	def toHex(self):
		highNibble = Bin.toDecimal((self & Bin("11110000")) >> 4)
		lowNibble =	Bin.toDecimal(self & Bin("00001111"))
		hexString = ""
		for i in [highNibble, lowNibble]:
			if i == 10:
				hexString += "A"
			elif i == 11:
				hexString += "B"
			elif i == 12:
				hexString += "C"
			elif i == 13:
				hexString += "D"
			elif i == 14:
				hexString += "E"
			elif i == 15:
				hexString += "F"
			else:
				hexString += str(i)
		return hexString

	@staticmethod
	def fullAdder(a, b, c=0):
		S = (a ^ b) ^ c
		C = (a & b) | c & (a ^ b)
		return S, C

	@staticmethod
	def overflowing_add(a,b):
		temp = Bin()
		C = 0
		for i in range(8):
			temp[i], C = Bin.fullAdder(a[i], b[i], C)
		return temp, C

	@staticmethod
	def underflowing_sub(a,b):
		b = ~b + Bin("00000001")
		temp, C = Bin.overflowing_add(a,b)
		return temp, 1 if C == 0 else 0

	@staticmethod
	def halfcarry(a,b):
		#print((a & Bin.fromHex("0F")) + (b & Bin.fromHex("0F")) & Bin.fromHex("10") == Bin.fromHex("10"))
		return 1 if ((a & Bin.fromHex("0F")) + (b & Bin.fromHex("0F"))) & Bin.fromHex("10") == Bin.fromHex("10") else 0

	@staticmethod
	def halfborrow(a,b):
		return 0 if Bin.halfcarry(a,b) == 1 else 1

	@staticmethod
	def fromDecimal(a):
		flip = False
		if a < 0:
			flip = True
			a = 0 - a
		temp = Bin()
		for i in range(8):
			if 2**(7-i) <= a:
				a -= 2**(7-i)
				temp.array[i] = 1
		if flip:
			return ~temp + Bin("00000001")
		return temp

	@staticmethod
	def fromHex(a):
		temp = Bin()
		highNibble = Bin.fromDecimal(int(a[0], 16)) << 4
		lowNibble = Bin.fromDecimal(int(a[1], 16))
		return highNibble | lowNibble

class Bin16():
	def __init__(self, a=None, b=None):
		if not a:
			a_, b_ = Bin(), Bin()
			self.array = [a_, b_]
		elif not b:
			a_, b_ = Bin(), Bin()
			for i in range(8):
				a_[7-i] = int(a[i])
			for i in range(8):
				b_[7-i] = int(a[i+8])
			self.array = [a_, b_]
		else:
			if type(a) == Bin and type(a) == Bin:
				self.array = [a,b]
			else:
				self.array = [Bin(a), Bin(b)]

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		string = ""
		for i in range(2):
			for j in range(7, -1,  -1):
				string += str(self.array[i][j])
		return string

	def __eq__(self, other):
		return self.array == other.array

	def __getitem__(self, index):
		if type(index) ==  int:
			return self.array[(index//8 +1)%2][index % 8]

	def __setitem__(self, index, val):
		if type(index) == int:
			self.array[(index//8 +1)%2][index % 8] = val
		return self

	def __invert__(self):
		temp = Bin16()
		for i in range(2):
			temp.array[i] = ~self.array[i]
		return temp

	def __and__(self, other):
		for i in range(2):
			self.array[i] = self.array[i] & other.array[i]
		return self

	def __or__(self, other):
		for i in range(2):
			self.array[i] = self.array[i] | other.array[i]
		return self

	def __xor__(self, other):
		for i in range(2):
			self.array[i] = self.array[i] ^ other.array[i]
		return self

	def __lshift__(self, a):
		binString = []
		for j in range(16):
				binString.append(self[15-j])
		for i in range(a):
			binString.pop(0)
			binString.append(0)
		return Bin16(binString)

	def __rshift__(self, a):
		binString = []
		for j in range(16):
				binString.append(self[15-j])
		for i in range(a):
			binString.pop()
			binString.insert(0, 0)
		return Bin16(binString)

	def __add__(self, other):
		if type(other) == int:
			other = Bin16.fromDecimal(other)
		elif type(other) == str:
			if len(other) == 16:
				other = Bin16(other)
			elif len(other) == 4:
				other = Bin16.fromHex(other)
		elif type(other) == Bin:
			other = Bin16(Bin(), other)
		temp = Bin16()
		c = 0
		for i in range(16):
			temp[i], c = Bin.fullAdder(self[i], other[i], c)
		return temp

	def __sub__(self, other):
		if type(other) == int:
			other = Bin16.fromDecimal(other)
		elif type(other) == str:
			if len(other) == 16:
				other = Bin16(other)
			elif len(other) == 4:
				other = Bin16.fromHex(other)
		other = ~other + Bin16("0000000000000001")
		return self.__add__(other)

	def toDecimal(self):
		decArray = []
		for i in self.array:
			decArray.append(i.toDecimal())
		decArray[0] = decArray[0] * 256
		return sum(decArray)

	def toHex(self):
		hexString = ""
		for i in self.array:
			hexString += i.toHex()
		return hexString

	def to8Bin(self):
		return self.array

	@staticmethod
	def fromDecimal(a):
		return Bin16(Bin.fromDecimal(a//256), Bin.fromDecimal(a % 256))

	@staticmethod
	def fromHex(a):
		return Bin16(Bin.fromHex(a[:2]), Bin.fromHex(a[2:]))


if __name__ == "__main__":
	def test(a, b):
		A = Bin.fromDecimal(a)
		B = Bin.fromDecimal(b)
		C = A + B
		if not ((A.toDecimal() == a) | (-256+A.toDecimal() == a)):
			print(1, a, A, A.toDecimal(), -256+A.toDecimal(), (A.toDecimal() == a | -256+A.toDecimal() == a))
			return False
		if not ((B.toDecimal() == b) | (-256+B.toDecimal() == b)):
			print(2, b, B, B.toDecimal(), -256+B.toDecimal())
			return False
		if not ((C.toDecimal() == a + b) | (-256+C.toDecimal() == a + b)):
			print(3, C, C.toDecimal(), C.toDecimal() == a + b, -256+C.toDecimal() == a + b)
			return False
		C = A - B
		if not ((C.toDecimal() == a - b) | (-256+C.toDecimal() == a - b)):
			print(4, C, C.toDecimal(), 0-(256-(C.toDecimal())), (C.toDecimal() == a - b) | (0-(256-(C.toDecimal())) == a - b))
			return False
		return True

	import random
	passed = 0
	failed = 0
	for i in range(25):
		a_ = [random.randint(0, 128), random.randint(0, 128), random.randint(-127, 128), random.randint(-127, 128)]
		b_ = [random.randint(0, 128), random.randint(-127, 128), random.randint(0, 128), random.randint(-127, 128)]
		for i in range(4):
			a, b = a_[i], b_[i]
			if test(a,b):
				passed += 1
			else:
				failed += 1
	print("Passed: {0}\tFailed: {1}".format(passed, failed))
