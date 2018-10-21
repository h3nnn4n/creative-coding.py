import pytest
from vector import Vector
from math import pi


def test_add():
    a = Vector(1, 2)
    b = Vector(3, 4)

    c = a + b

    assert c.x == 4
    assert c.y == 6

    assert a.x == 1
    assert a.y == 2

    assert b.x == 3
    assert b.y == 4


def test_sub():
    a = Vector(1, 2)
    b = Vector(3, 4)

    c = a - b

    assert c.x == -2
    assert c.y == -2

    assert a.x == 1
    assert a.y == 2

    assert b.x == 3
    assert b.y == 4


def test_iadd():
    a = Vector(1, 2)
    b = Vector(3, 4)

    a += b

    assert a.x == 4
    assert a.y == 6

    assert b.x == 3
    assert b.y == 4


def test_isub():
    a = Vector(1, 2)
    b = Vector(3, 4)

    a -= b

    assert a.x == -2
    assert a.y == -2

    assert b.x == 3
    assert b.y == 4


def test_setter():
    a = Vector()

    assert a.x == 0
    assert a.y == 0

    a.x = 1

    assert a.x == 1
    assert a.y == 0

    a.y = 1

    assert a.x == 1
    assert a.y == 1


def test_mul():
    a = Vector(1, 1)
    a = a * 2

    assert a.x == 2
    assert a.y == 2


def test_imul():
    a = Vector(1, 1)
    a *= 10

    assert a.x == 10
    assert a.y == 10


def test_norm():
    a = Vector(3, 4)
    assert a.norm == 5

    a = Vector()
    assert a.norm == 0


def test_normalize():
    a = Vector(3, 4)
    a.normalize()

    assert a.norm == 1


def test_zero():
    a = Vector(1, 1)
    a.zero()

    assert a.x == 0
    assert a.y == 0


def test_set_mag():
    a = Vector(3, 4)
    a.set_mag(2)
    assert a.norm == 2
    a.set_mag(5)
    assert a.norm == 5
    a.set_mag(1)
    assert a.norm == 1


def test_limit():
    a = Vector(3, 4)
    assert a.norm == 5

    a.limit(10)
    assert a.norm == 5

    a.limit(3)
    assert a.norm == 3

    a.limit(1)
    assert a.norm == 1


def test_from_angle():
    a = Vector().from_angle(0)
    assert abs(a.x - 1) < 1e-10
    assert abs(a.y - 0) < 1e-10

    a = Vector().from_angle(pi / 2)
    assert abs(a.x - 0) < 1e-10
    assert abs(a.y - 1) < 1e-10

    a = Vector().from_angle(pi)
    assert abs(a.x - -1) < 1e-10
    assert abs(a.y - 0) < 1e-10


def test_set():
    a = Vector(1, 2)
    b = Vector(5, 4)
    a.set(b)

    assert a.x == b.x
    assert a.y == b.y


def test_dist():
    a = Vector(1, 1)
    b = Vector(1, 2)

    assert a.dist(b) == 1
    assert b.dist(a) == 1

    a = Vector(2, 3)
    b = Vector(5, 7)

    assert a.dist(b) == 5
    assert b.dist(a) == 5
