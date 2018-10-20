import pytest
from vector import Vector


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


def test_set():
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
    a.set_mag(1)
    assert a.norm == 1
    a.set_mag(5)
    assert a.norm == 1
