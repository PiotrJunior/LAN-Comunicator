import socket
import threading
from string import printable
from curses import erasechar, wrapper, beep

HOST = raw_input("Entern host IP:\n")
PORT = int( raw_input("Enter port:\n") )
USERNAME = "reciver"
BUFFER_SIZE = 8192

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.send(USERNAME)

PRINTABLE = map(ord, printable)

def main(stdscr):
    lines = []
    Y, X = stdscr.getmaxyx()
    max_lines = (Y - 3)
    stdscr.clear()

    while True:
        data = sock.recv(BUFFER_SIZE)
        beep()
        if len(lines) > max_lines:
            lines = lines[1:]
            stdscr.clear()
            for i, line in enumerate(lines):
                stdscr.addstr(i, 0, line)

        stdscr.addstr(len(lines), 0, str(data))
        lines.append(str(data))

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
