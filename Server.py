import socket
import select
import sys
from  _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main(argv):
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ip_address = argv[1]
    port = argv[2]

    server.bind((ip_address, port))
    server.listen(100)


list_of_clients = []

def clientthread(conn, addr):
        #sends message
	conn.send(b'Welcome to NASAs data storage')

	while True:
            try:
                message = conn.recv(2048).decode()

                if message: 
                    #Conection to DB and save records
                    #Message structure I/key/value no spaces or R/key/num
                    msg = message.split('/')
                    if  msg.size() == 3:
                        if msg[0] == "I":
                            #how to save a record in the DB
                            message_to_send = "<" + str(addr[0]) + "> " + 'address saved a record'
                            send_to_clients(message_to_send, conn)
                        elif msg[0] =="R":
                            #how to read records from the DB
                            message_to_send = "<" + str(addr[0]) + "> " + 'address had read' + msg[2] + 'records'
                            send_to_clients(message_to_send, conn)
                    
                else:
                    remove(conn)
            except:
                continue

#sends to all cleints that register have been saved
def send_to_clients(message, connection):
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
