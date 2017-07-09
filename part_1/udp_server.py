import socket

UDP_IP = "192.168.0.11"
UDP_PORT = 10000

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) #definindo o tamanho do buffer
    print "received message:", data