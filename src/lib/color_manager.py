class ColorManager:
    def __init__(self):
        self.colors = {
            'cornsilk':       ( 255 , 248 , 220 ) , # fff8dc
            'thistle':        ( 216 , 191 , 216 ) , # d8bfd8
            'orange red':     ( 255 , 69  , 0   ) , # ff4500
            'powder blue':    ( 176 , 224 , 230 ) , # b0e0e6
            'steel blue':     ( 70  , 130 , 180 ) , # 4682b4
            'midnight green': ( 29  , 69  , 77  ) , # 1d454d
            'azure':          ( 240 , 255 , 255 ) , # f0ffff
            'honeydew':       ( 240 , 255 , 240 ) , # f0fff0
            'green yellow':   ( 173 , 255 , 47  ) , # adff2f
            'off white':      ( 251 , 250 , 248 ) , # fbfaf8
            'sinopia':        ( 193 , 81  , 35  ) , # c15123
            'almond':         ( 243 , 225 , 205 ) , # f3e1cd
            'tumbleweed': (198, 161, 134), # c6a186
            'bone':           ( 220, 214, 202), # dcd6ca
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
