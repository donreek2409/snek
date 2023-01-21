import time, sys, os
from pynput import keyboard

#initiating Listener (outside of an object...grrr!)
chars = []
term_size = os.get_terminal_size()

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

    def write(self, text, move = False, loc = [0,0]):
        if move:
            self.cursor_pos(loc[0], loc[1])
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
    while 2+2==4:
        while len(chars) == 0:
            time.sleep(0.01)
        while len(chars) != 0:
            vel = input_handler()
            time.sleep(0.1)



main()