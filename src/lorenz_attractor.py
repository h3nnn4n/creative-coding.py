import cmapy
import random
import numpy as np
from scipy.integrate import odeint

from lib.context_manager import ContextManager
from lib.color_manager import ColorManager
from lib.utils import add_alpha_to_color, normalize_rgb


def lorenz(X, t, sigma, beta, rho):
    u, v, w = X

    up = -sigma * (u - v)
    vp = rho * u - v - u * w
    wp = -beta * w + u * v

    return up, vp, wp


def calculate_lorenz(tmax=100, n_points=10000, sigma=10, beta=2.667, rho=28, u0=0, v0=1, w0=1.05):
    t = np.linspace(0, tmax, n_points)
    f = odeint(lorenz, (u0, v0, w0), t, args=(sigma, beta, rho))
    x, y, z = f.T

    return x, y, z


def main():
    color_manager = ColorManager()
    context_manager = ContextManager()

    ctx = context_manager.ctx
    surface = context_manager.surface
    scale = context_manager.scale
    width = context_manager.width
    height = context_manager.height

    alpha = 0.05
    color = color_manager.get_color("steel blue", alpha=alpha)
    context_manager.set_source_rgb(color)

    scale = 8.0

    ctx.translate(width / 2, height * 0.75)
    ctx.set_line_width(0.5)

    n_iters = 25
    for i in range(n_iters):
        print("%3d %%" % ((i+1) / n_iters * 100))

        color = cmapy.color('cool', i / n_iters, rgb_order=True)
        color = normalize_rgb(tuple(color))
        color = add_alpha_to_color(color, alpha)
        context_manager.set_source_rgb(color)

        x_t, y_t, z_t = calculate_lorenz(
            tmax=2 * 10**2,
            n_points=5 * 10**4,
            u0=random.random(),
            v0=random.random(),
            w0=random.random(),
        )
        xt, yt = x_t, z_t

        ctx.move_to(xt[0] * scale, yt[0] * -scale)

        count = 0

        for x, y in zip(xt[1:], yt[1:]):
            ctx.line_to(x * scale, y * -scale)

            count += 1

            if count > 100:
                count = 0
                ctx.stroke()
                ctx.move_to(x * scale, y * -scale)

        ctx.stroke()

    context_manager.save()


if __name__ == '__main__':
    main()
