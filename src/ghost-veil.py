from context_manager import ContextManager
from color_manager import ColorManager
from vector_field_background import VectorFieldBackground
from random_controller import RandomController
from particle import Particle
from vector import Vector
from utils import lerp, random_name
from random import uniform
from math import sqrt, floor, pi


class GhostVeil:
    def __init__(self, context=None, width=1, height=1):
        self.width = width
        self.height = height
        self.context = context

        self.particles = []

        self.color_name = 'thistle'
        self.color = None

    def spawn_particle(self):
        return Particle()

    def spawn_particles(self, n_particles=10):
        self.n_particles = n_particles
        self.particles = [
            self.spawn_particle()
                .set_velocity(Vector().random().set_mag(5))
            for _ in range(self.n_particles)
        ]
        return self

    def set_color(self, color_name='', color=None):
        self.color_name = color_name
        self.color = color
        return self

    def get_color(self, alpha=1):
        if self.color is None:
            return ColorManager().get_color(self.color_name, alpha=alpha)
        else:
            return self.color

    def draw(self, alpha=1):
        ctx = self.context.ctx
        ctx.set_line_width(1)
        for i, _ in enumerate(self.particles):
            if i > 0:
                ctx = self.context.ctx
                ctx.set_line_width(1)
                self.context.set_source_rgb(
                    self.get_color(alpha=alpha)
                )

                ctx.move_to(
                    self.particles[i].position.x,
                    self.particles[i].position.y
                )

                ctx.line_to(
                    self.particles[i - 1].position.x,
                    self.particles[i - 1].position.y
                )

                ctx.stroke()

    def initial_placement(self, height=None):
        if height is None:
            posy = self.height / 2.0
        else:
            posy = height

        posx = 0

        for i in range(self.n_particles):
            posx = i * self.width / self.n_particles + (self.width / self.n_particles) * 0.5
            self.particles[i].position.x = posx
            self.particles[i].position.y = posy

        return self

    def step(self, n=1):
        for _ in range(n):
            for particle in self.particles:
                particle.apply_force(
                    Vector().random().set_mag(1.25)
                )
                particle.step()

            self.draw(alpha=0.075)


def main():
    width = int(floor(1000))
    height = int(floor(width))

    context = ContextManager()
    context.set_resolution(
        width=width,
        height=height,
        scale=4
    ).create_surface()
    context.set_background(
        ColorManager().get_color('cornsilk')
    )

    ghost_veil = GhostVeil(
        context=context,
        width=context.width,
        height=context.height
    )

    dx = height * 0.1
    max_value = floor(height / dx)

    for i in range(max_value):
        color = context.lerp_rgb(
            ColorManager().get_color('orange red'),
            ColorManager().get_color('steel blue'),
            (i / max_value),
            mode='lch'
        )

        ghost_veil \
            .spawn_particles(n_particles=10) \
            .set_color(color=color) \
            .initial_placement(height=dx * i + dx * 0.5) \
            .step(n=25)

    # context.save(random_name(
    #     prefix='ghost-veil'
    # ))

    context.save('ghost-veil.png')

if __name__ == '__main__':
    main()
