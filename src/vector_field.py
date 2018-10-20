# pylint: disable=E1101
import cairo
import os

import numpy as np

from noise import snoise2, pnoise2
from random import random, uniform, seed
from math import pi, sin, cos, sqrt, ceil


class Vector:
    def __init__(self, x=0, y=0):
        self.data = np.zeros(2)

    def set_x(self, x):
        self.data[0] = x

    def set_y(self, y):
        self.data[1] = y

    def get_x(self):
        return self.data[0]

    def get_y(self):
        return self.data[1]

    def __add__(self, other):
        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def zero(self):
        self.x = 0
        self.y = 0

    x = property(get_x, set_x)
    y = property(get_y, set_y)


class Particle:
    def __init__(self):
        self.position = Vector()
        self.position_old = Vector()
        self.velocity = Vector()
        self.acceleration = Vector()


class VectorField:
    def __init__(self):
        self.scale = 4
        self.width = 600
        self.height = 600

        self.noise_scale = 0.0125
        self.noise_block_width = 2
        self.noise_map = np.zeros((
            self.width,
            self.height
        ))

        self.n_particles = 10
        self.particles = [
            Particle()
            for _ in range(self.n_particles)
        ]

        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            self.width * self.scale,
            self.height * self.scale
        )
        self.surface.set_device_scale(self.scale, self.scale)
        self.ctx = cairo.Context(self.surface)

    def set_background(self):
        self.ctx.set_source_rgb(0, 0, 0)
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
                    octaves=4,
                    persistence=0.5,
                    lacunarity=2.25,
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
                ) * amplitude

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

vf = VectorField()
vf.set_background()
vf.init_noise()
vf.draw_noise()
vf.save()
