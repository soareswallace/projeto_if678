import sys
import socket  
import numpy as np
import pandas as pd

PORTA = 5252


if __name__ == '__main__':
    dataset = pd.read_csv("dontOpenPasswordsInside.csv")
    logins = np.array(dataset.iloc[:,0].values)
    senhas = dataset.iloc[:,1].values


    print "Deseja Fazer um Upload(0) ou Download(1) ?"
    operation = int(raw_input())
    s = socket.socket()         # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = PORTA                 # Reserve a port for your service.
    print "O host escolhido foi:",host,":",port    
    if operation == 0:  #Upload
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
        
    if operation == 1:  #Download
        s.bind((host, port))        # Bind to the port
        f = open("reciveFile",'wb')
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
        

        