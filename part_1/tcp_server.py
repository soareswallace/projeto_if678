import socket
import sys

#Criando um socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ligando o socket a porta descrita para inciar a escuta do server
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
#esperando conexao
sock.listen(1)
while True:
    # esperando conexao
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()
	try:
		print >>sys.stderr, 'connection from', client_address
		#os dados estao chegando em pedacos e estao sendo retransmitidos
		while True:
			data = connection.recv(1024)
			print >>sys.stderr, 'received "%s" ' %data
			if data:
				print >>sys.stderr, 'sending data back to the client'
				connection.sendall(data)
			else:
				print >>sys.stderr, 'no more data from', client_address
				break
	finally:
		#fechando conexao
		connection.close()
