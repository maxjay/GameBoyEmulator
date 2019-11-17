from binary import Bin

class CPU:
	def __init__(self):
		self.Registers = {'A': Bin("000000000"),
						  'B': Bin("000000000"),
						  'C': Bin("000000000"),
						  'D': Bin("000000000"),
						  'E': Bin("000000000"),
						  'F': Bin("000000000"),
						  'H': Bin("000000000"),
						  'L': Bin("000000000")}
		self.flagRegister = Bin("11110000")

	def set_AF(self, bin_):
		self.Registers["A"] = bin_[:8]
		self.Registers["F"] = bin_[8:]

	def set_BC(self, bin_):
		self.Registers["B"] = bin_[:8]
		self.Registers["C"] = bin_[8:]

	def set_DE(self, bin_):
		self.Registers["D"] = bin_[:8]
		self.Registers["E"] = bin_[8:]

	def set_HL(self, bin_):
		self.Registers["H"] = bin_[:8]
		self.Registers["L"] = bin_[8:]

	def get_AF(self):
		return (self.Registers["A"] << 8) + self.Registers["F"]

	def get_BC(self):
		return (self.Registers["B"] << 8) + self.Registers["C"]

	def get_DE(self):
		return (self.Registers["D"] << 8) + self.Registers["E"]

	def get_HL(self):
		return (self.Registers["H"] << 8) + self.Registers["L"]
