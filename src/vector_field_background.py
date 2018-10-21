# pylint: disable=E1101
import cairo
import os

import numpy as np

from context_manager import ContextManager
from color_manager import ColorManager
from vector import Vector
from particle import Particle

from noise import snoise2, pnoise2
from random import random, uniform, seed
from math import pi, sin, cos, sqrt, ceil, floor
from utils import color_lerp


class VectorFieldBackground:
    def __init__(self, context=None):
        if context is None:
            self.context_manager = ContextManager()
        else:
            self.context_manager = context

        self.ctx = self.context_manager.ctx
        self.surface = self.context_manager.surface
        self.scale = self.context_manager.scale
        self.width = self.context_manager.width
        self.height = self.context_manager.height

        self.color = (255, 0, 0)

        self.noise_scale = 0.0125
        self.noise_block_width = 2
        self.noise_map = np.zeros((
            self.context_manager.width,
            self.context_manager.height
        ))
        self.noise_initialized = False

    def __getitem__(self, key):
        x, y = key

        if x >= len(self.noise_map) or y >= len(self.noise_map[x]):
            return None

        return self.noise_map[x, y]

    def set_bounds(self, width, heigth):
        self.width = width
        self.height = heigth
        return self

    def set_noise_scale(self, scale):
        self.noise_scale = scale
        return self

    def set_noise_block_width(self, width):
        self.noise_block_width = width
        return self

    def init_noise(self, mode='perlin'):
        if mode == 'perlin':
            return self.init_noise_perlin()

    def init_noise_perlin(self):
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

        return self

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
        return self

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

        return Vector().from_angle(angle).set_mag(1)

    def draw_vectors(self):
        for i in range(ceil(self.width / self.noise_block_width)):
            for j in range(ceil(self.height / self.noise_block_width)):
                self.draw_vector(i, j)
        return self

    def draw_vector(self, x, y):
        if random() < 0.35:
            return

        half_block = self.noise_block_width / 2
        self.context_manager.set_source_rgb(
            color_lerp(
                color_lerp(
                    ColorManager().get_color('cornsilk'),
                    (0, 0, 0),
                    0.975
                ),
                (1, 1, 1),
                0.975
            )
        )
        ctx = self.context_manager.ctx
        ctx.set_line_width(1)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)

        from_x = x * self.noise_block_width + half_block
        from_y = y * self.noise_block_width + half_block

        # ctx.save()
        # ctx.translate(from_x, from_y)
        to_x, to_y = (
            self.get_force(Vector(from_x, from_y))
            .set_mag(self.noise_block_width * 0.8)
            .data
        )
        # ctx.move_to(from_x, from_y)
        # ctx.line_to(from_x + to_x, from_y + to_y)
        ctx.arc(from_x + to_x, from_y + to_y, half_block, 0, 2.0 * pi)
        # print(from_x, from_y, to_x, to_y)

        if random() < 0.15:
            ctx.fill_preserve()

        ctx.stroke()
        # ctx.restore()
