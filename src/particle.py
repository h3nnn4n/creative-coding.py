from vector import Vector


class Particle:
    def __init__(self):
        self.position = Vector()
        self.position_old = Vector()
        self.velocity = Vector()
        self.acceleration = Vector()
        # self.max_velocity = 2

    def step(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0

    def apply_force(self, force):
        self.acceleration += force
