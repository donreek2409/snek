import time, sys, os
from pynput import keyboard

#initiating Listener (outside of an object...grrr!)
chars = []

def on_press(key):
    if chars.count(str(key)) == 0:
        chars.append(str(key))

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

    def move_cursor(self, x = 0,y = 0):
        new_pos = [self.curs_pos[0] + x, self.curs_pos[1]+y]
        self.write(f"\u001b[{new_pos[1]};{new_pos[0]}H")
        self.curs_pos = new_pos

    def cursor_pos(self, x = 0,y = 0):
        self.write(f"\u001b[{y};{x}H")

class GameWindow:
    def __init__(self, console):
        self.term_size = os.get_terminal_size()
        self.console = console

    def create_border(self, size = [19,19]):
        for i in range(size[0]+1):
            self.console.write(" ", True, [i, 0], True, 'white_back')
            self.console.write(" ", True, [i, size[1]], True, 'white_back')
        for i in range(size[1]):
            self.console.write(" ", True, [0, i], True, 'white_back')
            self.console.write(" ", True, [size[0], i], True, 'white_back')
    def get_term_size(self):
        self.term_size = os.get_terminal_size()
        return self.term_size

def input_handler():
    vel = [0,0]
    if chars.count("Key.up"):
        vel[1] -= 1
    if chars.count("Key.down"):
        vel[1] += 1
    if chars.count("Key.left"):
        vel[0] -= 1
    if chars.count("Key.right"):
        vel[0] += 1
    return vel

def main():
    console = Console()
    console.clear()
    console.write(console.hide_curs)
    window = GameWindow(console)
    window.create_border([100,40])
    #game loop
    while 2+2==4:
        #while button not pressed
        while len(chars) == 0:
            time.sleep(0.01)
        #while button pressed
        while len(chars) != 0:
            vel = input_handler()
            time.sleep(0.1)



main()