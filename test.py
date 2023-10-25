import socket

# Crea un socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('192.168.178.48', 2390)  # Sostituisci con il tuo indirizzo IP e porta

while True:
    message = input("Inserisci il tuo messaggio: ")

    if message.lower() == "esci":
        break

    # Invia il messaggio
    sent = sock.sendto(message.encode(), server_address)

    # Aspetta la risposta
    print('In attesa di risposta...')
    data, server = sock.recvfrom(4096)
    print('Ricevuto {!r}'.format(data.decode()))

sock.close()