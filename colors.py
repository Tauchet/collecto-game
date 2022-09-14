class Color():

    def __init__(self, name, symbol, ball_image_url):
        self.name = name
        self.symbol = symbol
        self.ball_image_url = ball_image_url

    def __repr__(self):
        return f"{self.symbol}"

COLOR_EMPTY = 'E'
COLOR_WHITE = Color('Blanco', 'W', 'white_ball.png')
COLOR_RED = Color('Rojo', 'R', 'red_ball.png')
COLOR_YELLOW = Color('Amarillo', 'Y', 'yellow_ball.png')
COLOR_GREEN = Color('Verde', 'G', 'green_ball.png')
COLOR_MAGENTA = Color('Magenta', 'M', 'magenta_ball.png')
COLOR_BLUE = Color('Azúl', 'B', 'blue_ball.png')

COLORS = (
    COLOR_WHITE,
    COLOR_RED,
    COLOR_YELLOW,
    COLOR_GREEN,
    COLOR_MAGENTA,
    COLOR_BLUE
)