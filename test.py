import board
from board_points import check_points
from colors import COLOR_BLUE, COLOR_EMPTY, COLOR_GREEN, COLOR_MAGENTA, COLOR_RED, COLOR_WHITE, COLOR_YELLOW
from locations import DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_UP, Cube, Direction

#Declaraciones

E = COLOR_EMPTY

M = COLOR_MAGENTA
G = COLOR_GREEN
R = COLOR_RED
Y = COLOR_YELLOW
B = COLOR_BLUE
W = COLOR_WHITE

matriz = [
    [R, G, W, E, B, E, E],
    [E, M, R, E, E, E, E],
    [E, W, G, E, R, E, E],
    [B, E, E, E, E, E, E],
    [E, E, E, E, E, R, W],
    [E, E, E, B, E, E, E],
    [E, E, E, Y, E, Y, B]
]

table = board.random(7)
table.handle = matriz
table.print()

print("----------------------------")
print(table.calculate_directions_available(6, 6))
print("----------------------------")

table.move(table.calculate_directions_available(6, 6)[DIRECTION_LEFT])


table.print()

#print(check_points(table))

#table.print()