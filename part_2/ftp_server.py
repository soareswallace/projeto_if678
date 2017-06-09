import socket
import sys

HOST = ""                 # Nome Simbolico que significa todas as interfaces
PORT = int(sys.argv[1])              # Porta escolhida arbitrariamente
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o Socket
s.bind((HOST, PORT))
s.listen(1) # Somente 1 conexao na fila eh aceita
conn, addr = s.accept() # Aceita uma conexao e guarda o socket que representa a conexao em conn e adress em addr
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break # Se nao tiver dados recebido (0) significa que a conexao acabou
    data = data.split('@')
    conn.sendall(data[0])
conn.close() # Fecha a conexao