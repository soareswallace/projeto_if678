import sys
import socket  
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
 
class App(QWidget):
 
    def __init__(self):
        super(App, self).__init__()
        self.title = 'IF678 - FTP'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        #self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
        self.openFileNameDialog()
        #self.openFileNamesDialog()
        #self.saveFileDialog()
 
 
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            return fileName


if __name__ == '__main__':
    print "Deseja Fazer um Upload(0) ou Download(1) ?"
    operation = int(raw_input())
    if operation == 0:  #Upload
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12340                 # Reserve a port for your service.
        print "O host escolhido foi:",host,":",port
        s.connect((host, port))
        print "Escolha o arquivo:"
        app = QApplication(sys.argv)
        fileName = App().openFileNameDialog();
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
        s = socket.socket()         # Create a socket object
        host = socket.gethostname()  # Get local machine name
        port = 12340                 # Reserve a port for your service.
        print "O host escolhido foi:",host,":",port
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
        

        