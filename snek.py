import time, sys, os
from pynput import keyboard

#initiating Listener (outside of an object...grrr!)
chars = []
step_time = 0.2
skip_time = 0.05
velocity = [1,0]

def on_press(key):
    if chars.count(str(key)) == 0:
        chars.append(str(key))
    global velocity
    if str(key) == ("Key.up") and velocity != [0,1]:
        velocity = [0,-1]
    if str(key) ==("Key.down") and velocity != [0, -1]:
        velocity = [0,1]
    if str(key) ==("Key.left") and velocity != [1,0]:
        velocity = [-1,0]
    if str(key) ==("Key.right") and velocity != [-1, 0]:
        velocity = [1,0]

def on_release(key):
    if chars.count(str(key)) != 0:
        chars.remove(str(key))

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

class Console:
    def __init__(self):
        self.clearscr = "\u001b[2J"
        self.home = "\u001b[1000A\u001b[1000D"
        self.clear()
        self.curs_pos = [0,0]
        self.hide_curs = '\u001b[?25l'
        self.show_curs = '\u001b[?25h'
        #Color
        #backgrounds
        self.col_back_white = "\u001b[47m"
        self.col_back_black = "\u001b[40m"

    def write(self, text, move = False, loc = [0,0], col = False, text_color = ''):
        color_code = ''
        reset_color_code = ''
        if move:
            self.cursor_pos(loc[0], loc[1])
        if col:
            if text_color == 'white_back':
                color_code = self.col_back_white
                reset_color_code = self.col_back_black

        sys.stdout.write(color_code+text+reset_color_code)
        sys.stdout.flush()

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

class GameWindow:
    def __init__(self, console, size:list):
        self.size = size
        self.term_size = [os.get_terminal_size().columns, os.get_terminal_size().lines]
        self.console = console
        self.walls = []
        if size[0] > self.term_size[0] or size[1] > self.term_size[1]:
            self.too_small()
        self.build_wall_list()
        self.create_border(self.size)
    def create_border(self, size = [19,19]):
        for i in range(size[0]+1):
            #save wall tile
            self.walls[i - 1][0] = "wall"
            self.walls[i - 1][size[1]-1] = "wall"
            #paint the walls
            self.console.write(" ", True, [i, 0], True, 'white_back')
            self.console.write(" ", True, [i, size[1]], True, 'white_back')
        for i in range(size[1]):
            #save wall tile
            self.walls[size[0]-1][i-1] = "wall"
            self.walls[0][i-1] = "wall"
            #paint the walls
            self.console.write(" ", True, [0, i], True, 'white_back')
            self.console.write(" ", True, [size[0], i], True, 'white_back')
    def get_term_size(self):
        self.term_size = os.get_terminal_size()
        return self.term_size
    def build_wall_list(self):
        for i in range(0,self.size[0]):
            self.walls.append([])
            for j in range(0,self.size[1]):
                self.walls[i].append([])
    def too_small(self):
        self.console.clear()
        self.console.write("Console not large enough for application. Please resize your console window and relaunch.\nQuitting now...")
        quit()
    def quit_game(self):
        self.console.clear()
        quit()

class Debug:
    def __init__(self, console, window):
        self.console = console
        self.window = window
        self.write_loc = [window.size[0], window.size[1]]
    def write(self, text):
        self.console.cursor_pos(self.write_loc[0] + 3, 0)
        sys.stdout.write(text)
        sys.stdout.flush()

class Snek:
    def __init__(self, starting_segs:int, start_pos:list, console:Console, debug:Debug, window:GameWindow):
        self.segs = [start_pos]
        self.snek_len = starting_segs
        self.console = console
        self.debug = debug
        self.window = window

    def move_snek(self, vel):
        new_pos = [self.segs[0][0]+vel[0], self.segs[0][1]+vel[1]]
        self.console.cursor_pos(new_pos[0], new_pos[1])
        self.console.write("\u001b[42m \u001b[0m")
        if len(self.segs) < self.snek_len:
            self.segs.append([0,0])
        else:
            self.console.delete(self.segs[len(self.segs) - 1])
        for seg in range(len(self.segs)-1, -1, -1):
            if seg > 0:
                self.segs[seg] = self.segs[seg-1]
            else:
                self.segs[0] = new_pos
                break
        #check for wall collision
        if self.window.walls[self.segs[0][0]][self.segs[0][1]] == "wall":
            self.window.quit_game()

def main():
    console = Console()
    console.clear()
    console.write(console.hide_curs)
    window = GameWindow(console, [100,40])
    debug = Debug(console, window)
    mid_win = [round(window.size[0]/2), round(window.size[1]/2)]
    snek = Snek(3, mid_win, console, debug, window)
    snek.move_snek([1,0])
    t_time = step_time/0.001
    t = 0
    #game loop
    while 2+2==4:
        if chars.count("Key.up") > 0 or chars.count("Key.down") > 0 or chars.count("Key.left") > 0 or chars.count("Key.right"):
            t_time = skip_time/0.001
        else:
            t_time = step_time/0.001
        if t >= t_time:
            snek.move_snek(velocity)
            t = 0
        time.sleep(0.001)
        t += 1

main()