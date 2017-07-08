import socket
import sys
import os
import numpy as np
import pickle
import struct

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''.encode()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

with open('database.txt','r') as f:
    dataset = [tuple(map(str, i.rstrip('\r\n').split(' '))) for i in f]

def init():
    HOST = ""                 # Nome Simbolico que significa todas as interfaces
    PORT = int(sys.argv[1])              # Porta escolhida arbitrariamente escolhida pelo user
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o Socket
    s.bind((HOST, PORT))
    s.listen(10)
    return [HOST, PORT, s, dataset]


def insert_db(t):
    dataset.append(t);
    f = open('database.txt', 'a')
    line = ' '.join(str(x) for x in t)
    f.write(line + '\n')
    f.close()
    return

def create_dir(login):
    directory = "data/" + login + "/"
    if not os.path.exists(directory):
        os.makedirs(directory, 493)
    return directory

def send_status(msg):
    carry = msg.encode()
    data_string = pickle.dumps(carry, -1)
    send_msg(conn, data_string)
    return

def fileServer(directory, conn):
    #receive option
    data = recv_msg(conn)
    data_loaded = pickle.loads(data)
    opt = data_loaded["opt"].decode()
    fileName = data_loaded["fn"].decode()
    #download
    if (opt == "1"):
        file2save = recv_msg(conn)
        file2save_loaded = pickle.dumps(file2save)
        f = open(directory + fileName, "wb")
        f.write(file2save_loaded)
    
    #upload
        
    #share
    return
    
def loginInterface(conn):
    while True:
        data = recv_msg(conn)
        data_loaded = pickle.loads(data)

        ################### LOGIN CREATION ########################
        login_db = [str(i[0]) for i in dataset]
        login = data_loaded["login"].decode()
        senha = data_loaded["senha"].decode()
        opt = data_loaded["option"].decode()
     
        if (opt == "1"):
            if login in login_db:
                send_status("err")
            else:
                insert_db([login, senha])
                directory = create_dir(login)
                send_status("ok")
                fileServer(directory, conn)
                break

        if (opt == "2"):
            # check if login matches password
            if (login, senha) not in dataset:
                send_status("err")
            else:
                send_status("ok")
                fileServer("data/" + login + "/", conn)
                break

        elif (opt == "3"):
            conn.sendall("Fechando essa bagaca!")
    return

[HOST, PORT, s, dataset] = init()
while True:
    conn, addr = s.accept() # Aceita uma conexao e guarda o socket que representa a conexao em conn e adress em addr
    print ('Conectado por: ', addr)

    loginInterface(conn)
    
    
    conn.close() # Fecha a conexao
    
    
    
    
    
    
    
