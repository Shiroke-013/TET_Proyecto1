import socket
import select
import sys
from  _thread import *

#idk
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = "0.0.0.0"

Port = 3550

server.bind((IP_address, Port))

server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
        #sends message
	conn.send(b'You are part of this group chat!')

	while True:
            try:
                message = conn.recv(2048).decode()

                if message:
                    print("este es addr[0]" + str(addr[0]))
                    print("<" + str(addr[0]) + "> " + message)
                    
                    message_to_send = "<" + str(addr[0]) + "> " + message
                    sendToClients(message_to_send, conn)
                else:
                    remove(conn)
            except:
                continue

#sends to all clients
def sendToClients(message, connection):
    for clients in list_of_clients:
        print(clients)
        if clients!=connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

#remove client if desconected
def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	conn, addr = server.accept()

	list_of_clients.append(conn)

	print (addr[0] + " connected")

	# creates a thread for every client
	start_new_thread(clientthread,(conn,addr))	

conn.close()
server.close()
