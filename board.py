from math import floor
from colors import COLOR_EMPTY, COLORS, Color

import random as rnd
from locations import FAST_NEIGHBOURS, NEIGHBOURS, Cube, Direction

from utils import create_matrix

class Board():

    def __init__(self, size = 7):
        self.handle = create_matrix(size, COLOR_EMPTY)
        self.size = size
        self.middle_pos = floor(size / 2)
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
        for direction in neighbours:
            pos_x = direction.mov_x + x
            pos_y = direction.mov_y + y
            if self.is_color(pos_x, pos_y, color):
                return True
        return False

    def get_secure_position(self, x, y, color):
        for rx in range(self.size):
            for ry in range(self.size):
                rcolor = self.get_color(rx, ry)
                if rcolor != COLOR_EMPTY and rcolor != color:
                    if (not self.is_neighbour_color(x, y, rcolor, NEIGHBOURS)) and (not self.is_neighbour_color(rx, ry, color, NEIGHBOURS)):
                        return (rx, ry, rcolor)
        return (x, y, color)

    def get_movements_available(self):
        available = []
        for x in range(0, self.size):
            for y in range(0, self.size):
                if (len(self.calculate_directions_available(x, y)) > 0):
                    available.append( (x, y) )
        return available

    def get_first_empty(self, x, y, direction: Direction):

        position = None
        pos_x = x
        pos_y = y

        while self.check_bounds(pos_x, pos_y):
            
            if self.get_color(pos_x, pos_y) == COLOR_EMPTY:
                position = (pos_x, pos_y)
                pass
            elif position != None:
                return position
            
            pos_x = pos_x + direction.mov_x
            pos_y = pos_y + direction.mov_y

        return position

    def calculate_directions_available(self, x: int, y: int):
        directions = {}

        if self.get_color(x, y) == COLOR_EMPTY:
            return directions 

        for direction in NEIGHBOURS:
            direction_contrary = get_direction_contrary(direction)

            con_x = direction_contrary.mov_x + x
            con_y = direction_contrary.mov_y + y

            # Validar que sea una esquina o que tenga un espacio para mover con el dedo. 
            if (not self.check_bounds(con_x, con_y)) or self.get_color(con_x, con_y) == COLOR_EMPTY:

                first_empty = self.get_first_empty(x, y, direction)
                if first_empty != None:
                    directions[direction] = Cube(x, y, first_empty[0], first_empty[1])
        
        return directions

    def move(self, cube: Cube):
        order = []
        updated = []

        first_iteration_executed = False
        inverse_empty = False
        emptys = []

        for xf in range(cube.x_min, cube.x_max + 1):
            for yf in range(cube.y_min, cube.y_max + 1):
                color = self.get_color(xf, yf)
                updated.append((xf, yf))

                # Se tiene que enviar los vacíos al final y no al inicio
                if color == COLOR_EMPTY and not first_iteration_executed:
                    inverse_empty = True

                if color == COLOR_EMPTY:
                    emptys.append(color)
                else:
                    order.append(color)

                first_iteration_executed = True

        print(order)

        if inverse_empty:
            order = order + emptys
        else:
            order = emptys + order

        for xf in range(cube.x_min, cube.x_max + 1):
            for yf in range(cube.y_min, cube.y_max + 1):
                self.set_color(xf, yf, order.pop(0))

        return updated

    def first_color_with_count(self, count):
        colors = {}
        for y in range(0, self.size):
            for x in range(0, self.size):
                color = self.get_color(x, y)
                if color != COLOR_EMPTY:
                    if (color in colors):
                        colors[color] = colors[color] + 1
                    else:
                        colors[color] = 1
                    if colors[color] >= count:
                        return color
        return None

    def print(self):
        for y in range(0, self.size):
            for x in range(0, self.size):
                print(self.handle[y][x], end = " ")
            print("")

    pass

def get_direction_contrary(direction: Direction):
    return direction.get_contrary()

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
    colors = list(COLORS) * (size + 1)
    rnd.shuffle(colors);

    for x in range(size):
        for y in range(size):
            if x != instance.middle_pos or y != instance.middle_pos: 
                instance.set_color(x, y, get_color_whitout_repeat(instance, colors, x, y))
                continue 

    return instance