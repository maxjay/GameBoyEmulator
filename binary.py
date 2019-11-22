class Bin:
	@staticmethod
	def decToBin(a, bitLength=8):
		r = ""
		for i in range(bitLength):
			if 2**(bitLength-1-i) <= a:
				r += "1"
				a =  a - 2**(bitLength-1-i)
			else:
				r += "0"
		return Bin(r)

	@staticmethod
	def hexToBin(string):
		t = ""
		for i in string:
			if i == "A":
				i = 10
			elif i == "B":
				i = 11
			elif i == "C":
				i = 12
			elif i == "D":
				i = 13
			elif i == "E":
				i = 14
			elif i == "F":
				i = 15
			else:
				i = int(i)
			r = ""
			for j in range(4):
				if 2**(3-j) <= i:
					r += "1"
					i = i - 2**(3-j)
				else:
					r += "0"
			t = t + r
		return Bin(t)

	def __init__(self, value, bitLength = None):
		self.bitLength = bitLength if bitLength != None else len(value)
		self.value = value if len(value) == self.bitLength else "0"*(self.bitLength-len(value))+value

	def __getitem__(self, key):
		if isinstance(key, slice):
			return Bin(self.value[key])
		elif isinstance(key, int):
			return Bin(self.value[self.bitLength - key -1])

	def __setitem__(self, key, value):
		self.value[key] = value
		return Bin(self.value)

	def toHex(self):
		string = ""
		for i in range(self.bitLength//4):
			a = 0
			for j in range(4):
				if self.value[(i*4)+j] == "1":
					a += 2**(3-j)
			if a == 10:
				a = "A"
			elif a == 11:
				a = "B"
			elif a == 12:
				a = "C"
			elif a == 13:
				a = "D"
			elif a == 14:
				a = "E"
			elif a == 15:
				a = "F"
			else:
				a = str(a)
			string += a
		return string

	def toDec(self):
		a = 0
		for i in range(self.bitLength):
			if self.value[i] == "1":
				a += 2**(self.bitLength - i - 1)
		return a

	def __lshift__(self, other):
		return Bin(self.value + "0"*other)

	def __rshift__(self, other):
		return Bin("0"*other + self.value)

	def __xor__(self, other):
		if self.bitLength > other.bitLength:
			other = other >> (self.bitLength - other.bitLength)
		elif self.bitLength < other.bitLength:
			self = self >> (other.bitLength - self.bitLength)
		r = ""
		for i in range(self.bitLength):
			if self[i] != other[i]:
				r = "1" + r
			else:
				r = "0" + r
		return Bin(r)

	def __or__(self, other):
		print("or")
		if self.bitLength > other.bitLength:
			other = other >> (self.bitLength - other.bitLength)
		elif self.bitLength < other.bitLength:
			self = self >> (other.bitLength - self.bitLength)
		r = ""
		for i in range(self.bitLength):
			if self[i] == "1":
				r = "1" + r
			elif other[i] == "1":
				r = "1" + r
			else:
				r = "0" + r
		return Bin(r)

	def __and__(self, other):
		if self.bitLength > other.bitLength:
			other = other >> (self.bitLength - other.bitLength)
		elif self.bitLength < other.bitLength:
			self = self >> (other.bitLength - self.bitLength)
		r = ""
		for i in range(self.bitLength):
			if self[i] == other[i] == "1":
				r = "1" + r
			else:
				r = "0" + r
		return Bin(r)

	@staticmethod
	def overflowing_add(a, b):
		if a[a.bitLength - 1] == b[b.bitLength -1] == "1":
			return 1, a+b
		else:
			return 0, a+b

	def __invert__(self):
		r = ""
		for i in self.value:
			if i == "1":
				r += "0"
			else:
				r += "1"
		return Bin(r)

	def __ne__(self, other):
		if isinstance(other, str):
				if other == self.value:
					return False
		else:
			if other.value == self.value:
				return False
			else:
				return True

	def __eq__(self, other):
		if isinstance(other, str):
			if other == self.value:
				return True
		else:
			if other.value == self.value:
				return True
			else:
				return False

	def __str__(self):
		return self.value

	def __repr__(self):
		return self.value

	def __add__(self, other):
		if isinstance(other, int):
			other = self.decToBin(other)
		if self.bitLength > other.bitLength:
			other = other >> (self.bitLength - other.bitLength)
		elif self.bitLength < other.bitLength:
			self = self >> (other.bitLength - self.bitLength)
		r = ""
		carry = 0
		for i in range(self.bitLength):
			if carry:
				if self[i] ^ other[i] == "1":
					r = "0" + r
				else:
					r = "1" + r
					carry = 0
			else:
				if self[i] ^ other[i] == "1":
					r = "1" + r
				else:
					r = "0" + r
			carry += 1 if self[i] & other[i] == "1"  else 0
		return Bin(r)

	def __sub__(self, other):
		if isinstance(other, int):
			other = self.decToBin(other)
		if self.bitLength > other.bitLength:
			other = other >> (self.bitLength - other.bitLength)
		elif self.bitLength < other.bitLength:
			self = self >> (other.bitLength - self.bitLength)
		other = ~other;
		other = other + Bin("1")
		return other + self
