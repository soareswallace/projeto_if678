import json
import random
import socket

UDP_IP = "localhost"
UDP_PORT = 7777
INIT = {
    "mode": "init"
}
player_on_hold = None

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("Na fila: ", player_on_hold)
    print("Entrou: ", addr)
    if player_on_hold is None:
        player_on_hold = addr
    else:
        players = [1,2]
        random.shuffle(players)

        INIT["player"] = players.pop()
        INIT["addr"] = player_on_hold
        sock.sendto(json.dumps(INIT).encode(), addr)

        INIT["player"] = players.pop()
        INIT["addr"] = addr
        sock.sendto(json.dumps(INIT).encode(), player_on_hold)
        player_on_hold = None
