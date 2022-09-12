from math import floor
from colors import COLOR_EMPTY, COLORS, Color

import random as rnd

FAST_NEIGHBOURS = (
    (0, -1),
    (-1, 0)
)

NEIGHBOURS = (
    (0, -1), # Arriba
    (0, 1), # Abajo
    (1, 0), # Derecha
    (-1, 0), # Izquierda
)

class Board():

    def __init__(self, size = 7):
        self.handle = []
        self.size = size
        self.middle_pos = floor(size / 2)
        for _ in range(0, size):
            self.handle.append([COLOR_EMPTY] * 7)
        pass

    def check_bounds(self, x: int, y: int):
        return x >= 0 and x < self.size and y >= 0 and y < self.size

    def get_color(self, x: int, y: int) -> Color:
        if self.check_bounds(x, y):
            return self.handle[y][x]
        return None
    
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

    def get_first_empty(self, x_min: int, x_max: int, y_min: int, y_max: int):
        position = None

        for xf in range(x_min, x_max + 1):
            for yf in range(y_min, y_max + 1):
                if self.get_color(xf, yf) == COLOR_EMPTY:
                    position = (xf, yf)
                elif position:
                    return position

        return position

    def move(self, x_min: int, x_max: int, y_min: int, y_max: int):
        order = []

        for xf in range(x_min, x_max + 1):
            for yf in range(y_min, y_max + 1):
                color = self.get_color(xf, yf)
                if color == COLOR_EMPTY:
                    order.insert(0, color)
                else:
                    order.append(color)

        for xf in range(x_min, x_max + 1):
            for yf in range(y_min, y_max + 1):
                self.set_color(xf, yf, order.pop(0))

    def calculate_directions_available(self, x: int, y: int):
        directions = []
        for direction in NEIGHBOURS:
            (dx, dy) = direction
            pos_x = dx + x
            pos_y = dy + y

            # Validar que sea una esquina o que tenga un espacio para mover con el dedo. 
            if (not self.check_bounds(pos_x, pos_y)) or self.get_color(pos_x, pos_y) == COLOR_EMPTY:
                (dcx, dcy) = get_direction_contrary(direction)
                
                temp_x = x + (dcx * (self.size - 1))
                temp_y = y + (dcy * (self.size - 1))

                x_min = min(x, temp_x)
                x_max = max(x, temp_x)
                y_min = min(y, temp_y)
                y_max = max(y, temp_y)

                first_empty = self.get_first_empty(x_min, x_max, y_min, y_max)
                if first_empty != None:
                    directions.append((direction, first_empty))
        
        return directions

    def print(self):
        print("---------------------------------")
        for y in range(0, self.size):
            for x in range(0, self.size):
                print(self.handle[y][x], end = " ")
            print("")

    pass

def get_direction_contrary(direction):
    (x, y) = direction
    return (x * -1, y * -1)

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
        print("FORMULANDO", f"({x}, {y})", color, "->", f"({next_x}, {next_y})", next_color)
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

    return instance