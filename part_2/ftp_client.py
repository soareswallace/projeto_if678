import socket
import sys
import pickle
import getpass
import struct

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
        carry = {"option": opt.encode(), "login": login.encode(), "senha": senha.encode()}
        data_string = pickle.dumps(carry, -1)
        send_msg(s, data_string)
        
        status = recv_msg(s)
        st = pickle.loads(status).decode()
        
        if (st == "err"):
            if (opt == "1"):
                print ("Login ja existe.")
            elif (opt == "2"):
                print ("Login ou senha incorretos.")
        
        elif (st == "ok"):
            break
    print ("Logado!")
    return

def fileServer():
    #receive option
    opt = input("1 - Upload\n2- Download\n4- Sair\nDigite opcao: ")
    if (opt == "4"):
        carry = {"opt":opt.encode(), "fn":"".encode()}
        data_string = pickle.dumps(carry,-1)
        send_msg(s,data_string)
        return 1
    
    fileName = input("Digite o nome do arquivo: ")
    carry = {"opt":opt.encode(), "fn":fileName.encode()}
    data_string = pickle.dumps(carry, -1)
    send_msg(s, data_string)
    #upload
    if (opt == "1"):
        file2send = open(fileName, 'rb')
        fileLoad = file2send.read()
        byte_file = pickle.dumps(fileLoad, -1)
        send_msg(s, byte_file)
        file2send.close()
        
    #download
    elif (opt == "2"):
        byte_file = recv_msg(s)
        file_received = pickle.loads(byte_file)
        file2recv = open("downloads/" + fileName, 'wb')
        file2recv.write(file_received)
        file2recv.close()
    #share
    
    return 0

#--Global variables-#
[HOST, PORT, s] = init() # initialize
#------------------#

funcLogin()
while True:
	# --------------------------- CONNECTION ----------------------------------#
	##########CONNECTION INTERFACE##############
	ex = fileServer()
	if (ex == 1):
	    break
	###########################################
	#--------------------------------------------------------------------------#
s.close()
