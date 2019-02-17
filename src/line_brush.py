import random
from context_manager import ContextManager
from color_manager import ColorManager
from math import pi, floor, sin, cos


class LineBrush:
    def __init__(self, context=None, width=800, height=800):
        if context is None:
            context = ContextManager()

        self.context = context
        self.width = width
        self.height = height

        self.color = ColorManager().get_color('orange red')

        self.backend = None
        self.backend_options = {}
        self.set_backend()

    def set_color(self, color, alpha=1):
        if isinstance('', str):
            color = ColorManager().get_color(color, alpha=alpha)

        self.color = color

        return self

    def set_backend(self, backend_name='straight_lines', options={}, overwrite=False):
        if overwrite:
            self.backend_options = options.copy()
        else:
            self.backend_options = {**self.backend_options, **options}

        if backend_name == 'straight_lines':
            self.backend = self.random_lines
            if 'n_lines' not in self.backend_options.keys():
                self.backend_options['n_lines'] = 100

        return self

    def random_lines(self):
        n_lines = self.backend_options['n_lines']
        block_size = self.backend_options['block_size']

        ctx = self.context.ctx

        ctx.set_line_width(1)
        self.context.set_source_rgb(self.color)

        for _ in range(n_lines):
            x1, y1 = random.uniform(0, block_size), random.uniform(0, block_size)
            x2, y2 = random.uniform(0, block_size), random.uniform(0, block_size)

            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)

            ctx.stroke()

    def circle(self, center_x, center_y, radius, contour=True):
        ctx = self.context.ctx

        ctx.save()
        ctx.translate(center_x - radius, center_y - radius)
        ctx.arc(radius, radius, radius, 0, 2 * pi)
        ctx.clip()

        if contour:
            ctx.set_line_width(1)
            self.context.set_source_rgb(self.color)
            ctx.arc(radius, radius, radius, 0, 2 * pi)

        self.backend_options['block_size'] = radius * 2
        self.backend()

        ctx.reset_clip()
        ctx.restore()


def main():
    width = int(floor(1000))
    height = int(floor(width))

    context = ContextManager() \
        .set_resolution(width=width, height=height, scale=4) \
        .create_surface() \
        .set_background(ColorManager().get_color('cornsilk'))

    line_brush = LineBrush(context=context, width=width, height=height)

    n_circles = 6
    circle_radius = 50
    outer_circle_radius = 125

    line_brush.circle(width / 2, height / 2, circle_radius)

    for i in range(0, n_circles):
        angle = i / n_circles * pi * 2

        center_x = outer_circle_radius * sin(angle) + width / 2
        center_y = outer_circle_radius * cos(angle) + height / 2
        line_brush.circle(center_x, center_y, circle_radius)

    context.save('line_brush.png')


if __name__ == "__main__":
    main()
