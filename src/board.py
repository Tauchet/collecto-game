from math import floor
from colors import COLOR_EMPTY, COLORS, Color

import random as rnd

FAST_NEIGHBOURS = (
    (0, -1),
    (-1, 0)
)

NEIGHBOURS = (
    (0, -1),
    (-1, 0),
    (0, 1),
    (1, 0)
)

class Board():

    def __init__(self, size = 7):
        self.handle = []
        self.size = size
        self.middle_pos = floor(size / 2)
        for _ in range(0, size):
            self.handle.append([COLOR_EMPTY] * 7)
        pass

    def get_color(self, x: int, y: int) -> Color:
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return None
        return self.handle[y][x]
    
    def set_color(self, x: int, y: int, color: Color):
        self.handle[y][x] = color

    def is_color(self, x: int, y: int, color: Color):
        return self.get_color(x, y) == color

    def is_neighbour_color(self, x, y, color, neighbours = FAST_NEIGHBOURS):
        for (nx, ny) in neighbours:
            pos_x = nx + x
            pos_y = ny + y
            if self.is_color(pos_x, pos_y, color):
                return True
        return False

    def get_secure_position(self, x, y, color):
        for rx in range(self.size):
            for ry in range(self.size):
                rcolor = self.get_color(rx, ry)
                if rcolor != '*' and rcolor != color:
                    if (not self.is_neighbour_color(x, y, rcolor, NEIGHBOURS)) and (not self.is_neighbour_color(rx, ry, color, NEIGHBOURS)):
                        return (rx, ry, rcolor)
        return (x, y, color)

    def print(self):
        for y in range(0, self.size):
            for x in range(0, self.size):
                print(self.handle[y][x], end = " ")
            print("")

    pass

def get_color_whitout_repeat(board: Board, colors, x: int, y: int):

    intents = len(colors) - 1
    color = colors.pop(0)
    bug_last_color = False

    while (bug_last_color := board.is_neighbour_color(x, y, color)) and intents > 0:
        intents -= 1
        colors.append(color)
        color = colors.pop(0)

    # No hay más opciones de colores y por lo tanto la posición
    # que seleccionó tiene un vecino con el mismo color
    if bug_last_color:
        (next_x, next_y, next_color) = board.get_secure_position(x, y, color)
        print("ERROR", f"({x}, {y})", color, "->", f"({next_x}, {next_y})", next_color)
        board.set_color(next_x, next_y, color)
        color = next_color

    return color

def random(size = 7):

    instance = Board(size)
    colors = ([] + list(COLORS.values())) * (size + 1)
    rnd.shuffle(colors);

    for x in range(size):
        for y in range(size):
            if x != instance.middle_pos or y != instance.middle_pos: 
                instance.set_color(x, y, get_color_whitout_repeat(instance, colors, x, y))
                continue 

    instance.print()

    return instance