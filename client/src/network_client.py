""" Funcionalidades fundamentais de um cliente da rede estão contidas neste arquivo """

import time
import socket

class NetworkClient:
    """ Classe NetworkClient """

    def __init__(self):
        """ Construtor """
        self.SERVER_ADDR = ''
        self.PORT = 8888

    def connect(self):
        """ Connect to server """
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((self.SERVER_ADDR, self.PORT))
        self.send_text("This is from Client")

    def send_text(self, msg):
        """ Sends text message through socket connection """
        self.socket_client.sendall(bytes(msg,'UTF-8'))

    def recieve_text(self):
        """ Returns string message recieved from socket interface """
        data = self.socket_client.recv(1024)
        return data.decode()

    def end_connection(self):
        """ Sends terminating message to server """
        self.send_text('bye')

    def log_in(self, username, password):
        """ Performs user authentication between server and client """
        self.send_text('Log-in request,'+ username + ',' + password)
        response = self.recieve_text()
        time.sleep(1)
        print(response)
        if response == 'Found':
            return True
        else:
            return False

    def run(self):
        """ Realiza loop principal de aquisição de dados """
        in_data =  self.socket_client.recv(1024)
        print("From Server :" ,in_data.decode())
        out_data = input()
        self.send_text(out_data)
        if out_data=='bye':
            return False
        return True

    def close(self):
        """ Close socket connection """
        print('End of client connection')
        self.end_connection()
        self.socket_client.close()
