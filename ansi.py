import time, sys
from pynput import keyboard

chars = []

def on_press(key):
    if chars.count(key) == 0:
        chars.append(key)

def on_release(key):
    if chars.count(key) != 0:
        chars.remove(key)


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

class Console:
    def __init__(self):
        self.clearscr = "\u001b[2J"
        self.home = "\u001b[1000A\u001b[1000D"
        self.clear()
        self.curs_pos = [0,0]

    def write(self, text):
        sys.stdout.write(text)
        sys.stdout.flush()

    def clear(self):
        self.write(self.clearscr + self.home)

    def move_cursor(self, x = 0,y = 0):
        new_pos = [self.curs_pos[0] + x, self.curs_pos[1]+y]
        self.write(f"\u001b[{new_pos[1]};{new_pos[0]}H")
        self.curs_pos = new_pos

    def cursor_pos(self, x = 0,y = 0):
        self.write(f"\u001b[{y};{x}H")
   


def input_handler(inp):
    vel = [0,0]
    match inp:
        case 72: #up press
            vel[1] = -1
        case 80: #down pressed
            vel[1]= 1
        case 75: #left pressed
            vel[0] = -1
        case 77: #right pressed
            vel[0] = 1
    return vel

def main():
    console = Console()
    console.clear()
    last_inp = None
    while 2+2==4:
        print(chars)


main()