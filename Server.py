import socket
import select
import sys

from  _thread import *

#MySQL
import pymysql


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
list_of_clients = []

db_name = ""

def main(argv):
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if len(sys.argv) != 7:
        print('Correct usage: script, IP address, port number, host, user, password, DB Name')
        exit()
    else: 
        ip_address = argv[1]
        port = argv[2]
        host = argv[3]
        user = argv[4]
        psswd = argv[5]
        db_name = argv[6]

    server.bind((ip_address, port))
    server.listen(100)

    cur, connection = start_connection(host, user, psswd, db_name)

    aux = True
    while aux:

	    conn, addr = server.accept()

	    list_of_clients.append(conn)

	    print (addr[0] + " connected")

	    # creates a thread for every client
	    start_new_thread(client_thread,(conn,addr, cur, connection))	

    server.close()

def start_connection(host, user, psswd, db_name):
    connection = pymysql.connect(host,user, psswd, db_name)
    with connection:
        cur = connection.cursor()
        return cur, connection

def client_thread(conn, addr, cur, connection):
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
                            if check_table_exists(connection):
                                insert_data = """INSERT INTO database-1 (Key, Value) VALUES ({},{})""".format(msg[1], msg[2])
                                cur.execute(insert_data)
                                connection.commit()
                            else: 
                                cur.execute("CREATE TABLE database-1 (Key VARCHAR(255), Value VARCHAR(255))")
                                insert_data = """INSERT INTO database-1 (Key, Value) VALUES ({},{})""".format(msg[1], msg[2])
                                cur.execute(insert_data)
                                connection.commit()

                            message_to_send = "<" + str(addr[0]) + "> " + 'address saved a record'
                            send_to_clients(message_to_send, conn)
                        elif msg[0] =="R":
                            #how to read records from the DB
                            message_to_send = "<" + str(addr[0]) + "> " + 'address had read' + msg[2] + 'records'
                            send_to_clients(message_to_send, conn)
                    
                else:
                    remove(conn)
                    conn.close()
            except:
                continue


def check_table_exists(db_connection):
    db_cur = db_connection.cursor()
    db_cur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{}'
        """.format('database-1'))
    if db_cur.fetchone()[0] == 1:
        db_cur.close()
        return True

    db_cur.close()
    return False

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

