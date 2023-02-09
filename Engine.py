import time
import sys
from pynput import keyboard
class Engine:

    def __init__(self, grid_size = (100, 50)):

        self.inputs = self.Input()
        self.console = self.Console()
        self.console.write(self.console.hide_curs)
        self.grid = self.Grid(grid_size, self.console)

    class Input:

        def __init__(self):
            self.start_listen()
            self.held_chars = []
            self.press_func = 0
            self.release_func = 0

        def set_input(self, press_func = 0, release_func = 0):
            self.press_func = press_func
            self.release_func = release_func

        def start_listen(self):
            def on_press(key):
                if self.held_chars.count(str(key)) == 0:
                    self.held_chars.append(str(key))
                if self.press_func == 0:
                    pass
                else:
                    self.press_func(str(key))

            def on_release(key):
                if str(key) in self.held_chars:
                    self.held_chars.remove(str(key))
                if self.release_func == 0:
                    pass
                else:
                    self.release_func(str(key))

            listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            listener.start()

    class Console:
        def __init__(self):
            self.clearscr = "\u001b[2J"
            self.home = "\u001b[1000A\u001b[1000D"
            self.curs_pos = [0,0]
            self.clear()
            self.hide_curs = '\u001b[?25l'
            self.show_curs = '\u001b[?25h'
            #Color
            #backgrounds
            self.col_back_white = "\u001b[47m"
            self.col_back_black = "\u001b[40m"

        def write(self, text, move = False, loc = [0,0], col = False, front_col = '', back_col = ''):
            color_code = ''
            reset_color_code = ''
            if move:
                self.cursor_pos(loc[0], loc[1])
            if col:
                color_code = self.color(front_col, back_col)
                reset_color_code = self.color('reset', 'reset')

            sys.stdout.write(color_code+text+reset_color_code)
            sys.stdout.flush()
            self.curs_pos[0] = self.curs_pos[0] + len(text)
            
        def clear(self):
            self.write(self.clearscr + self.home)

        def delete(self, tile:list):
            self.write(" ", True, tile)
            self.curs_pos = [self.curs_pos[0] - 1,self.curs_pos[1]]

        def move_cursor(self, x = 0,y = 0):
            new_pos = [self.curs_pos[0] + x, self.curs_pos[1]+y]
            self.write(f"\u001b[{new_pos[1]};{new_pos[0]}H")
            self.curs_pos = new_pos

        def cursor_pos(self, x = 0,y = 0):
            self.write(f"\u001b[{y};{x}H")
            self.curs_pos = [x,y]
        
        def color(self, front, back):
            new_color = ""

            front_black =  "\u001b[30m"
            front_red =  "\u001b[31m"
            front_green =  "\u001b[32m"
            front_yellow = "\u001b[33m"
            front_blue =  "\u001b[34m"
            front_magenta =  "\u001b[35m"
            front_cyan =  "\u001b[36m"
            front_white = "\u001b[37m"
            front_reset =  "\u001b[0m"

            match front:
                case "black":
                    new_color = front_black
                case "red":
                    new_color = front_red
                case "green":
                    new_color = front_green
                case "yellow":
                    new_color = front_yellow
                case "blue":
                    new_color = front_blue
                case "magenta":
                    new_color = front_magenta
                case "cyan":
                    new_color = front_cyan
                case "white":
                    new_color = front_white
                case "reset":
                    new_color = front_reset

            back_black = "\u001b[40m"
            back_red = "\u001b[41m"
            back_green = "\u001b[42m"
            back_yellow =  "\u001b[43m"
            back_blue =  "\u001b[44m"
            back_magenta =  "\u001b[45m"
            back_cyan =  "\u001b[46m"
            back_white = "\u001b[47m"
            back_reset =  "\u001b[0m"

            match back:
                case "black":
                    new_color = new_color + back_black
                case "red":
                    new_color = new_color + back_red
                case "green":
                    new_color = new_color + back_green
                case "yellow":
                    new_color = new_color + back_yellow
                case "blue":
                    new_color = new_color + back_blue
                case "magenta":
                    new_color = new_color + back_magenta
                case "cyan":
                    new_color = new_color + back_cyan
                case "white":
                    new_color = new_color + back_white
                case "reset":
                    new_color = new_color + back_reset
            
            return new_color

    class Object:
        def __init__(self, name:str, content:str, color_front='white', color_back='black'):
            self.name = name
            self.content = content
            self.color_front = color_front
            self.color_back = color_back
            self.location = []

    class Grid:
        class Tile:
            def __init__(self, location:tuple):
                self.location = location
                self.object = None
                

            def add_obj(self, obj):
                self.object = obj
                self.object.location = self.location

            def remove_obj(self):
                self.object = None
        
        def __init__(self, size:tuple, console):
            self.grid = self.create_grid(size)
            self.console = console

        def draw_grid(self):
            for x in range(0, len(self.grid)-1):
                for y in range(0, len(self.grid[x])-1):
                    if self.grid[x][y].object != None:
                        self.console.write(self.grid[x][y].object.content, True, [x,y])

        def create_grid(self, size:tuple):
            grid = []
            for i in range(size[0] - 1):
                grid.append([])
                for j in range(size[1] - 1):
                    grid[i].append(self.Tile((i,j)))
            return grid


