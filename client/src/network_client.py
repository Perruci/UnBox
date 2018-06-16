""" Funcionalidades fundamentais de um cliente da rede estão contidas neste arquivo """

import socket
import messages

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
        self.socket_client.sendall(messages.send_text("This is from Client"))

    def run(self):
        """ Realiza loop principal de aquisição de dados """
        in_data =  self.socket_client.recv(1024)
        print("From Server :" ,in_data.decode())
        out_data = input()
        self.socket_client.sendall(messages.send_text(out_data))
        if out_data=='bye':
            return False
        return True

    def close(self):
        """ Close socket connection """
        print('End of client connection')
        self.socket_client.sendall(messages.send_text('bye'))
        self.socket_client.close()
