import socket
import sys

def init():
	HOST = "localhost"
	PORT = int(sys.argv[1])    #leitura da porta que sera dada com input do user.
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # criando o socket
	s.connect((HOST, PORT)) # conectando ao servidor
	return [HOST, PORT, s]

def readCred():
	login = raw_input("Digite seu login: ")
	senha = raw_input("Digite sua senha: ")
	return [login, senha]

def menu():
	opt = raw_input("\n1 - Criar login\n2 - Login\n3-Sair\nDigite opcao: ")
	[login, senha] = readCred()
	return [int(opt), login, senha]

def send_string(str):
	s.sendall(str) # enviando a string hello world
	data = s.recv(1024) # esperando resposta do servidor
	print (repr(data))
	return data

def send_file(fileName):
	f = open(fileName,'rb')
	l = f.read(1024)
	while (l):
	    print 'Enviando...'
	    s.send(l)
	    l = f.read(1024)
	f.close()
	print "Terminei de enviar"
	s.shutdown(socket.SHUT_WR)
	return

def file_clnt():
	opt = raw_input("\n1 - Upload\n2 - Download\n3-Sair\nDigite opcao: ")
	fileName = raw_input("Digite o nome do arquivo (nome.formato): ")
	str2send = opt + "@" + fileName + "@" + "trash"
	data = send_string(str2send)
	send_file(fileName)

def conn_interface(opt, login, senha):
	# Create login
	if opt == 1:
		while True:
			str2send = str(opt) + "@" + login + "@" + senha
			data = send_string(str2send)
			if (repr(data) != "'Login ja existente!'"):
				break
			else:
				[login, senha] = readCred()

	# Login to existing accounts
	if opt == 2:
		while True:
			str2send = str(opt) + "@" + login + "@" + senha
			data = send_string(str2send)
			if (repr(data) != "'Login ou senha incorretos!'"):
				break
			elif (repr(data) != "'Logado!'"):
				[login, senha] = readCred()
			else:
				print "Bugou"
				return

	file_clnt()
	return

#--Global variables-#
opt = 0
data = "l"
[HOST, PORT, s] = init() # initialize
#------------------#

while True:
	# --------------------------- CONNECTION ----------------------------------#
	[opt, login, senha] = menu() # login (menu)
	if opt == 3:
		break

	###########CONNECTION INTERFACE##############
	conn_interface(opt, login, senha)
	############################################

	#########          Login        ###########
	# while True:
	# 	print "Bem-vindo a Zuera"
	# 	print "Escolha o arquivo"
	# 	fileName = raw_input()
	# 	print "O arquivo escolhido foi", fileName
	# 	f = open(fileName, 'rb')
	# 	print "Sending..."
	# 	l = f.read(1024)
	# 	while (l):
	# 		print "Sending..."
	# 		s.send(l)
	# 		l = f.read(1024)
	# 	f.close()
	# 	s.shutdown(socket.SHUT_WR) #esse negocio chato
	# 	print "Done Sending"
	# 	data = s.recv(1024) # esperando resposta do servidor
	# 	print "Servidor disse:", data
	# opt = raw_input("Digite 3 para sair, qualquer outra coisa para continuar...\n")
	#print 'Received', repr(data) # printa os dados recebidos
	###########################################
	#-----------------------------------------------------------------#

	#--------------------SISTEMA DE ARQUIVOS--------------------------------#

	#--------------------------------------------------------------------------#
s.close()
