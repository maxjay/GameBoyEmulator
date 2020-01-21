from memory import Memory
from binary import Bin16, Bin

class Tile():

	def __init__(self):
		self.palette = {"00": " ",
				"01": u'\u2592',
				"10": u'\u2593',
				"11": u'\u2588'}
		self.data = [Bin.fromHex("00"),
					Bin.fromHex("00"),
					Bin.fromHex("3C"),
					Bin.fromHex("3C"),
					Bin.fromHex("4E"),
					Bin.fromHex("4E"),
					Bin.fromHex("0E"),
					Bin.fromHex("0E"),
					Bin.fromHex("3C"),
					Bin.fromHex("3C"),
					Bin.fromHex("70"),
					Bin.fromHex("70"),
					Bin.fromHex("7E"),
					Bin.fromHex("7E"),
					Bin.fromHex("00"),
					Bin.fromHex("00")]

	def render(self):
		for i in self.data:
			string = ""
			for j in range(0, 8, 2):
				string += (self.palette[str(i[7-j]) + str(i[6-j])])
			print(string)

class GPU():
	def __init__(self):
		self.memory = Memory()
		self.memory.load("a.dump")
		self.tile0 = self.memory[Bin16.fromHex("8000").toDecimal():Bin16.fromHex("8FFF").toDecimal()]
		self.tile1 = self.memory[Bin16.fromHex("8FFF").toDecimal():Bin16.fromHex("9FFF").toDecimal()]
		self.tileMap0 = self.memory[Bin16.fromHex("9800").toDecimal():Bin16.fromHex("9BFF").toDecimal()]
		self.tileMap1 = self.memory[Bin16.fromHex("9C00").toDecimal():Bin16.fromHex("9FFF").toDecimal()]

if __name__ == "__main__":
	a = Tile()
	a.render()
