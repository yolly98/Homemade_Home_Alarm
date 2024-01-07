import socket
import queue
from Log import Log

class UDPServer:

    instance = None

    def __init__(self):
        self.local_port = None
        self.msgQueue = queue.Queue()
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def init(self, local_port):
        self.local_port = local_port
        self.udp_socket.bind(('0.0.0.0', local_port))

    @staticmethod
    def get_instance():
        if UDPServer.instance is None:
            UDPServer.instance = UDPServer()
        return UDPServer.instance
    
    def get_message(self):
        return self.msgQueue.get(block=True, timeout=None)
    
    def listen(self):
        while True:
            data, addr = self.udp_socket.recvfrom(self.local_port)
            received_msg = data.decode('utf-8')
            Log.get_instance().print('recv', f"Received UDP message from {addr}: {received_msg}")
            self.msgQueue.put(f'{addr[0]}/{addr[1]}{received_msg}')
            UDPServer.send('ACK', addr[0], int(addr[1]))
            
    def send(msg, ip, port):
        Log.get_instance().print('send', f"Sent UDP message '{msg}' to ({ip}, {port})")
        tmp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tmp_socket.sendto(msg.encode('utf-8'), (ip, port))
        tmp_socket.close()
        