class Direction():

    def __init__(self, uid, name, mov_x, mov_y):
        self.uid = uid
        self.name = name
        self.mov_x = mov_x
        self.mov_y = mov_y

    def get_contrary(self):
        return CONTRARY_DIRECTIONS[self.uid]
    
    def __repr__(self) -> str:
        return f"Direction[{self.name}, {self.mov_x}, {self.mov_y}]"

class Cube():

    def __init__(self, ax, ay, bx, by):
        self.x_min = min(ax, bx)
        self.y_min = min(ay, by)
        self.x_max = max(ax, bx)
        self.y_max = max(ay, by)

    def __repr__(self) -> str:
        return f"Cube[{self.x_min},{self.y_min},{self.x_max},{self.y_max}]"

DIRECTION_UP = Direction(0, 'UP', 0, -1)
DIRECTION_DOWN = Direction(1, 'DOWN', 0, 1)
DIRECTION_LEFT = Direction(2, 'LEFT', -1, 0)
DIRECTION_RIGHT = Direction(3, 'RIGHT', 1, 0)
DIRECTIONS = (DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT)
CONTRARY_DIRECTIONS = (DIRECTION_DOWN, DIRECTION_UP, DIRECTION_RIGHT, DIRECTION_LEFT)

NEIGHBOURS = DIRECTIONS
FAST_NEIGHBOURS = (DIRECTION_UP, DIRECTION_LEFT)

def get_cube_from(a, b):
    return Cube(a[0], a[1], b[0], b[1])