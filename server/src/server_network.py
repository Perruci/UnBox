""" Funcionalidades fundamentais de um servidor da rede estão contidas neste arquivo """

import socket
import threading
import client_thread

class ServerNetwork:
    """ Classe ServerNetwork """

    def __init__(self):
        """ Construtor """
        self.LOCALHOST = ''
        self.PORT = 8888
        self.threads = []

    def __del__(self):
        self.close()

    def setup(self):
        """ Setup server network connections """
        # Server network setup
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind((self.LOCALHOST, self.PORT))
        print("Server started")
        print("Waiting for client request..")

    def monitor(self):
        """ Monitors new clients and starts a client thread for each one """
        self.socket_server.listen(1)
        clientsock, clientAddress = self.socket_server.accept()
        newthread = client_thread.ClientThread(clientAddress, clientsock)
        newthread.start()
        self.threads.append(newthread)

    def close(self):
        """ Close threads """
        for thread in self.threads:
            thread.join()
