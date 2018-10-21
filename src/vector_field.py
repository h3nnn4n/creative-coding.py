# pylint: disable=E1101
import cairo
import os

import numpy as np

from context_manager import ContextManager
from vector import Vector
from particle import Particle

from noise import snoise2, pnoise2
from random import random, uniform, seed
from math import pi, sin, cos, sqrt, ceil, floor


class VectorField:
    def __init__(self):
        self.context_manager = ContextManager()
        self.ctx = self.context_manager.ctx
        self.surface = self.context_manager.surface
        self.scale = self.context_manager.scale
        self.width = self.context_manager.width
        self.height = self.context_manager.height

        self.noise_scale = 0.0125
        self.noise_block_width = 1
        self.noise_map = np.zeros((
            self.width,
            self.height
        ))

        self.particle_life = 12
        self.particle_max_velocity = 4

        self.n_particles = 100
        self.particles = [
            self.spawn_particle()
            for _ in range(self.n_particles)
        ]

    def __getitem__(self, key):
        x, y = key

        if x >= len(self.noise_map) or y >= len(self.noise_map[x]):
            return None

        return self.noise_map[x, y]

    def spawn_particle(self):
        return (
            Particle().set_bounds(Vector(self.width, self.height))
                      .random_position(self.width, self.height)
                      .set_life(self.particle_life)
                      .set_max_velocity(self.particle_max_velocity)
                      .set_color(self.get_color)
        )

    def set_source_rgb(self, r=1, g=1, b=1, a=1):
        if max(r, g, b) > 1:
            r /= 255
            g /= 255
            b /= 255

        self.ctx.set_source_rgba(r, g, b, a)

    def set_background(self, r, g, b):
        self.set_source_rgb(r, r, b)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

    def save(self, name='output.png'):
        self.surface.write_to_png(name)

    def init_noise(self):
        for i in range(ceil(self.width / self.noise_block_width)):
            for j in range(ceil(self.height / self.noise_block_width)):
                self.noise_map[i][j] = pnoise2(
                    i * self.noise_scale,
                    j * self.noise_scale,
                    octaves=10,
                    persistence=0.35,
                    lacunarity=2.0,
                    repeatx=(self.width / self.noise_block_width) * self.noise_scale,
                    repeaty=(self.height / self.noise_block_width) * self.noise_scale
                )

        self.update_noise_interval()
        self.normalize_noise(amplitude=2.0 * pi)
        self.update_noise_interval()

    def normalize_noise(self, amplitude=1):
        for i in range(ceil(self.width / self.noise_block_width)):
            for j in range(ceil(self.height / self.noise_block_width)):
                self.noise_map[i][j] = (
                    (self.noise_map[i][j] - self.noise_range[0]) /
                    (self.noise_range[1] - self.noise_range[0])
                ) * amplitude - pi / 2

    def draw_noise(self):
        for i in range(ceil(self.width / self.noise_block_width)):
            for j in range(ceil(self.height / self.noise_block_width)):
                self.ctx.set_source_rgb(
                    self.noise_map[i][j] / (2.0 * pi),
                    self.noise_map[i][j] / (2.0 * pi),
                    self.noise_map[i][j] / (2.0 * pi)
                )
                self.ctx.rectangle(
                    i * self.noise_block_width,
                    j * self.noise_block_width,
                    self.noise_block_width - 1,
                    self.noise_block_width - 1
                )
                self.ctx.stroke_preserve()
                self.ctx.fill()

    def update_noise_interval(self):
        low = float('inf')
        high = float('-inf')

        for i in range(ceil(self.width / self.noise_block_width)):
            for j in range(ceil(self.height / self.noise_block_width)):
                low = min(low, self.noise_map[i][j])
                high = max(high, self.noise_map[i][j])

        self.noise_range = (low, high)

    def get_force(self, position):
        x, y = position.data
        x = floor(x / self.noise_block_width)
        y = floor(y / self.noise_block_width)

        angle = self[x, y]

        if angle is None:
            return None

        return Vector().from_angle(angle).set_mag(2)

    def step(self, n=1, log_interval=None):
        if log_interval is not None:
            print('step %6.2f%%' % (0))

        for i in range(n):
            for particle in self.particles:
                if not particle.alive:
                    continue

                particle.apply_force(self.get_force(particle.position))
                particle.step()
                self.draw_particle(particle)

            if log_interval is not None and (i % log_interval == 0 or i == n - 1) and i > 0:
                print('step %6.2f%%' % ((i / n) * 100))

            for k, v in enumerate(self.particles):
                if not v.alive:
                    self.particles[k] = self.spawn_particle()

        print('step %6.2f%%' % (100))

    def get_color(self, particle):
        a = (178, 34, 34)
        b = (64, 224, 208)

        x = particle.position.x
        v = particle.position.y / self.height

        if x < self.width * (1 / 3):
            return self.context_manager.lerp_rgb(a, b, v, mode='xyz')
        elif x < self.width * (2 / 3):
            return self.context_manager.lerp_rgb(a, b, v, mode='rgb')
        else:
            return self.context_manager.lerp_rgb(a, b, v, mode='lch')

    def lerp(self, a, b, c):
        return (a * c) + (1 - c) * b

    def draw_particle(self, particle):
        color_scale = 0.75
        self.set_source_rgb(
            particle.color[0] * color_scale,
            particle.color[1] * color_scale,
            particle.color[2] * color_scale,
            0.125 * 0.65
        )
        self.ctx.set_line_width(1)
        self.ctx.move_to(particle.position_old.x, particle.position_old.y)
        self.ctx.line_to(particle.position.x, particle.position.y)
        self.ctx.stroke()


if __name__ == '__main__':
    vf = VectorField()
    vf.set_background(250, 235, 215)
    vf.init_noise()
    # vf.draw_noise()
    vf.step(n=5000, log_interval=100)
    vf.save()
