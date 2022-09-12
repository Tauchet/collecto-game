class Color():

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return f"{self.symbol}"

COLOR_EMPTY = Color('Vacío', ' ')
COLORS = {
    'W': Color('Blanco', 'W'),
    'R': Color('Rojo', 'R'),
    'Y': Color('Amarillo', 'Y'),
    'G': Color('Verde', 'G'),
    'M': Color('Magenta', 'M'),
    'C': Color('Cyan', 'C')
}