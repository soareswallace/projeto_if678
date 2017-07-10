import socket
import sys
import pickle
import getpass
import struct

#!-*- conding: utf8 -*-

def init():
    HOST = "localhost"
    PORT = int(sys.argv[1])    #leitura da porta que sera dada com input do user.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # criando o socket
    s.connect((HOST, PORT)) # conectando ao servidor
    return [HOST, PORT, s]
	
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

def readCred():
    opt = input("1 - Criar Login\n2 - Logar\nDigite opcao: ")
    log = input("Digite login: ")
    senha = getpass.getpass("Digite senha: ")

    return [opt, log, senha]
    
def funcLogin():
    #Login
    status = ""
    while True:
        [opt, login, senha] = readCred()
        carry = {"option": opt, "login": login, "senha": senha}
        data_string = pickle.dumps(carry, -1)
        send_msg(s, data_string)
        
        status = recv_msg(s)
        st = pickle.loads(status)
        
        if (st == "err"):
            if (opt == "1"):
                print ("Login ja existe.")
            elif (opt == "2"):
                print ("Login ou senha incorretos.")
        
        elif (st == "ok"):
            break
    print ("Logado!")
    return

def download(fileName, s):
    byte_file = recv_msg(s)
    file_received = pickle.loads(byte_file)
    file2recv = open("downloads/" + fileName, 'wb')
    file2recv.write(file_received)
    file2recv.close()
    return
    
def upload(fileSrc, s):
    file2send = open(fileSrc, 'rb')
    fileLoad = file2send.read()
    byte_file = pickle.dumps(fileLoad, -1)
    send_msg(s, byte_file)
    st = recv_msg(s)
    print (pickle.dumps(st))

    if (st == "err"):
        print ("deu erro")        
    elif (st == "ok"):
        print ("deu certo")
    file2send.close()
    return

def fileServer():
    #receive option
    opt = input("1- Upload\n2- Download\n3- Criar pasta\n5- Sair\nDigite opcao: ")
    if (opt == "5"):
        carry = {"opt":opt}
        data_string = pickle.dumps(carry,-1)
        send_msg(s,data_string)
        return 5
    
    #create folder
    if (opt == "3"):
        folderName = input("Digite o nome da pasta: ")
        carry = {"opt":opt, "foldername":folderName} 
        data_string = pickle.dumps(carry,-1)
        send_msg(s,data_string)
        st = recv_msg(s)
        st_received = pickle.loads(st)
        
        if (st_received == "exfolder"):
            print ("Ja existe pasta com esse nome!")
            return -1
        
        else:
            return 3
       
    if (opt == "4"):
        folderName = input("Digite o nome da pasta: ")
        fileName = input("Digite o nome do arquivo: (enter para toda a pasta)")
        login = input("Digite o nome do usuario para compartilhar: ")
        carry = {"opt":opt, "foldername":folderName, "filename":fileName, "login":login}        
        data_string = pickle.dumps(carry,-1)
        send_msg(s,data_string)
        st = recv_msg(s)
        st_received = pickle.loads(st)
        
        print(st_received)

    #upload
    if (opt == "1"):
        folderName = input("Digite o nome da pasta de destino no server (enter para raiz): ")
        fileName = input("Digite o nome do arquivo: ")
        
        file2send = open(fileName, 'rb')
        fileLoad = file2send.read()
        byte_file = pickle.dumps(fileLoad, -1)

        carry = {"opt":opt, "foldername": folderName,"fn":fileName, "filecontent":byte_file}
        data_string = pickle.dumps(carry, -1)
        send_msg(s, data_string)
        
        st = recv_msg(s)
        print (pickle.loads(st))
        
    #download
    elif (opt == "2"):
        folderName = input("Digite o nome da pasta de origem no server (enter para raiz): ")
        fileName = input("Digite o nome do arquivo: ")

        carry = {"opt":opt, "foldername": folderName,"fn":fileName}
        data_string = pickle.dumps(carry, -1)
        send_msg(s, data_string)
        
        file2recv = open(fileName, 'wb')
        filerecv = recv_msg(s)
        filerecv_loaded = pickle.loads(filerecv)
        file2recv.write(filerecv_loaded)
        file2recv.close()
        
        st = recv_msg(s)
        print (pickle.loads(st))
    else:
        return -1
    
    return 0

#--Global variables-#
[HOST, PORT, s] = init() # initialize
#------------------#

funcLogin()
while True:
    # --------------------------- CONNECTION ----------------------------------#
    ##########CONNECTION INTERFACE##############
    ex = fileServer()
    if (ex == 5):
        break
        
    elif (ex == 3):
        print ("Pasta criada!")

    elif(ex == -1):    
        print ("Operacao invalida!")
	###########################################
	#--------------------------------------------------------------------------#
s.close()
