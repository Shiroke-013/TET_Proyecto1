import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main(argv):
    ip_address = argv[1]
    port = argv[2]
    server.connect((ip_address, port))

    while True:
    	sockets_list = [sys.stdin, server]
    	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    	for socks in read_sockets:
                if socks == server:
                    message = socks.recv(2048)
                    print (message.decode())    
                else:
                    message = sys.stdin.readline()
                    server.send(message.encode())
                    sys.stdout.write(message)
                    sys.stdout.flush()

main(sys.argv)
server.close()