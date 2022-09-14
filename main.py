from cgitb import text
import tkinter as tk
from tkinter import messagebox
from PIL import Image

import board
from board_points import check_points
from colors import COLORS
from gui import GameCell, GameCellState, GameMovement
from locations import DIRECTIONS
from player import Player
from utils import create_matrix, get_url_image

class GameMain():
    def __init__(self):

        
        # Creamos los jugadores
        self.current_player_index = -1
        self.players = [
            Player("#1"),
            Player("#2")
        ]

        # Creamos la ventana inicial
        self.main_window = tk.Tk()
        self.main_window.title("Collecto")
        self.main_window.config(width=400, height=300, padx=20, pady=20,background='black')

        # Creamos donde se colocará el juego
        self.game_frame = tk.Frame(self.main_window, width=400, height=300, background="#804040")
        self.game_frame.grid(column=1, row=0)

        # Creamos los textos de puntajes
        self.window_players = []
        row = 0
        for player in self.players:
            label = tk.Label(text=f'Jugador {player.name}: {player.total_points} (Bolas: {player.total_balls})', background="#804040", font=("Monospaced",18), fg="white", pady=10)
            label.grid(column=1, row=3 + row, sticky=tk.S+tk.N+tk.E+tk.W)
            row = row + 1
            self.window_players.append(label)

        self.gui_player_current = tk.Label(text=f'Jugador', pady=10, background="#804040", font=("Monospaced",18), fg="white")
        self.gui_player_current.grid(column=1, row=1, sticky=tk.S+tk.N+tk.E+tk.W)
        
        # Creamos el sistema de movimientos
        image_default = tk.PhotoImage(file = get_url_image('boton-flecha.png'))
        self.movements = tk.Frame(self.main_window, background="black", padx=20, pady=20)
        self.window_movements = (
            GameMovement(self.movements, 0, get_url_image('boton-arriba-activo.png'), image_default, 1, 1, self.move),
            GameMovement(self.movements, 1, get_url_image('boton-abajo-activo.png'), image_default, 2, 1, self.move),
            GameMovement(self.movements, 2, get_url_image('boton-izquierda-activo.png'), image_default, 2, 0, self.move),
            GameMovement(self.movements, 3, get_url_image('boton-derecha-activo.png'), image_default, 2, 2, self.move)
        )
        self.movements.grid(column=1, row=2)
        
        # Ejecutamos el primer jugador
        self.next_player()

    def next_player(self):

        # Sumamos para encontrar el siguiente jugador
        self.current_player_index = self.current_player_index + 1
        if len(self.players) <= self.current_player_index:
            self.current_player_index = 0

        # Reiniciamos los datos
        self.last_cell = None
        self.last_cell_directions = None
        self.update_movements()

        # Actualizamos el mensaje para conocer quién es el jugador actual
        player = self.players[self.current_player_index]
        self.gui_player_current['text'] = f'Es el turno del jugador {player.name}'
        
        pass

    # Función para la ejecución del movimiento dado por el botón de la interfaz
    def move(self, direction):

        if self.last_cell == None:
            return

        selected_cube = self.last_cell_directions.get(direction)
        if selected_cube == None:
            return

        cube: board.BoardCube = selected_cube

        # Ejecutamos el movimiento
        self.table.move(cube)

        # Encontramos las parejas de colores
        points = check_points(self.table)
        
        # Actualizamos los movimientos disponibles
        self.check_available_movements(update_render = False)

        # Actualizamos el tablero de colores
        self.update_balls()
        
        # Agregamos & actualizamos el puntaje de los jugadores en pantalla
        current_player = self.players[self.current_player_index]
        current_player.add_points(points)
        for i in range(0, len(self.players)):
            player = self.players[i]
            self.window_players[i]['text'] = f'Jugador {player.name}: {player.total_points} (Bolas: {player.total_balls})'

        # Validamos que haya terminado el juego
        if (self.check_stop()):
            winner = self.get_winner()
            if winner != None:
                messagebox.showinfo('Información', message=f'Ha ganado el jugador {winner.name}')
            else :
                messagebox.showinfo('Información', message=f'¡Ha ocurrido un empate!')
            exit()

        # Damos el turno al siguiente jugador
        self.next_player()

        pass

    # Función para determina el ganador de la partida
    def get_winner(self):
        winners = []
        winner_points = 0

        # Recorremos a todos los jugadores
        for player in self.players:

            # Si el jugado rencontrado es mayor al puntaje actual quiere decir que debe limpiar y colocarlo como único ganador
            if player.total_points > winner_points:
                winners.clear()
                winner_points = player.total_points
                winners.append(player)

            # Si tienen el mismo puntaje se agrega a la lista como empate
            elif player.total_points == winner_points:
                winners.append(player)

        # Si la lista tiene un tamaño de 1, quiere decir que existe un ganador unanime
        if len(winners) == 1:
            return winners[0]

        # Probablemente exista un empate
        return None

    # Función para detectar si ya no existe un color con al menos 2 incidencias en el tablero
    def check_stop(self):
        return self.table.first_color_with_count(2) == None

    # Bases para cargar todas las imagenes del juego
    def load_assets(self):
        self.PIXEL_VIRTUAL = tk.PhotoImage(width=1, height=1)
        self.IMAGE_BALLS = {}
        for color in COLORS:
            self.IMAGE_BALLS[color] = Image.open(get_url_image(color.ball_image_url)).convert("RGBA")

    # Obtener la imagen de un color
    def get_color_image(self, color):
        return self.IMAGE_BALLS.get(color)

    # Iniciar un juego
    def start_game(self):

        # Generamos el tablero aleatorio
        self.table = board.random()

        # Creamos la representación matricial del tablero pero en el renderizado
        self.render_table = create_matrix(self.table.size)
        for x in range(0, self.table.size):
            for y in range(0, self.table.size):
                color = self.table.get_color(x, y)
                cell = self.render_table[y][x] = GameCell(self.game_frame, x, y, on_click = self.click_cell_game)
                cell.change_color(self.get_color_image(color))
                cell.update()

        # Actualizamos las celdas que son posibles tener un movimiento
        self.check_available_movements()

        pass

    # Actualizamos el estado del tablero de renderización según si tienen movimientos o no
    def check_available_movements(self, update_render = True):

        # Obtenemols todos las posiciones que tienen un movimiento
        available = self.table.get_movements_available()

        for x in range(0, self.table.size):
            for y in range(0, self.table.size):
                cell = self.render_table[y][x]

                # Obtenemos el estado actual del movimiento
                state = GameCellState.NORMAL
                if (x, y) in available:
                    state = GameCellState.AVAILABLE
                
                # Actualizamos la celda y actualizamos el renderizado
                if cell.change_state(state) and update_render:
                    cell.update()
        pass

    # Función para actualziar el estado de los botones de movimiento
    def update_movements(self):
        for i in range(0, 4):
            if self.last_cell_directions != None and self.last_cell_directions.get(DIRECTIONS[i]) != None:
                self.window_movements[i].change_state(True)
            else:
                self.window_movements[i].change_state(False)

    # Función para seleccionar una celda con posibles movimientos
    def click_cell_game(self, cell: GameCell):
        
        if self.last_cell != None and self.last_cell != cell:
            self.last_cell.change_state(GameCellState.AVAILABLE)
            self.last_cell.update()

        self.last_cell = cell;
        self.last_cell_directions = self.table.calculate_directions_available(cell.x, cell.y)
        self.last_cell.change_state(GameCellState.SELECTED)
        self.last_cell.update()
        self.update_movements()
        
        pass

    # Actualizamos el color de todas las celdas
    def update_balls(self):
        for y in range(0, self.table.size):
            for x in range(0, self.table.size):
                cell = self.render_table[y][x]
                cell.change_color(self.get_color_image(self.table.get_color(x, y)))
                cell.update()

    # Función para mostrar la aplicación
    def show(self):
        self.main_window.mainloop()


# Ejecución inicial
window = GameMain()
window.load_assets()
window.start_game()
window.show()
