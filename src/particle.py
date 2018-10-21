from random import random

from vector import Vector


class Particle:
    def __init__(self):
        self.position = Vector()
        self.position_old = Vector()
        self.velocity = Vector()
        self.acceleration = Vector()
        self.max_velocity = 2

        self.life = 1000
        self.alive = True

        self.bounds = Vector(1, 1)

    def random_position(self, max_x=1, max_y=1):
        self.position.x = random() * max_x
        self.position.y = random() * max_y

        return self

    def set_bounds(self, bounds):
        self.bounds.set(bounds)

        return self

    def set_life(self, life):
        self.life = life

        if self.life > 0:
            self.alive = True

        return self

    def set_color(self, callback):
        self.color = callback(self)

        return self

    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y

        return self

    def stop(self):
        self.velocity.zero()
        self.acceleration.zero()

        return self

    def set_max_velocity(self, max_velocity):
        self.max_velocity = max_velocity

        return self

    def step(self):
        self.heartbeat()

        self.position_old.set(self.position)
        self.velocity += self.acceleration
        self.velocity.limit(self.max_velocity)
        self.position += self.velocity
        self.acceleration *= 0

        self.check_bounds()

    def heartbeat(self):
        self.life -= 1

        if self.life <= 0:
            self.alive = False

    def check_bounds(self):
        if self.position.x < 0 or self.position.x > self.bounds.x:
            self.alive = False

        if self.position.y < 0 or self.position.y > self.bounds.y:
            self.alive = False

    def apply_force(self, force):
        self.acceleration += force
