import socket
import sys
import pandas as pd
import numpy as np

HOST = ""                 # Nome Simbolico que significa todas as interfaces
PORT = int(sys.argv[1])              # Porta escolhida arbitrariamente escolhida pelo user
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o Socket
s.bind((HOST, PORT))
s.listen(10) # Somente 1 conexao na fila eh aceita
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
        elif option == 2:
            enviar_again = 1
            while [login,senha] in dataset and enviar_again == 1:
                f = open('recebido_ftp', 'wb')
                conn.sendall("Logado!")
                l = conn.recv(1024)
                while(l):
                    f.write(l)
                    l = conn.recv(1024)
                f.close()
                print "Recebido pelo servidor"
                conn.send('Recebi')
                conn.send('Quer enviar mais um arquivo ? \n1 - Sim\n0 - Nao ')
                
                enviar_again = conn.recv(1024)
                if enviar_again == '1':
                    enviar_again = 1
                    conn.sendall("Logado!")
        elif option == 3:
            conn.sendall("Fechando essa bagaca!")

    conn.close() # Fecha a conexao
