PORTA = 5252

s = socket.socket()         # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = PORTA                 # Reserve a port for your service.
    print "O host escolhido foi:",host,":",port  

s.bind((host, port))        # Bind to the port
f = open("receiveFile",'wb')
s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    print "Receiving..."
    l = c.recv(1024)
    while (l):
        print "Receiving..."
        f.write(l)
        l = c.recv(1024)
    f.close()
    print "Done Receiving"
    c.send('Thank you for connecting')
    c.close()                # Close the connection