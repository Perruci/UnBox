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

    def run(self):
        """ Main thread function

        Called after thread is started: ie. thread.start().
        """
        
        print ("Connection from : ", self.caddress)
        self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg=='bye':
              break
            print ("from client", msg)
            self.csocket.send(bytes(msg,'UTF-8'))
        print ("Client at ", self.caddress , " disconnected...")
