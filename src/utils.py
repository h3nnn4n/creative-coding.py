from colormath.color_objects import sRGBColor, LCHuvColor, XYZColor


def lerp(a, b, c):
    return (a * c) + (1 - c) * b


def normalize_rgb(r, g=None, b=None, a=None):
    if type(r) is tuple:
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


def color_lerp(a, b, v):
    if type(a) is not tuple:
        a = color_to_tuple(a)

    if type(b) is not tuple:
        b = color_to_tuple(b)

    return (
        lerp(a[0], b[0], v),
        lerp(a[1], b[1], v),
        lerp(a[2], b[2], v)
    )


def color_to_tuple(a):
    if type(a) is LCHuvColor:
        return (a.lch_l, a.lch_c, a.lch_h)

    if type(a) is sRGBColor:
        return (a.rgb_r, a.rgb_g, a.rgb_b)

    if type(a) is XYZColor:
        return (a.xyz_x, a.xyz_y, a.xyz_z)


def tuple_to_LCHuvColor(a):
    return LCHuvColor(a[0], a[1], a[2])


def tuple_to_XYZColor(a):
    return XYZColor(a[0], a[1], a[2])
