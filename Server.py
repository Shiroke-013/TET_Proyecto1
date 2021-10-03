import socket
import select
import sys
import mysql.connector
#import pymysql
from  _thread import *


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
list_of_clients = []

db_name = sys.argv[6]

def main(argv):
    print("Empecé")
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if len(sys.argv) != 7:
        print('Correct usage: script, IP address, port number, host, user, password, DB Name')
        exit()
    else: 
        ip_address = argv[1]
        port = int(argv[2])
        host = argv[3]
        user = argv[4]
        psswd = argv[5]

    server.bind((ip_address, port))
    server.listen(100)

    #cur, connection = start_connection(host, user, psswd, db_name)
    aux = True
    while aux:

	    conn, addr = server.accept()

	    list_of_clients.append(conn)

	    print (addr[0] + " connected")

	    # creates a thread for every client
	    start_new_thread(client_thread,(conn, addr, host, user, psswd, db_name))	

    server.close()

def start_connection(host, user, psswd, db_name):
    #connection = pymysql.connect(host=host, user=user, password=psswd, database=db_name)
    connection = mysql.connector.connect(user=user, password=psswd, host=host, database=db_name)
    with connection:
        cur = connection.cursor()
        return cur, connection


def client_thread(conn, addr, host, user, psswd, db_name):
    #cur = start_connection(host, user, psswd, db_name) 
    connection = mysql.connector.connect(user=user, password=psswd, host=host, database=db_name)
    cur = connection.cursor()
    #sends message
    conn.send(b'Welcome to NASAs data storage')

    while True:
            message = conn.recv(2048).decode()
            print("Received: ", message)
            if message: 
                #Conection to DB and save records
                #Message structure I/key/value no spaces or S/key/num
                msg = message.split('/')
                print(msg)
                print("msg size: ", len(msg))
                if  len(msg) == 3:
                    print(msg)
                    if msg[0] == 'I':
                        print("insert")
                        #how to save a record in the DB
                        #print("Result of check table: ", check_table_exists(connection))
                        #if check_table_exists(connection):
                            #print("Table exists")
                        insert_data = "INSERT INTO nasa_data (dkey, value) VALUES ('{}','{}');".format(msg[1], msg[2])
                        print(insert_data)
                        cur.execute(str(insert_data))
                        connection.commit()
                        message_to_send = "<" + str(addr[0]) + "> " + 'address saved a record'
                        send_to_sender(message_to_send, conn)
                    elif msg[0] =='S':
                        print("Select")
                        #how to select records from the DB
                        if check_table_exists(connection):
                            print("S and table exist")
                            sel = "SELECT {} FROM {}  WHERE {};".format(msg[2], 'nasa_data', msg[1])
                            print(sel)
                            data = cur.execute(sel)
                            send_to_sender(data, conn)
                            for rec in data:
                                print (rec[0] + "," + rec[1])
                            
                            message_to_send = "<" + str(addr[0]) + "> " + 'address had read' + msg[2] + 'records'
                            send_to_sender(message_to_send, conn)
                        else:
                            print("Sending faile")
                            message_to_send = "<" + str(addr[0]) + "> " + 'table does not exist, failed to read'
                            send_to_sender(message_to_send, conn)
                    else: 
                        print("ELSE from I and S")
                        message_to_send = "<" + str(addr[0]) + "> " + 'pls be intelligent'
                        send_to_sender(message_to_send, conn)
            else:
                print("ELSE REMOVE CONNECTION")
                remove(conn)
                conn.close()
                #print("EXCEPT")
            #except:
                #continue

#sends to the sender that register have been saved
def send_to_sender(message, connection):
    for clients in list_of_clients:
        print(clients)
        if clients==connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

#remove client if desconected
def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

main(sys.argv)