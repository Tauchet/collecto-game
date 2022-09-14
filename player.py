from math import floor

class Player():

    def __init__(self, name):
        self.name = name
        self.total_balls = 0
        self.points = {}
        self.total_points = 0

    def add_points(self, points):
        
        for (color, p) in points.items():

            print(color, p)

            if color in self.points:
                self.points[color] = self.points[color] + p
            else:
                self.points[color] = p

            self.total_balls = self.total_balls + p


        total_points = 0
        for (color, p) in self.points.items():
            total_points = total_points + floor(self.points[color] / 3)
            
        self.total_points = total_points
        
