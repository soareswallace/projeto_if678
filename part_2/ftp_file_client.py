# Echo client program
import socket
import sys
opt = '0'
while opt != '3':
	HOST = "localhost"
	PORT = int(sys.argv[1])    #leitura da porta que sera dada com input do user.
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # criando o socket
	s.connect((HOST, PORT)) # conectando ao servidor
	# USER INTERFACE]

	# --------------------- LOGIN -------------------------------------#
	opt = raw_input("\n1 - Criar login\n2 - Login\nDigite opcao: ")
	login = raw_input("Digite seu login: ");
	senha = raw_input("Digite sua senha: ");

	s.sendall(opt + "@" + login + "@" + senha) # enviando a string hello world
	data = s.recv(1024) # esperando resposta do servidor
	print repr(data)
	while data == "Login ja existente":
		opt = raw_input("\n1 - Criar login\n2 - Login\nDigite opcao: ")
		login = raw_input("Digite seu login: ");
		senha = raw_input("Digite sua senha: ");

		s.sendall(opt + "@" + login + "@" + senha) # enviando a string hello world
		data = s.recv(1024) # esperando resposta do servidor
		print repr(data)
	while data == "Logado!":
		print "Bem-vindo a Zuera"
		print "Escolha o arquivo"
		fileName = raw_input()
		print "O arquivo escolhido foi", fileName
		f = open(fileName, 'rb')
		print "Sending..."
		l = f.read(1024)
		while (l):
			print "Sending..."
			s.send(l)
			l = f.read(1024)
		f.close()
		s.shutdown(socket.SHUT_WR)
		print "Done Sending"
		data = s.recv(1024) # esperando resposta do servidor
		print "Servidor disse:", data
	opt = raw_input("Digite 3 para sair, qualquer outra coisa para continuar...\n")
	#print 'Received', repr(data) # printa os dados recebidos
	#-----------------------------------------------------------------#

	#--------------------SISTEMA DE ARQUIVOS--------------------------------#

	#--------------------------------------------------------------------------#
s.close()