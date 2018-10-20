# pylint: disable=E1101
import cairo
import os

from random import random, uniform, seed
from math import pi

scale = 4
width = 600
height = 600

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width * scale, height * scale)
ctx = cairo.Context(surface)
surface.set_device_scale(scale, scale)


def draw_line_from_sequence(ctx, points, color):
    ctx.set_source_rgba(color[0], color[1], color[2], color[3])
    ctx.set_line_width(1)

    ctx.move_to(points[0][0], points[0][1])

    for (x, y) in points[1:]:
        ctx.line_to(x, y)

    ctx.stroke()


def circle_clip(ctx, x=None, y=None, r=None):
    if x is None:
        x = width / 2

    if y is None:
        y = height / 2

    if r is None:
        r = min(x, y) * 0.25

    ctx.arc(x, y, r, 0, 2 * pi)
    ctx.clip()


def update_points(points):
    for i in range(len(points)):
        points[i] = (
            points[i][0] + uniform(-2, 2),
            points[i][1] + uniform(-2, 2)
        )


def update_color(color):
    for i in range(3):
        color[i] += uniform(-1, 1) / 40


def set_background(ctx):
    ctx.set_source_rgb(255 / 255, 255 / 255, 255 / 255)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()


def draw_lines(ctx, n_groups=3, n_lines=100):
    for _ in range(n_groups):
        points = [
            (random() * width, random() * height)
            for _ in range(4)
        ]

        color = [73 / 255, 137 / 255, 153 / 255, 0.01]

        for _ in range(n_lines):
            update_color(color)
            update_points(points)
            draw_line_from_sequence(ctx, points, color)


def circle_thing(ctx, x=None, y=None, r=None):
    if x is None:
        x = width / 2

    if y is None:
        y = height / 2

    if r is None:
        r = min(x, y) * 0.5

    # ctx.set_source_rgb(0 / 255, 0 / 255, 0 / 255)
    # ctx.arc(x, y, r, 0, 2 * pi)
    # ctx.fill()

    circle_clip(ctx, x, y, r)
    draw_lines(ctx, n_groups=20, n_lines=500)
    ctx.reset_clip()


# random_data = os.urandom(8)
# seed_value = int.from_bytes(random_data, byteorder="big")
# seed(seed_value)
# print('seed(%d)' % seed_value)

seed(729890378782812217)

set_background(ctx)
circle_thing(ctx)

circles = [
    (width * 0.16, height * 0.14, width * 0.11),
    (width * 0.70, height * 0.12, width * 0.09),
    (width * 0.46, height * 0.86, width * 0.04),
    (width * 0.89, height * 0.52, width * 0.16),
]

for x, y, r in circles:
    circle_thing(
        ctx,
        x=x,
        y=y,
        r=r
    )

draw_lines(ctx, n_lines=500)

circle_thing(ctx, width * 0.12, height * 0.89, width * 0.04)

surface.write_to_png('rectangle.png')
