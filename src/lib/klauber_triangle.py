import numpy as np

from math import pi, sin, cos
from random import uniform

from .color_manager import ColorManager


class KlauberTriangle():
    def __init__(self, context=None, width=800, height=600):
        self.context = context
        self.width = width
        self.height = height

        self.prime_grid = None

    def draw(self, center_x, center_y, size, block_size=10, space=2):
        self.calculate_prime_matrix(size)

        ctx = self.context.ctx

        width = (block_size + space)

        x_offset = width * self.ncols / 2
        y_offset = width * self.nrows / 2

        # self.background_triangle(center_x, center_y, x_offset, y_offset)

        ctx.set_line_width(2.5)
        # self.context.set_source_rgb(175, 50, 50, 100)
        # self.context.set_source_rgb(ColorManager().get_color('thistle'))

        for i in range(self.nrows):
            for j in range(self.ncols):
                x = center_x - (j + 1.5) * width + x_offset
                y = center_y + i * width - y_offset

                if self.prime_grid[i, j]:
                    # ctx.rectangle(x, y, block_size, block_size)
                    color = self.context.lerp_rgb(
                        ColorManager().get_color('orange red'),
                        ColorManager().get_color('steel blue'),
                        (uniform(0, 1)),
                        mode='xyz'
                    )

                    self.context.set_source_rgb((*color, uniform(0.55, 0.9)))

                    ctx.arc(x, y, block_size / 2, 0, 2 * pi)
                    if uniform(0, 1) < 0.5:
                        ctx.stroke()
                    else:
                        ctx.fill()

    def background_triangle(self, center_x, center_y, x_offset, y_offset):
        ctx = self.context.ctx

        self.context.set_source_rgb(155, 58, 20, 75)
        ctx.set_line_width(1)

        ctx.move_to(center_x, center_y - y_offset)
        ctx.line_to(center_x + x_offset, center_y + y_offset)
        ctx.line_to(center_x - x_offset, center_y + y_offset)
        ctx.line_to(center_x, center_y - y_offset)

        ctx.stroke()

    def calculate_prime_matrix(self, size):
        n = size
        ncols = 2 * n + 1
        nmax = n**2

        primes = np.array([n for n in range(2, n**2 + 1) if all((n % m) != 0 for m in range(2, int(np.sqrt(n)) + 1))])
        a = np.zeros(nmax)
        a[primes - 1] = 1

        arr = np.zeros((n, ncols))
        for i in range(n):
            arr[i, (n - i):(n + i + 1)] = a[i**2:i**2 + 2 * i + 1]

        self.prime_grid = arr
        self.ncols = ncols
        self.nrows = ncols // 2
