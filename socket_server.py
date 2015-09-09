import socket
import select

from geister_server import GeisterServer

def exec_command(sock, str, pid):
    r = True
    while True:
        i = str.find('\r\n')
        if i == -1:
            break
        cmd = str[:i]
        str = str[i+2:]
        
        r = r and GeisterServer().command(cmd, pid)
        GeisterServer().print_board()
                    
    if r :
        sock.send(b"OK")
    else :
        sock.send(b"NG")

    return str

def main():
    port = [10000, 10001]
    bufsize = 4096

    server_sock = [socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                   socket.socket(socket.AF_INET, socket.SOCK_STREAM)]
    readfds = set(server_sock)
    try:
        for i in range(2):
            server_sock[i].bind(("", port[i]))
            server_sock[i].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock[i].listen(1)

        conn = [None, None]
        msg = ["", ""]
        
        while True:
            rready, wready, xready = select.select(readfds, [], [])
            for sock in rready:
                if sock is server_sock[0]:
                    conn[0], address = server_sock[0].accept()
                    readfds.add(conn[0])
                elif sock is server_sock[1]:
                    conn[1], address = server_sock[1].accept()
                    readfds.add(conn[1])
                else:
                    m = sock.recv(bufsize)
                    if sock is conn[0]:
                        pid = 0
                    elif sock is conn[1]:
                        pid = 1
                    else:
                        sock.send(b"NG")
                        contine
                        
                    msg[pid] = msg[pid] + m.decode('UTF-8')
                    msg[pid] = exec_command(sock, msg[pid], pid)

    finally:
        for sock in readfds:
            sock.close()
    return

if __name__ == '__main__':
  main()

