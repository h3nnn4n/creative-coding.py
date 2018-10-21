class ColorManager:
    def __init__(self):
        self.colors = {
            'cornsilk': (255, 248, 220),
            'thistle': (216, 191, 216)
        }

    def get_color(self, key, alpha=1.0, normalized=True):
        if key in self.colors.keys():
            return (
                *self.normalized(self.colors[key]),
                alpha
            )

    def normalized(self, color):
        if max(color) > 1:
            return (
                color[0] / 255,
                color[1] / 255,
                color[2] / 255
            )

        return color
