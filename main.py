from cgitb import text
import tkinter as tk
from tkinter import messagebox
from turtle import color
from PIL import Image

import board
from board_points import check_points
from colors import COLORS
from gui import GameCell, GameCellState, GameMovement
from locations import DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP, DIRECTIONS
from player import Player
from utils import create_matrix, get_url_image

class GameMain():
    def __init__(self):

        

        self.current_player_index = -1
        self.players = [
            Player("Cristian"),
            Player("Bedoya")
        ]

        self.main_window = tk.Tk()
        self.main_window.title("Collecto")
        self.main_window.config(width=400, height=300, padx=20, pady=20,background='black')

        self.game_frame = tk.Frame(self.main_window, width=400, height=300, background="#804040")
        self.game_frame.grid(column=1, row=0)

        self.window_players = []
        row = 0
        for player in self.players:
            label = tk.Label(text=f'{player.name}: {player.total_points} (Bolas: {player.total_balls})', background="#804040", font=("Monospaced",18), fg="white", pady=10)
            label.grid(column=1, row=3 + row, sticky=tk.S+tk.N+tk.E+tk.W)
            row = row + 1
            self.window_players.append(label)

        self.gui_player_current = tk.Label(text=f'Jugador', pady=10, background="#804040", font=("Monospaced",18), fg="white")
        self.gui_player_current.grid(column=1, row=1, sticky=tk.S+tk.N+tk.E+tk.W)
        
        image_default = tk.PhotoImage(file = get_url_image('boton-flecha.png'))
        self.movements = tk.Frame(self.main_window, background="black", padx=20, pady=20)
        self.window_movements = (
            GameMovement(self.movements, 0, get_url_image('boton-arriba-activo.png'), image_default, 1, 1, self.move),
            GameMovement(self.movements, 1, get_url_image('boton-abajo-activo.png'), image_default, 2, 1, self.move),
            GameMovement(self.movements, 2, get_url_image('boton-izquierda-activo.png'), image_default, 2, 0, self.move),
            GameMovement(self.movements, 3, get_url_image('boton-derecha-activo.png'), image_default, 2, 2, self.move)
        )
        self.movements.grid(column=1, row=2)
        

        self.next_player()

    def next_player(self):

        self.current_player_index = self.current_player_index + 1
        if len(self.players) <= self.current_player_index:
            self.current_player_index = 0

        self.last_cell = None
        self.last_cell_directions = None
        self.update_movements()

        player = self.players[self.current_player_index]
        self.gui_player_current['text'] = f'Es el turno del jugador {player.name}'
        
        pass

    def move(self, direction):

        if self.last_cell == None:
            return

        selected_cube = self.last_cell_directions.get(direction)
        if selected_cube == None:
            return

        cube: board.BoardCube = selected_cube
        #print(cube)

        #self.table.print()
        self.table.move(cube)
        #messagebox.askokcancel(title = "Hola", message="Acepta")
        self.update_balls()

        #print("  ")
        #print("--------------------------------")
        #print("  ")
        #self.table.print()
        points = check_points(self.table)
        #messagebox.askokcancel(title = "Hola 2", message="Acepta 2")
        
        self.check_available_movements(update_render = False)
        self.update_balls()
        
        current_player = self.players[self.current_player_index]
        current_player.add_points(points)

        for i in range(0, len(self.players)):
            player = self.players[i]
            self.window_players[i]['text'] = f'{player.name}: {player.total_points} (Bolas: {player.total_balls})'

        if (self.check_stop()):
            winner = self.get_winner()
            if winner != None:
                messagebox.showinfo('Información', message=f'Ha ganado el jugador {winner.name}')
            else :
                messagebox.showinfo('Información', message=f'¡Ha ocurrido un empate!')
            exit()

        self.next_player()

        pass

    def get_winner(self):
        winners = []
        winner_points = 0
        for player in self.players:

            if player.total_points > winner_points:
                winners.clear()
                winner_points = player.total_points
                winners.append(player)
            elif player.total_points == winner_points:
                winners.append(player)

        if len(winners) == 1:
            return winners[0]

        return None


    def check_stop(self):
        return self.table.first_color_with_count(2) == None

    def load_assets(self):
        # Bases para cargar todas las imagenes del juego
        self.PIXEL_VIRTUAL = tk.PhotoImage(width=1, height=1)
        self.IMAGE_BALLS = {}
        for color in COLORS:
            self.IMAGE_BALLS[color] = Image.open(get_url_image(color.ball_image_url)).convert("RGBA")

    def get_color_image(self, color):
        return self.IMAGE_BALLS.get(color)

    def start_game(self):
        self.table = board.random()
        self.render_table = create_matrix(self.table.size)
        for x in range(0, self.table.size):
            for y in range(0, self.table.size):
                color = self.table.get_color(x, y)
                cell = self.render_table[y][x] = GameCell(self.game_frame, x, y, on_click = self.click_cell_game)
                cell.change_color(self.get_color_image(color))
                cell.update()
        self.check_available_movements()
        pass

    def check_available_movements(self, update_render = True):
        available = self.table.get_movements_available()
        for x in range(0, self.table.size):
            for y in range(0, self.table.size):
                cell = self.render_table[y][x]
                state = GameCellState.NORMAL

                if (x, y) in available:
                    state = GameCellState.AVAILABLE
                
                if cell.change_state(state) and update_render:
                    cell.update()
        pass

    def update_movements(self):
        for i in range(0, 4):
            if self.last_cell_directions != None and self.last_cell_directions.get(DIRECTIONS[i]) != None:
                self.window_movements[i].change_state(True)
            else:
                self.window_movements[i].change_state(False)

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

    def update_balls(self):
        for y in range(0, self.table.size):
            for x in range(0, self.table.size):
                cell = self.render_table[y][x]
                cell.change_color(self.get_color_image(self.table.get_color(x, y)))
                cell.update()

    def show(self):
        self.main_window.mainloop()


window = GameMain()
window.load_assets()
window.start_game()
window.show()
