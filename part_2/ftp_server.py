import socket
import sys
import os
import pickle
import struct
import threading
from threading import Thread

def send_msg(sock, msg):
    print ("tamanho da mensagem:", len(msg))
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

dataset = {}
with open('dataset.txt','rb') as f:
    if os.path.getsize('dataset.txt') > 0: 
        dataset = pickle.loads(f.read())

folders = {}
with open('folders.txt','rb') as f:
    if os.path.getsize('folders.txt') > 0: 
        folders = pickle.loads(f.read())

def init():
    HOST = sys.argv[1]               # Nome Simbolico que significa todas as interfaces
    PORT = int(sys.argv[2])              # Porta escolhida arbitrariamente escolhida pelo user
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o Socket
    s.bind((HOST, PORT))
    s.listen(10)
    return [HOST, PORT, s, dataset]


def insert_db(login, senha):
    dataset[login] = senha;
    with open('dataset.txt','wb') as f: 
        pickle.dump(dataset,f)
    return

def create_dir(login, folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName, 493)
        folders[login].append(folderName)
        return folderName
    return "exfolder"

def send_status(conn, msg):
    carry = msg
    data_string = pickle.dumps(carry, -1)
    send_msg(conn, data_string)
    return

def download(fileDst,fileCnt, conn):
    f = open(fileDst, "wb")
    f.write(pickle.loads(fileCnt))
    f.close()
    return

def upload(fileSrc, conn):
    file2send = open(fileSrc, 'rb')
    fileLoad = file2send.read()
    byte_file = pickle.dumps(fileLoad, -1)
    send_msg(conn, byte_file)
    file2send.close()
    return


def fileServer(login, conn):
    #global folders
    #receive option
    print (folders)
    while True:
        data = recv_msg(conn)
        if (data is None):
            break
        data_loaded = pickle.loads(data)
        
        opt = data_loaded["opt"]
        
        #se o cliente faz upload
        if (opt == "1"):            
            folderName = data_loaded["foldername"]
            fileName = data_loaded["fn"]
            pth = folderName + "/" + fileName 
            print (login)
            if (folderName in folders[login]):
                download(pth, data_loaded["filecontent"], conn)
                send_status(conn, "ok")
            else:
                send_status(conn, "err")
            
        #se o cliente faz download
        if (opt == "2"):
            folderName = data_loaded["foldername"]
            fileName = data_loaded["fn"]
            pth = folderName + "/" + fileName
            if (pth in folders[login] or folderName in folders[login]):
                send_status(conn, "ok")
                upload(pth, conn)
            else:
                send_status(conn, "err")
            
        #create folder
        if (opt == "3"):
            folderName = data_loaded["foldername"]
            st = create_dir(login, folderName)
            saveFolders()
            data = pickle.dumps(st,-1)
            send_msg(conn, data)
        
        #share
        if (opt == "4"):
            logshare = data_loaded["login"]
            fileName = data_loaded["filename"]
            folderName = data_loaded["foldername"]
            
            name = folderName
            if (fileName != ""):
                name += + "/" + fileName
                
            if (logshare in dataset and name in folders[login]):
                folders[logshare].append(name)
            saveFolders()
            data = pickle.dumps("ok",-1)
            send_msg(conn,data)
        if (opt == "5"):
            break
    return -1

def saveFolders():
    with open('folders.txt','wb') as folderFile:
        folder_byte = pickle.dumps(folders)
        folderFile.write(folder_byte)
        folderFile.close()

def loginInterface(conn,addr):
    while True:
        data = recv_msg(conn)
        if (data is None):
            break
        data_loaded = pickle.loads(data)
        login = data_loaded["login"]
        senha = data_loaded["senha"]
        opt = data_loaded["option"]
        ex = 0
        if (opt == "1"):
            if login in dataset:
                send_status(conn, "err")
            else:
                insert_db(login, senha)
                folders[login] = []
                saveFolders()
                send_status(conn, "ok")
                ex = fileServer(login, conn)
                break

        if (opt == "2"):
            # check if login matches password
            if login not in dataset or dataset[login] != senha:
                send_status(conn,"err")
            else:
                send_status(conn,"ok")
                ex = fileServer(login, conn)
                break

        if (ex == "-1"):
            break
    return

[HOST, PORT, s, dataset] = init()

while True:
    conn, addr = s.accept()
    print ("Conectado por: ", addr[0])
    thread = threading.Thread(target = loginInterface, args=(conn,addr))
    thread.start()
    
    
    
    
