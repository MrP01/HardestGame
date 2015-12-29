import math, pygame

class Vector(object):
	def __init__(self, x, y=None):
		self._x, self._y=0, 0
		if y is None: self.x, self.y = x
		else: self.x, self.y = x, y
	
	def x(self):
		return self._x
	def setX(self, x):
		self._x=int(x)
	x=property(x, setX)
	
	def y(self):
		return self._y
	def setY(self, y):
		self._y=int(y)
	y=property(y, setY)

	def normalized(self):
		return Vector(self.x/self.length(), self.y/self.length())

	def length(self):
		return math.hypot(self.x, self.y)

	def __add__(self, other):
		return Vector(self.x+other.x, self.y+other.y)

	def __iadd__(self, other):
		self.x+=other.x
		self.y+=other.y
		return self

	def __sub__(self, other):
		return Vector(self.x-other.x, self.y-other.y)

	def __isub__(self, other):
		self.x-=other.x
		self.y-=other.y
		return self

	def __mul__(self, other):
		return Vector(self.x*other, self.y*other)

	def __imul__(self, other):
		self.x*=other
		self.y*=other
		return self

	def __len__(self):
		return 2

	def __getitem__(self, item):
		if item == 0:
			return self.x
		else:
			return self.y

	def __setitem__(self, key, value):
		if key == 0:
			self.x=value
		else:
			self.y=value

	def __iter__(self):
		yield self.x
		yield self.y

	def __str__(self):
		return "Vector({x}, {y})".format(x=self.x, y=self.y)
