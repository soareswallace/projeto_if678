# Echo client program
import socket
import sys

HOST = "localhost"
PORT = int (sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # criando o socket
s.connect((HOST, PORT)) # conectando ao servidor
# USER INTERFACE
login = raw_input("Digite seu login: ");
senha = raw_input("Digite sua senha: ");

s.sendall(login + "@" + senha) # enviando a string hello world 
data = s.recv(1024) # esperando resposta do servidor
s.close()
print 'Received', repr(data) # printa os dados recebidos