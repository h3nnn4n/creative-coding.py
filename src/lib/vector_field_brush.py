# pylint: disable=E1101
import cairo
import os

import numpy as np

from .context_manager import ContextManager
from .vector import Vector
from .particle import Particle

from noise import snoise2, pnoise2
from random import random, uniform, seed
from math import pi, sin, cos, sqrt, ceil, floor


class VectorFieldBrush:
    def __init__(self, context=None):
        if context is None:
            self.context_manager = ContextManager()
        else:
            self.context_manager = context

        self.ctx = self.context_manager.ctx
        self.surface = self.context_manager.surface
        self.scale = self.context_manager.scale
        self.width = None
        self.height = None

        self.color = (255, 0, 0)

        self.noise_scale = 0.0125
        self.noise_block_width = 1
        self.noise_map = np.zeros((
            self.context_manager.width,
            self.context_manager.height
        ))
        self.noise_initialized = False

        self.particle_life = 12
        self.particle_max_velocity = 4

        self.n_particles = 100
        self.particles = []

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

    def set_particle_life(self, life):
        self.particle_life = life
        return self

    def set_particle_max_velocity(self, max_velocity):
        self.particle_max_velocity = max_velocity
        return self

    def spawn_particle(self):
        return (
            Particle().set_bounds(Vector(self.width, self.height))
                      .random_position(self.width, self.height)
                      .set_life(self.particle_life)
                      .set_max_velocity(self.particle_max_velocity)
                      .set_color(self.get_color)
        )

    def spawn_particles(self):
        self.particles = [
            self.spawn_particle()
            for _ in range(self.n_particles)
        ]

        return self

    def get_color(self, _):
        return self.color

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
        if len(self.particles) == 0:
            self.spawn_particles()

        if not self.noise_initialized:
            self.init_noise()

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

    def draw_particle(self, particle):
        color_scale = 0.75
        self.context_manager.set_source_rgb(
            particle.color[0] * color_scale,
            particle.color[1] * color_scale,
            particle.color[2] * color_scale,
            0.125 * 0.65
        )
        self.ctx.set_line_width(1)
        self.ctx.move_to(particle.position_old.x, particle.position_old.y)
        self.ctx.line_to(particle.position.x, particle.position.y)
        self.ctx.stroke()

    def circle(self, center_x, center_y, radius, color, steps=250):
        ctx = self.ctx
        self.color = color
        self.set_bounds(radius * 2, radius * 2)
        self.spawn_particles()

        ctx.save()
        ctx.translate(center_x, center_y)
        ctx.arc(radius, radius, radius, 0, 2 * pi)
        ctx.clip()
        self.step(n=steps)
        ctx.reset_clip()
        ctx.restore()
