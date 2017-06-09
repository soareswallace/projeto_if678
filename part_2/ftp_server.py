import socket
import sys
import pandas as pd
import numpy as np
HOST = ""                 # Nome Simbolico que significa todas as interfaces
PORT = int(sys.argv[1])              # Porta escolhida arbitrariamente
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o Socket
s.bind((HOST, PORT))
s.listen(1) # Somente 1 conexao na fila eh aceita
conn, addr = s.accept() # Aceita uma conexao e guarda o socket que representa a conexao em conn e adress em addr
print 'Connected by', addr

dataset = np.array( pd.read_csv("dontOpenPasswordsInside.csv").iloc[:,:].values, dtype=str)


while 1:
    data = conn.recv(1024)
    if not data: continue # Se nao tiver dados recebido (0) significa que a conexao acabou
    data = data.replace(" ", "")
    data = data.split('@')
    option = int(data[0])
    login = data[1]
    senha = data[2]
    for l in data:
        conn.sendall(l)
    if option == 1:  # Criar
        if login in dataset[:,0]:
            conn.sendall("Login ja existente")
    elif option == 2:  
        if [login,senha] in dataset:
            conn.sendall("Logado!")
    
        
conn.close() # Fecha a conexao