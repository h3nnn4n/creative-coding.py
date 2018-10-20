# pylint: disable=E1101
import cairo

from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LCHuvColor, XYZColor
from utils import lerp, color_lerp, normalize_rgb, tuple_to_LCHuvColor, \
    tuple_to_XYZColor, color_to_tuple


class ContextManager:
    def __init__(self):
        self.set_resolution()
        self.create_surface()
        self.set_background()

    def set_resolution(self, width=600, height=600, scale=4):
        self.scale = scale
        self.width = width
        self.height = height

        return self

    def create_surface(self):
        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            self.width * self.scale,
            self.height * self.scale
        )
        self.surface.set_device_scale(self.scale, self.scale)
        self.ctx = cairo.Context(self.surface)

        return self

    def set_background(self, r=1, g=1, b=1):
        self.set_source_rgb(r, g, b)
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.fill()

        return self

    def save(self, name='output.png'):
        self.surface.write_to_png(name)

    def set_source_rgb(self, r=1, g=1, b=1, a=1):
        r, g, b = normalize_rgb(r, g, b)
        self.ctx.set_source_rgba(r, g, b, a)

    def lerp_rgb(self, a, b, p, mode='lch'):
        if mode == 'lch':
            return self.lerp_rgb_via_lch(a, b, p)

        if mode == 'xyz':
            return self.lerp_rgb_via_xyz(a, b, p)

        if mode == 'rgb':
            return color_lerp(a, b, p)

    def lerp_rgb_via_lch(self, a, b, p):
        return self.lerp_rgb_via(a, b, p, 'lch')

    def lerp_rgb_via_xyz(self, a, b, p):
        return self.lerp_rgb_via(a, b, p, 'xyz')

    def lerp_rgb_via(self, a, b, p, mode='lch'):
        if mode == 'lch':
            color_object = LCHuvColor
        elif mode == 'xyz':
            color_object = XYZColor

        a = normalize_rgb(a)
        b = normalize_rgb(b)

        color_a = sRGBColor(a[0], a[1], a[2])
        color_b = sRGBColor(b[0], b[1], b[2])

        color_a_ = convert_color(color_a, color_object)
        color_b_ = convert_color(color_b, color_object)

        if mode == 'lch':
            color_c_ = tuple_to_LCHuvColor(
                color_lerp(color_a_, color_b_, p)
            )
        elif mode == 'xyz':
            color_c_ = tuple_to_XYZColor(
                color_lerp(color_a_, color_b_, p)
            )

        color_c = color_to_tuple(convert_color(color_c_, sRGBColor))

        return color_c
