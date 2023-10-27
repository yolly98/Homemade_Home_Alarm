import socket
import threading
from pydub import AudioSegment
from pydub.playback import play
import time

server_ip = '192.168.178.48'
server_port = 2390
local_port = 2390
alarm = AudioSegment.from_file("alarm.mp3")

ALARM_STATUS = False

def alarm_player():
    global ALARM_STATUS
    print("Listener thread started")
    while True:
        if ALARM_STATUS:
            play(alarm)

def udp_listener():
    global ALARM_STATUS
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', local_port))
    print("Listener thread started")
    while True:
        data, addr = udp_socket.recvfrom(local_port)
        received_msg = data.decode('utf-8')
        print(f"\nReceived UDP message from {addr}: {received_msg}")
        udp_socket.sendto("ACK".encode('utf-8'), (server_ip, server_port))
        if received_msg != 'ACK':
            received_msg = received_msg.split('/')
            if received_msg[3] == 'DETECTED':
                ALARM_STATUS = True
            elif received_msg[3] == 'FREE':
                ALARM_STATUS = False

def udp_sender():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Sender Thread started")
    while True:
        message = input("Insert Message to send: ")
        udp_socket.sendto(message.encode('utf-8'), (server_ip, server_port))

udp_listener_thread = threading.Thread(target=udp_listener)
udp_sender_thread = threading.Thread(target=udp_sender)
alarm_player_thread = threading.Thread(target=alarm_player)

udp_listener_thread.start()
udp_sender_thread.start()
alarm_player_thread.start()
