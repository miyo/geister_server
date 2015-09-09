import sys
import socket
from contextlib import closing

def main(port):
    host = '127.0.0.1'
    bufsize = 4096
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
        sock.connect((host, port))

        sock.send(b"SET:BCDE\r\n")
        print(sock.recv(bufsize))
        sock.send(b"MOV:A,NORTH\r\n")
        print(sock.recv(bufsize))
        sock.send(b"MOV:A,NORTH\r\n")
        print(sock.recv(bufsize))
        sock.send(b"MOV:A,NORTH\r\n")
        print(sock.recv(bufsize))
        sock.send(b"MOV:A,EAST\r\n")
        print(sock.recv(bufsize))
        sock.send(b"MOV:A,WEST\r\n")
        print(sock.recv(bufsize))
        sock.send(b"MOV:A,SOUTH\r\n")
        print(sock.recv(bufsize))
        sock.send(b"MOV:A,NORTH\r\n")
        print(sock.recv(bufsize))
        sock.send(b"MOV:A,NORTH\r\n")
        print(sock.recv(bufsize))
        sock.send(b"MOV:A,WEST\r\n")
        print(sock.recv(bufsize))
        sock.send(b"MOV:A,WEST\r\n")
        print(sock.recv(bufsize))

        sock.close()

    return

if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    port = 10000
    if argc > 1:
        port = int(argv[1])
    main(port)
  
