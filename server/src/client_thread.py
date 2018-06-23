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

    def authenticate_user(self, username, password):
        """ Username and password authentication """
        # TODO: Access to database
        return True

    def run(self):
        """ Main thread function

        Called after thread is started: ie. thread.start().
        """

        print ("Connection from : ", self.caddress)
        msg = ''
        while True:
            msg = self.recieve_text()
            if msg=='bye':
                print ("Client at ", self.caddress , " disconnected...")
                break
            split_msg = msg.split(',')
            if split_msg[0] == 'Log-in request':
                print('Log-in request')
                username = split_msg[1]
                password = split_msg[2]
                print('Username: {}'.format(username))
                print('Password: {}'.format(password))
                if self.authenticate_user(username, password):
                    print('User authenticated')
                    self.send_text('Found')
                else:
                    print('Authentication failure')
                    self.send_text('Not Found')
