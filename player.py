from math import floor

# Clase para el control de los datos de un jugador
class Player():

    def __init__(self, name):
        self.name = name
        self.total_balls = 0
        self.points = {}
        self.total_points = 0

    # Función para agregar y actualziar los puntos totales obtenidos por
    # los colores agrupados encontrados en el tablero
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
        
