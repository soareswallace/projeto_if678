import socket
import sys

#Criando um socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connectando o socket a um servidor que esteja escutando a porta descrita
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
try:

    # Send data
    message = 'Esta eh a mensagem que sera repetida.'
    print >>sys.stderr, 'Enviando %s"' % message
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'Mensagem recebida "%s"' % data

finally:
    print >>sys.stderr, 'Socket sendo fechada'
    sock.close()
