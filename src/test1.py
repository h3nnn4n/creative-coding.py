# pylint: disable=E1101
import cairo
import os

from random import random, uniform, seed
from math import pi, sin, cos, sqrt

scale = 4
width = 600
height = 600

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width * scale, height * scale)
surface.set_device_scale(scale, scale)
ctx = cairo.Context(surface)

surface_mask = cairo.ImageSurface(cairo.FORMAT_ARGB32, width * scale, height * scale)
surface_mask.set_device_scale(scale, scale)
ctx_mask = cairo.Context(surface_mask)


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

# seed(729890378782812217)
# seed(12584113332985461323)
seed(16844609366066532813)

set_background(ctx)

ctx_mask.set_source_rgba(255 / 255, 255 / 255, 255 / 255, 0)
ctx_mask.rectangle(0, 0, width, height)
ctx_mask.fill()

# set_background(ctx_mask)

# circle_thing(ctx)

# circles = [
#     (width * 0.50, height * 0.39, width * 0.15),
#     (width * 0.35, height * 0.65, width * 0.15),
#     (width * 0.65, height * 0.65, width * 0.15)
# ]

# for x, y, r in circles:
#     circle_thing(
#         ctx,
#         x=x,
#         y=y,
#         r=r
#     )

x_center = width / 2
y_center = height / 2
radius = width * 0.20
points = 3
angle_step = 2.0 * pi / points
circle_radius = sqrt(2 * (radius ** 2) - 2 * (radius ** 2) * cos(angle_step)) / 2

for i in range(points):
    angle = angle_step * i
    x = x_center + radius * sin(angle)
    y = y_center + radius * cos(angle)

    # circle_thing(
    #     ctx,
    #     x=x,
    #     y=y,
    #     r=circle_radius
    # )

    ctx_mask.set_source_rgba(0.5, 0, 0, 0.5)
    ctx_mask.arc(x, y, circle_radius, 0, 2 * pi)
    ctx_mask.fill()

circle_thing(
    ctx,
    x=x_center,
    y=y_center,
    r=radius - circle_radius
)

ctx_mask.set_source_rgba(0.5, 0, 0, 0.5)
ctx_mask.arc(x_center, y_center, radius - circle_radius, 0, 2 * pi)
ctx_mask.fill()

ctx.mask_surface(surface_mask)

draw_lines(ctx, n_lines=500)

# ctx.mask_surface(surface_mask)

# circle_thing(ctx, width * 0.12, height * 0.89, width * 0.04)

surface.write_to_png('rectangle.png')
surface_mask.write_to_png('rectangle_mask.png')
