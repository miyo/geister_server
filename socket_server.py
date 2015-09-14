import socket
import select

from geister_server import GeisterServer

def exec_command(sock, conn, str, pid):
    r = True
    while True:
        i = str.find('\r\n')
        if i == -1:
            break
        cmd = str[:i]
        str = str[i+2:]
        
        r = GeisterServer().command(cmd, pid)
        GeisterServer().print_board()
        print(cmd)
        print(r)
                    
    if r :
        
        if GeisterServer().status() == GeisterServer.WAIT_FOR_PLAYER0:
            conn[0].send(GeisterServer().encode_board(0).encode())
        elif GeisterServer().status() == GeisterServer.WAIT_FOR_PLAYER1:
            conn[1].send(GeisterServer().encode_board(1).encode())
        elif GeisterServer().status() == GeisterServer.GAME_END:
            winner = GeisterServer().winner()
            looser = 1 if winner == 0 else 1
            conn[winner].send(b'WON'); conn[winner].close(); conn[winner] = None
            conn[looser].send(b'LOST'); conn[looser].close(); conn[looser] = None
            GeisterServer().server_init()
            
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
                if sock is server_sock[0] and conn[0] is None:
                    conn[0], address = server_sock[0].accept()
                    readfds.add(conn[0])
                    conn[0].send(b"SET?")
                elif sock is server_sock[1] and conn[1] is None:
                    conn[1], address = server_sock[1].accept()
                    readfds.add(conn[1])
                    conn[1].send(b"SET?")
                else:
                    if sock is conn[0]:
                        pid = 0
                    elif sock is conn[1]:
                        pid = 1
                    else:
                        continue
                        
                    m = sock.recv(bufsize)
                    msg[pid] = msg[pid] + m.decode('UTF-8')
                    msg[pid] = exec_command(sock, conn, msg[pid], pid)
                    if conn[0] is None and conn[1] is None:
                        readfds = set(server_sock)

    finally:
        for sock in readfds:
            sock.close()
    return

if __name__ == '__main__':
  main()

