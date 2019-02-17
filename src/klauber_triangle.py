import numpy as np


class KlauberTriangle():
    def __init__(self, context=None, width=800, height=600):
        self.context = context
        self.width = width
        self.height = height

        self.prime_grid = None

    def draw(self, center_x, center_y, size, block_size=10, space=2):
        self.calculate_prime_matrix(size)

        ctx = self.context.ctx

        self.context.set_source_rgb(1, 0, 0)

        width = (block_size + space)

        x_offset = width * self.ncols / 2
        y_offset = width * self.nrows / 2

        for i in range(self.nrows):
            for j in range(self.ncols):
                x = center_x - j * width + x_offset
                y = center_y + i * width - y_offset

                if self.prime_grid[i, j]:
                    ctx.rectangle(x, y, block_size, block_size)
                    ctx.fill()

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
