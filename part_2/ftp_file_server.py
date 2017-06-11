import socket
import sys
import pandas as pd
import numpy as np

HOST = ""                 # Nome Simbolico que significa todas as interfaces
PORT = int(sys.argv[1])              # Porta escolhida arbitrariamente escolhida pelo user
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o Socket
s.bind((HOST, PORT))
s.listen(1) # Somente 1 conexao na fila eh aceita

dataset = np.array( pd.read_csv("dontOpenPasswordsInside.csv").iloc[:,:].values, dtype=str)

while True:
    conn, addr = s.accept() # Aceita uma conexao e guarda o socket que representa a conexao em conn e adress em addr
    print 'Connected by', addr
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data = data.replace(" ", "")
        data = data.split('@')
        option = int(data[0])
        login = data[1]
        senha = data[2]
        while login in dataset[:,0] and option == 1:
            conn.sendall("Login ja existente")
            data = conn.recv(1024)
            if not data:
                break
            data = data.replace(" ", "")
            data = data.split('@')
            option = int(data[0])
            login = data[1]
            senha = data[2]
        if option == 1:
            alloc = pd.DataFrame([{login,senha}])
            alloc.to_csv("dontOpenPasswordsInside.csv", mode="a", header=False, index=False)
            conn.sendall("Login criado com sucesso!")
            conn.close() # Fecha a conexao
        elif option == 2:
            if [login,senha] in dataset:
                conn.sendall("Logado!")
                conn.close() # Fecha a conexao
        else:
            conn.sendall("Login ou senha incorretos!")
            conn.close() # Fecha a conexao

    conn.close() # Fecha a conexao
