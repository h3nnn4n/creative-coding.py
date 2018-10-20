import numpy as np


class Vector:
    def __init__(self, x=0, y=0):
        self.data = np.zeros(2)
        self.x = x
        self.y = y

    def set_x(self, x):
        self.data[0] = x

    def set_y(self, y):
        self.data[1] = y

    def get_x(self):
        return self.data[0]

    def get_y(self):
        return self.data[1]

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self = self + other
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self = self - other
        return self

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __imul__(self, other):
        self = self * other
        return self

    def __str__(self):
        return '%f %f' % (self.x, self.y)

    def __repr__(self):
        return '%f %f' % (self.x, self.y)

    def normalize(self):
        self.data = self.data / self.norm

    @property
    def norm(self):
        return np.sqrt((np.sum(self.data ** 2)))

    def set_mag(self, mag):
        self.normalize()
        self *= mag

    def zero(self):
        self.x = 0
        self.y = 0

    x = property(get_x, set_x)
    y = property(get_y, set_y)
