import time, sys, msvcrt
from getkey import getkey, keys

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
   
def get_input():
    chars = []
    final_char = -1
    if msvcrt.kbhit():
        while msvcrt.kbhit():
            chars.append(ord(msvcrt.getch()))
        final_char = chars[len(chars)-1]
    return final_char

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
        inp = get_input()
        vel = input_handler(inp)
        if inp != -1:
            console.move_cursor(vel[0], vel[1])
        else:
            time.sleep(0.2)
        last_inp = inp
main()