import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print "IP de destindo:", UDP_IP
print "Porta de Destino:", UDP_PORT
print "Mensagem:", MESSAGE

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))