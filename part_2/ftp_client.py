PORTA = 5252

s = socket.socket()         # Create a socket object
host = socket.gethostname()  # Get local machine name
port = PORTA                 # Reserve a port for your service.
print "O host escolhido foi:",host,":",port  

s.connect((host, port))
print "Escolha o arquivo:"
#Digitar file
fileName = raw_input()
print "O arquivo escolhido foi:",fileName

f = open(fileName,'rb')
print 'Sending...'
l = f.read(1024)
while (l):
    print 'Sending...'
    s.send(l)
    l = f.read(1024)
f.close()
print "Done Sending"
s.shutdown(socket.SHUT_WR)
print s.recv(1024)
s.close()

