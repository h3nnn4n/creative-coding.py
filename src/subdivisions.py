from context_manager import ContextManager
from color_manager import ColorManager
from particle import Particle
from utils import lerp
from random import uniform


class Subdivision:
    def __init__(self, context=None, width=1, height=1):
        self.width = width
        self.height = height
        self.context = context

        self.n_particles = 3
        self.particles = []

    def spawn_particle(self):
        return Particle()

    def spawn_particles(self):
        self.particles = [
            self.spawn_particle()
            for _ in range(self.n_particles)
        ]
        return self

    def initial_placement(self, points=[]):
        for k, (x, y) in enumerate(points):
            self.particles[k].position.x = x
            self.particles[k].position.y = y
        return self

    def draw(self, alpha=0.1):
        ctx = self.context.ctx

        ctx.move_to(
            self.particles[0].position.x,
            self.particles[0].position.y
        )

        for particle in self.particles[1:]:
            ctx.line_to(
                particle.position.x,
                particle.position.y
            )

        ctx.close_path()
        ctx.set_line_width(1)
        self.context.set_source_rgb(
            ColorManager().get_color('thistle', alpha=alpha * 2)
        )
        ctx.stroke_preserve()
        self.context.set_source_rgb(
            ColorManager().get_color('thistle', alpha=alpha)
        )
        ctx.fill()

    def split(self):
        for i in range(len(self.particles) - 1, 0, -1):
            a = self.particles[i].position
            b = self.particles[i - 1].position
            scale = a.dist(b) * 0.25
            self.particles.insert(
                i,
                Particle().set_position(
                    lerp(a.x, b.x, 0.5) + uniform(-scale, scale),
                    lerp(a.y, b.y, 0.5) + uniform(-scale, scale)
                )
            )

    def step(self, n=1):
        if len(self.particles) == self.n_particles:
            self.draw()

        for _ in range(n):
            self.split()
            self.draw(alpha=0.075)


def main():
    # color_manager = ColorManager()
    context = ContextManager()
    context.set_background(
        ColorManager().get_color('cornsilk')
    )
    subdivision = Subdivision(
        context=context,
        width=context.width,
        height=context.height
    ).spawn_particles() \
     .initial_placement(
        [
            (context.width * 0.5, context.height * 0.1),
            (context.width * 0.3, context.height * 0.5),
            (context.width * 0.5, context.height * 0.9)
        ]
    )
    subdivision.step(n=12)

    context.save('subdivisions.png')

if __name__ == '__main__':
    main()
