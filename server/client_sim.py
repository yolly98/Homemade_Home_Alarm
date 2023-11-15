import threading
import socket
import queue

CLEINT_PORT = 2920
SERVER_PORT = 2390

class UDPServer:

    instance = None

    def __init__(self):
        self.local_port = None
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def init(self, local_port):
        self.local_port = local_port
        self.udp_socket.bind(('0.0.0.0', local_port))

    @staticmethod
    def get_instance():
        if UDPServer.instance is None:
            UDPServer.instance = UDPServer()
        return UDPServer.instance
    
    def listen(self):
        while True:
            data, addr = self.udp_socket.recvfrom(self.local_port)
            received_msg = data.decode('utf-8')
            print(f"\nReceived UDP message from {addr}: {received_msg}")
            
    def send(self, msg, ip, port):
        self.udp_socket.sendto(msg.encode('utf-8'), (ip, port))


if __name__ == '__main__':
    
    UDPServer.get_instance().init(CLEINT_PORT)

    udp_listener_thread = threading.Thread(target=UDPServer.get_instance().listen)
    
    udp_listener_thread.start()

    while True:
        msg = input()
        UDPServer.get_instance().send(msg, 'localhost', SERVER_PORT)

    udp_listener_thread.join()
    msg_handler_thead.join()