import socket
import threading
from string import printable
from curses import erasechar, wrapper

HOST = raw_input("Entern host IP:\n")
PORT = int( raw_input("Enter port:\n") )
USERNAME = raw_input("Enter username:\n")
BUFFER_SIZE = 8192

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.send(USERNAME)

PRINTABLE = map(ord, printable)

def input(stdscr):
    ERASE = input.ERASE = getattr(input, "ERASE", ord(erasechar()))
    Y, X = stdscr.getyx()
    s = []

    while True:
        c = stdscr.getch()

        if c in (13, 10):
            break
        elif c == ERASE:
            y, x = stdscr.getyx()
            if x > X:
                del s[-1]
                stdscr.move(y, (x - 1))
                stdscr.clrtoeol()
                stdscr.refresh()
        elif c in PRINTABLE:
            s.append(chr(c))
            stdscr.addch(c)

    return "".join(s)

def prompt(stdscr, y, x, prompt=">>> "):
    stdscr.move(y, x)
    stdscr.clrtoeol()
    stdscr.addstr(y, x, prompt)
    return input(stdscr)

def main(stdscr):
    lines = []
    Y, X = stdscr.getmaxyx()
    max_lines = (Y - 3)
    stdscr.clear()

    while True:
        s = prompt(stdscr, (Y - 1), 0)  # noqa
        if s == ":q":
            break
        else:
            sock.send(str(s))

        # scroll
        if len(lines) > max_lines:
            lines = lines[1:]
            stdscr.clear()
            for i, line in enumerate(lines):
                stdscr.addstr(i, 0, line)

        stdscr.addstr(len(lines), 0, "You: " + s)
        lines.append("You: " + s)

        stdscr.refresh()

wrapper(main)

'''
def recive():
    data = s.recv(BUFFER_SIZE)
    print( data )

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(USERNAME)

t = threading.Thread( target=recive )
t.start()

running = True
while running:
    msg = raw_input("");
    s.send(msg)
'''
#python Documents/PythonServer/client.py
