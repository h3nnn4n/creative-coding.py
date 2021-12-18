import string

from colormath.color_objects import sRGBColor, LCHuvColor, XYZColor
from datetime import datetime
from random import sample


def lerp(a, b, c):
    return (a * c) + (1 - c) * b


def normalize_rgb(r, g=None, b=None, a=None):
    if isinstance(r, tuple):
        if len(r) == 3:
            return normalize_rgb_(r)
        else:
            return normalize_rgba_(r)

    if a is None:
        return normalize_rgb_((r, g, b))

    return normalize_rgba_((r, g, b, a))


def normalize_rgb_(color):
    r, g, b = color

    if max(r, g, b) > 1:
        r /= 255
        g /= 255
        b /= 255

    return r, g, b


def normalize_rgba_(color):
    r, g, b, a = color

    if max(r, g, b) > 1:
        r /= 255
        g /= 255
        b /= 255
        a /= 255

    return r, g, b, a


def add_alpha_to_color(color, alpha):
    return (color[0], color[1], color[2], alpha)


def color_lerp(a, b, v):
    if not isinstance(a, tuple):
        a = color_to_tuple(a)

    if not isinstance(b, tuple):
        b = color_to_tuple(b)

    return (
        lerp(a[0], b[0], v),
        lerp(a[1], b[1], v),
        lerp(a[2], b[2], v)
    )


def color_to_tuple(a):
    if isinstance(a, LCHuvColor):
        return (a.lch_l, a.lch_c, a.lch_h)

    if isinstance(a, sRGBColor):
        return (a.rgb_r, a.rgb_g, a.rgb_b)

    if isinstance(a, XYZColor):
        return (a.xyz_x, a.xyz_y, a.xyz_z)


def tuple_to_LCHuvColor(a):
    return LCHuvColor(a[0], a[1], a[2])


def tuple_to_XYZColor(a):
    return XYZColor(a[0], a[1], a[2])


def random_name(prefix=None, suffix=None, extension='png'):
    name = ''

    now = datetime.now()
    char_set = string.ascii_uppercase + string.digits
    r_string = ''.join(sample(char_set * 6, 6))
    time_string = '-'.join(map(str, [
        now.year, now.month, now.day, now.hour, now.minute, now.second
    ]))

    if prefix is not None:
        name += str(prefix)
        name = '_'.join([name, time_string])
    else:
        name += time_string

    name = '_'.join([name, r_string])

    if suffix is not None:
        name = '_'.join([name, str(suffix)])

    name = '.'.join([name, extension])

    return name


def signal(value):
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0
