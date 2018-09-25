import socket
import os
import threading
from curses import *

HOST = "192.168.43.203"#input("Enter host IP:\n")
PORT = 8900 #int( input("Enter port:\n") )
USERNAME = "reciver"
BUFFER_SIZE = 8192
MAX_COLOR = 0
DO_PROGRAM = True
ipToColor = {}
screenX = 0
screenY = 0
userDate = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.send(USERNAME.encode('ascii'))

def promptInput(stdscr):
	ERASE = 263
	s = []

	while True:
		c = stdscr.getch()
		if c in (13, 10):
			break
		elif c == ERASE:
			y, x = stdscr.getyx()
			del s[-1]
			stdscr.move(y, (x - 1))
			stdscr.clrtoeol()
			stdscr.refresh()
		else:
			s.append(chr(c))
			stdscr.addch(c)
	return "".join(s)

def getMessage(stdscr):
	stdscr.move(stdscr.getmaxyx()[0]-1, 0)
	stdscr.clrtoeol()
	stdscr.addstr(stdscr.getmaxyx()[0]-1, 0, ">>> ")
	return promptInput(stdscr)


# def initColors(stdscr):
# 	init_pair(1, stdscr.COLOR_RED, stdscr.COLOR_BLACK)
# 	init_pair(2, stdscr.COLOR_GREEN, stdscr.COLOR_BLACK)
# 	init_pair(3, stdscr.COLOR_YELLOW, stdscr.COLOR_BLACK)
# 	init_pair(4, stdscr.COLOR_BLUE, stdscr.COLOR_BLACK)
# 	init_pair(5, stdscr.COLOR_MAGENTA, stdscr.COLOR_BLACK)
# 	init_pair(6, stdscr.COLOR_CYAN, stdscr.COLOR_BLACK)
# 	init_pair(7, stdscr.COLOR_WHITE, stdscr.COLOR_BLACK)

def specialInput(command):
	if(command == ':q'):
		DO_PROGRAM = False

def main(stdscr):
	screenY, screenX = stdscr.getmaxyx()
	lines = []
	start_color()
	# initColors(stdscr)
	stdscr.clear()
	MAX_COLOR = 0
	def recieveData():
		while True:
			data = sock.recv(BUFFER_SIZE)
			dataEncoded = data.decode("ascii")
			if(dataEncoded.split("~")[0] not in ipToColor):
				ipToColor[dataEncoded.split("~")[0]] = 1
				# MAX_COLOR+=1
			userColor = ipToColor[dataEncoded.split("~")[0]]
			if (len(dataEncoded.split("~"))>1):
				userDate.append('[' + dataEncoded.split("~")[1] + ']')
				lines.append(' '+ dataEncoded[2] + ': ' + '~'.join(dataEncoded.split("~")[3:]))
				stdscr.addstr(len(lines), 0, userDate[len(userDate)-1], color_pair(0))
				stdscr.addstr(lines[len(lines)-1], color_pair(0))
			stdscr.move( screenY - 1, 4 )
			stdscr.refresh()

	t = threading.Thread(target = recieveData )
	t.start()
	while(DO_PROGRAM):
		toSend = getMessage(stdscr)
		if(toSend):
			if(toSend[0] != ':'):
				sock.send(toSend.encode("ascii"))
			else:
				specialInput(toSend)
		if len(lines) > screenY-3:
			lines = lines[1:]
			stdscr.clear()
			for i, line in enumerate(lines):
				stdscr.addstr(i, 0, line)
			stdscr.refresh()

wrapper(main)



# if(__name__ == '__main__'):
# 	main()
