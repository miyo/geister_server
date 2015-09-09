import time
import os
import base64
import socket
import struct
import array
import sys

class websocket_client:
    
    def __init__(self, host, port):
        self.sock = socket.create_connection([host, port])

    def make_ws_data_frame(self, data):
        FIN = 0x80
        RSV1 = 0x0
        RSV2 = 0x0
        RSV3 = 0x0
        OPCODE = 0x1
        MASK = 0x80
        payload = 0x0
        
        frame = struct.pack('B', FIN | RSV1 | RSV2 | OPCODE)
        data_len = len(data)
        if data_len <= 125:
            payload = struct.pack('B', MASK | data_len)
        elif data_len < 0xFFFF:
            payload = struct.pack('!BH', 126 | MASK, data_len)
        else:
            payload = struct.pack('!BQ', 127 | MASK, data_len)
            
        frame += payload
        masking_key = os.urandom(4)
        mask_array = array.array('B', masking_key)
        unmask_data = array.array('B', data.encode('UTF-8'))
            
        for i in range(data_len):
            unmask_data[i] = unmask_data[i] ^ masking_key[i % 4]
            
        mask_data = unmask_data.tobytes()
        frame += masking_key
        frame += mask_data
        
        return [frame, len(frame)]

    HTTP_GET = """GET / HTTP/1.1\r\nConnection: Keep-Alive\r\n\r\n"""

    ws_upgrade_header = {
        'Upgrade' : 'websocket',
        'Connection' : 'Upgrade',
        'Sec-WebSocket-Key' : base64.b64encode(os.urandom(16)).decode('UTF-8'),
        'Sec-WebSocket-Version' : '13',
    }

    def connect(self):
        self.sock.send(websocket_client.HTTP_GET.encode('UTF-8'))

        recv_buf = ""
        recv_buf = self.sock.recv(4096)
        #print(recv_buf.decode('UTF-8'))

        headers = "GET /ws HTTP/1.1\r\nHost: localhost\r\n"
        for key in websocket_client.ws_upgrade_header:
            headers += key + ": " + websocket_client.ws_upgrade_header[key] + "\r\n"
        headers += "\r\n"
        #print(headers)
        self.sock.send(headers.encode('UTF-8'))
        recv_buf = self.sock.recv(4096)

    def send(self, msg):
        message, message_len = self.make_ws_data_frame('Hello')
        self.sock.send(message)

    def recv(self):
        recv_buf = self.sock.recv(4096)
        msg = ""
        if recv_buf[1] > 126:
            msg = recv_buf[3:].decode('UTF-8')
        else:
            msg = recv_buf[2:].decode('UTF-8')
        return msg

    def close(self):
        self.sock.close()

if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    print(argv)
    print(argc)
    port = 8080
    if argc > 1:
        port = int(argv[1])
    client = websocket_client('localhost', port)
    client.connect()
    client.send('Hello')
    msg = client.recv()
    print(msg)
    client.close()
