from enum import Enum
import tkinter as tk
from xmlrpc.client import Boolean
from PIL import Image, ImageTk

from colors import Color
from locations import DIRECTIONS
from utils import get_url_image

class GameCellState(Enum):
    NORMAL = 0
    AVAILABLE = 1
    SELECTED = 2

class GameMovement():

    def __init__(self, parent, uid, image, default_image, row, column, on_click):
        self.uid = uid
        self.current_image = tk.PhotoImage(file = image)
        self.default_image = default_image
        self.handle = tk.Button(parent, image = self.current_image, bd = "0", background="black", cursor='cross')
        self.handle.image = self.current_image
        self.handle.grid(column=column, row=row)
        self.change_state(False)
        self.handler_click = on_click
        self.handle.bind('<Button>', self.click)
        pass

    def click(self, event):
        self.handler_click(DIRECTIONS[self.uid])

    def change_state(self, state: bool):
        self.state = state

        if state:
            self.handle['image'] = self.current_image
        else:
            self.handle['image'] = self.default_image


class GameCell():

    def __init__(self, main_window, x, y, on_click):
        self.state = GameCellState.NORMAL
        self.base_image = tk.PhotoImage(file=get_url_image('base.png'))
        self.main_window = main_window
        self.y = y
        self.x = x
        self.handler_on_click = on_click

    def change_state(self, state: GameCellState):
        old_state = self.state
        self.state = state
        return old_state != state

    def change_color(self, color: Color):
        self.color = color

    def update(self):

        img = get_url_image('base.png')
        cursor = 'arrow'
        if self.state == GameCellState.AVAILABLE:
            cursor = 'fleur'
            img = get_url_image('base_available.png')
        elif self.state == GameCellState.SELECTED:
            cursor = 'fleur'
            img = get_url_image('base_selected.png')

        bg = Image.open(img)
        if (self.color != None):
            final_bg = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
            final_bg.paste(bg, (0,0))
            final_bg.paste(self.color, (8, 8), mask=self.color)
            bg = final_bg

        photo = ImageTk.PhotoImage(bg)
        self.ball = tk.Button(self.main_window, image=photo, width=48, height=48, bd='0', cursor=cursor, bg='#804040')
        self.ball.image = photo
        self.ball.grid(row=self.y, column=self.x, padx=5, pady=5)

        # if self.color == None:
        #     self.ball = tk.Button(self.main_window, image=self.base_image, width=46, height=46, bd='0', cursor='cross', bg=background)
        #     self.ball.grid(row=self.y, column=self.x, padx=5, pady=5)
        # else:
        #     self.ball = tk.Button(self.main_window, image=self.base_image, width=46, height=46, bd='0', bg=background, cursor='fleur')
        #     self.ball.grid(row=self.y, column=self.x, padx=5, pady=5)
        #     self.ball2 = tk.Button(self.ball, image=self.color, width=46, height=46, bd='0', cursor='fleur')
        #     self.ball2.pack()
        
        self.ball.bind('<Enter>', self.on_focus_enter)
        self.ball.bind('<Leave>', self.on_focus_leave)
        self.ball.bind('<Button>', self.on_click)

    def on_click(self, event):

        if self.state != GameCellState.AVAILABLE:
            return

        self.handler_on_click(self)
        
        pass

    def on_focus_enter(self, event):
        #self.handler_on_focus_enter(self)
        pass
        #image2 = tk.PhotoImage(file="./images/yellow_ball.png")
        #self.handle.configure(image = image2)
        #self.handle.image = image2

    def on_focus_leave(self, event):
        #self.handler_on_focus_leave(self)
        pass
        #image2 = tk.PhotoImage(file="./images/red_ball.png")
        #self.handle.configure(image = image2)
        #self.handle.image = image2