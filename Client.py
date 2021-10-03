import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main(argv):
    ip_address = argv[1]
    port = int(argv[2])
    server.connect((ip_address, port))
    aux = True
    
    while aux:
    	sockets_list = [sys.stdin, server]
    	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    	for socks in read_sockets:
                if socks == server:
                    message = socks.recv(2048)
                    print (message.decode())    
                else:
                    message = sys.stdin.readline().replace("\n", "")
                    if message == "exit":
                        server.close()
                        aux = False
                    else:
                        server.send(message.encode())
                        sys.stdout.flush()
    
main(sys.argv)
