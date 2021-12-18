from lib.context_manager import ContextManager
from lib.random_controller import RandomController
from lib.color_manager import ColorManager
from lib.particle import Particle
from lib.vector import Vector
from lib.utils import random_name, signal

from random import uniform, choice, randint
from math import floor, sin, cos, radians


class Dalmatian:
    def __init__(self, context):
        self.context = context

    def draw(self, x, y, min_dots=7, max_dots=15):
        a = 50
        for _ in range(randint(min_dots, max_dots)):
            Blob(self.context).draw(
                x + uniform(-a, a),
                y + uniform(-a, a),
                strenght=4,
                radius=uniform(4, 12),
                step=15,
                smoothing=7,
                magnitude=1,
            )


class Blob:
    def __init__(self, context):
        self.context = context

    def draw(
        self, x, y, strenght=5, radius=25, step=25, smoothing=15, fill=True, magnitude=5
    ):
        ctx = self.context.ctx
        points = []

        for angle in range(0, 360, int(360 / step)):
            x_ = x + radius * sin(radians(angle))
            y_ = y + radius * cos(radians(angle))

            points.append(Vector(x_, y_))

        for p in points:
            p.set(p + Vector().random().set_mag(strenght * magnitude))

        ctx.set_line_width(8)

        for _ in range(smoothing):
            for i in range(len(points)):
                a = points[(i - 1) % len(points)]
                b = points[i]
                c = points[(i + 1) % len(points)]
                v = a + b + c
                v.x = v.x / 3.0
                v.y = v.y / 3.0
                b.set(v)

        ctx.move_to(*points[0].data)
        for p in points[1:]:
            ctx.line_to(*p.data)

        if fill:
            ctx.fill()
        else:
            ctx.line_to(*points[0].data)
            ctx.stroke()


def main():
    width = int(floor(1000))
    height = int(floor(width))

    color_manager = ColorManager()

    context = ContextManager()
    context.set_resolution(
        width=width, height=height, scale=4
    ).create_surface().set_background(color_manager.get_color("off white"))

    # START

    context.set_source_rgb(ColorManager().get_color("tumbleweed"))
    Blob(context).draw(800, 775, strenght=10, radius=250, step=60, smoothing=7)

    RandomController(59799479867451)
    i = 0
    for _ in range(10):
        x = uniform(0, width)
        y = uniform(0, height)

        colors = ["almond", "tumbleweed", "bone"]
        i += 1
        context.set_source_rgb(ColorManager().get_color(colors[i % len(colors)]))
        Blob(context).draw(x, y, strenght=10, radius=250, step=60, smoothing=7)

    RandomController(216350572992617)
    context.set_source_rgb(ColorManager().get_color("midnight green"))
    for _ in range(10):
        Dalmatian(context).draw(uniform(0, width), uniform(0, height))

    RandomController(132780261639155)
    context.set_source_rgb(ColorManager().get_color("midnight green"))
    for _ in range(5):
        Dalmatian(context).draw(uniform(0, width), uniform(0, height), min_dots=10, max_dots=25)

    RandomController(59799479867451)
    context.set_source_rgb(ColorManager().get_color("sinopia"))
    Blob(context).draw(
        340, 0, strenght=10, radius=375, step=120, smoothing=30, fill=False
    )
    Blob(context).draw(
        1100, 500, strenght=10, radius=400, step=120, smoothing=20, fill=False
    )
    Blob(context).draw(
        300, 1100, strenght=10, radius=375, step=120, smoothing=25, fill=False
    )

    # END

    name = random_name(
        prefix="multiple_blobs",
        extension="png",
    )
    print(f"saving to {name}")
    context.save(name)


if __name__ == "__main__":
    main()
