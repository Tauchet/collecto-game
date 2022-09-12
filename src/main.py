import board
from colors import COLOR_EMPTY

current_board: board.Board = board.random()
current_board.set_color(3, 4, COLOR_EMPTY)
current_board.print()

(pos_x, pos_y) = (3, 0)
(direction, movement) = current_board.calculate_directions_available(pos_x, pos_y)[0]
current_board.move(pos_x, movement[0], pos_y, movement[1])
current_board.print()