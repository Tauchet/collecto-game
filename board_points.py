from board import Board
from colors import COLOR_EMPTY

#Metodos
def down(board: Board, value, x, y, couple_position):
    if board.is_color(x, y + 1, value):
        couple_position.add((x, y, value))
        couple_position.add((x, y + 1,value))

def right(board: Board, value, x, y, couple_position):
    if board.is_color(x + 1, y, value):
        couple_position.add((x, y, value))
        couple_position.add((x + 1, y, value))

def check_points(board: Board):

    #Conjunto que almacena las parejas que coinciden
    couple_position = set()

    for x in range(0, board.size):
        for y in range(0, board.size):
            
            color = board.get_color(x, y)
            if color == COLOR_EMPTY:
                continue

            right(board, color, x, y, couple_position)
            down(board, color, x, y, couple_position)

    points = {}
    for position_game in couple_position:

        board.set_color(position_game[0], position_game[1], COLOR_EMPTY)
        print(position_game[0], position_game[1])

        if position_game[2] in points:
            points[position_game[2]] = points[position_game[2]] + 1
        else:
            points[position_game[2]] = 1

    return points