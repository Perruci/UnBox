""" Classe responsável por receber cada cliente em uma Thread """

import socket
import threading

class ClientThread(threading.Thread):
    """ Classe ClientThread

    Responsável por receber um novo cliente em uma thread independente.

    Attributes:
        clientAddress:
        clientsocket:
    """

    def __init__(self,clientAddress,clientsocket):
        """ Contrutor da classe. """
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = clientAddress
        print ("New connection added: ", self.caddress)

    def send_text(self, msg):
        """ Sends text message through socket connection """
        self.csocket.send(bytes(msg,'UTF-8'))

    def recieve_text(self):
        """ Returns text message recieved by the socket """
        data = self.csocket.recv(2048)
        return data.decode()

    def run(self):
        """ Main thread function

        Called after thread is started: ie. thread.start().
        """

        print ("Connection from : ", self.caddress)
        self.send_text("Succsessful connection to server!")
        msg = ''
        while True:
            msg = self.recieve_text()
            if msg=='bye':
              break
            print ("from client", msg)
            self.send_text(msg)
        print ("Client at ", self.caddress , " disconnected...")
