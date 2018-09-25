import time
import socket
from thread import *

TCP_IP = '192.168.43.203'
TCP_PORT = 8900
BUFFER_SIZE = 8192
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connlist = []

class User:
	def __init__(self,conn,addr):
		self.connection = conn
		self.adres = addr
	def setUsername(self,un):
		self.username = un

def initServer():
	try:
		s.bind((TCP_IP,TCP_PORT))
	except socket.error as e:
		print(str(e))

	s.listen(5)
	print("Ready")


def clientThread(chatUser):
	print( chatUser.adres[0], "Connected!" )
	usern = chatUser.connection.recv(BUFFER_SIZE)
	chatUser.setUsername(usern)
	print("Username", chatUser.username.rstrip())
	for x in connlist:
		x.connection.send("User " + chatUser.username.rstrip() + " entered the chatroom")
	SHEARED = -1
	while True:
		data = chatUser.connection.recv(BUFFER_SIZE)
		if not data:
			for x in connlist:
				if x.adres != chatUser.adres:
					x.connection.send("User " + chatUser.username.rstrip() + " disconnected")
			print("[" + chatUser.adres[0] + "] " + chatUser.username.rstrip() + " Disconnected")
			connlist.remove(chatUser)
			chatUser.connection.close()
			break
		print( chatUser.adres[0] + '~' + chatUser.username.rstrip() + ":", data.rstrip() )
		for x in connlist:
			if x.adres != chatUser.adres:
				x.connection.send( chatUser.adres[0] + '~' + time.strftime("%H:%M:%S") + "~" + chatUser.username.rstrip() + ": " + data.rstrip())


initServer()
while True:
	conn, addr = s.accept()
	newUser = User(conn,addr)
	connlist.append(newUser)
	start_new_thread(clientThread,(newUser,))
