import socket
import sys
import pickle
import getpass
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

def init():
	HOST = "localhost"
	PORT = int(sys.argv[1])    #leitura da porta que sera dada com input do user.
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # criando o socket
	s.connect((HOST, PORT)) # conectando ao servidor
	return [HOST, PORT, s]

def funcLogin(opt, login, senha):
    #Login
    status = ""
    while True:
        #print ("Enviando", opt, login, senha)
        carry = {"option": opt.encode(), "login": login.encode(), "senha": senha.encode()}
        data_string = pickle.dumps(carry, -1)
        send_msg(s, data_string)
        status = recv_msg(s)
        status_loaded = pickle.loads(status)
        print (status_loaded["result"].decode())
        break
        if (status == "err"):
            if (opt == 1):
                print ("Login ja existe.")
            elif (opt == 2):
                print ("Login ou senha incorretos.")

        elif (status == "ok"):
            break

    print ("Logado!")
    return

def readCred():
    opt = input("Digite opcao - 1 ou 2: ")
    log = input("Digite login: ")
    senha = getpass.getpass("Digite senha: ")

    return [opt, log, senha]

#--Global variables-#
[HOST, PORT, s] = init() # initialize
#------------------#

while True:
	# --------------------------- CONNECTION ----------------------------------#
	init()
	[opt, login, senha] = readCred()

	if opt == 3:
		break

	else:
	    ###########CONNECTION INTERFACE##############
	    funcLogin(opt, login, senha)
	    ############################################
	break
	#--------------------------------------------------------------------------#
s.close()
