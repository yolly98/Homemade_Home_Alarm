import socket
import threading

server_ip = '192.168.178.48'
server_port = 2390
local_port = 2390

def udp_listener():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', local_port))
    print("Listener thread started")
    while True:
        data, addr = udp_socket.recvfrom(local_port)
        print(f"\nReceived UDP message from {addr}: {data.decode('utf-8')}")

def udp_sender():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Sender Thread started")
    while True:
        message = input("Insert Message to send: ")
        udp_socket.sendto(message.encode('utf-8'), (server_ip, server_port))

udp_listener_thread = threading.Thread(target=udp_listener)
udp_sender_thread = threading.Thread(target=udp_sender)

udp_listener_thread.start()
udp_sender_thread.start()
