""" Funcionalidades fundamentais de um cliente da rede estão contidas neste arquivo """

import time
import socket
import logging

class NetworkClient:
    """ Classe NetworkClient """

    def __init__(self):
        """ Construtor """
        self.SERVER_ADDR = ''
        self.PORT = 8888
        self.connect()
        self.logger_setup()
# Setup ------------------------------------------------------------
    def connect(self):
        """ Connect to server """
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((self.SERVER_ADDR, self.PORT))

    def logger_setup(self):
        """ Setup logging functionality """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        # create a file handler
        handler = logging.FileHandler('client/client_history.log')
        handler.setLevel(logging.DEBUG)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # add the handlers to the self.logger
        self.logger.addHandler(handler)

    def send_text(self, msg):
        """ Sends text message through socket connection """
        self.socket_client.sendall(bytes(msg,'UTF-8'))
        self.logger.debug('Message sent from client: {}'.format(msg))

    def recieve_text(self):
        """ Returns string message recieved from socket interface """
        data = self.socket_client.recv(1024)
        data = data.decode()
        self.logger.debug('Message recieved on client: {}'.format(data))
        return data

    def send_file(self, filename, file_size):
        """ Sends a binary file through socket """
        try:
            with open(filename, 'rb') as file:
                file_data = file.read(1024)
                while file_data:
                    self.socket_client.send(file_data)
                    file_data = file.read(1024)
        except:
            self.logger.info('Error uploading through socket. Filename {}, file size: {}'.format(filename, file_size))
            return False
        self.logger.info('Uploaded file {} of size {} to server'.format(filename, file_size))
        return True

    def recieve_file(self, filename, file_size):
        """ Recieves a binary file and writes to filename """
        self.logger.debug('Expecting to recieve a file of size {}'.format(file_size))
        try:
            with open(filename, 'wb') as file:
                recieved_size = 0
                while True:
                    data = self.socket_client.recv(1024)
                    recieved_size += len(data)
                    file.write(data)
                    if recieved_size >= file_size:
                        break
        except:
            self.logger.info('Error: could not write to file {}'.format(filename))
            return False
        self.logger.info('File downloaded and writtent to {}'.format(filename))
        return True

    def close(self):
        """ Close socket connection """
        print('End of client connection')
        self.end_connection()
        self.socket_client.close()

    def end_connection(self):
        """ Sends terminating message to server """
        self.send_text('bye')

# Operation Manegemt ------------------------------------------------------------
    def log_in(self, username, password):
        """ Performs user authentication between server and client

        return: Boolean tuple of user_exists and password_correct

        """
        user_exists, password_correct = False, False
        self.send_text('Log-in request,'+ username + ',' + password)
        response = self.recieve_text()
        time.sleep(1)

        if response == 'Found':
            user_exists, password_correct = True, True
        elif response == 'Password incorrect':
            user_exists, password_correct = True, False
        elif response == 'Not Found':
            user_exists, password_correct = False, False

        return user_exists, password_correct

    def register(self, username, password):
        """ Requests registration of a new user to server """
        self.send_text('Register request,'+ username + ',' + password)
        response = self.recieve_text()
        time.sleep(1)
        if response == 'Created':
            return True
        else:
            return False

    def request_filesystem(self):
        """ Request the user filesystem """
        message = 'View files'
        self.send_text(message)
        response = self.recieve_text()
        time.sleep(1)
        return response

    def upload_file(self, file_path, target_path, file_size):
        """ Uploads a file to the server

        Sends the message in two parts: a header containing the target file path and the file size, then the actual file.

        """
        message = 'Upload request,{},{}'.format(target_path, file_size)
        self.send_text(message)
        time.sleep(0.5)
        self.send_file(file_path, file_size)

    def download_file(self, server_file, client_file):
        """ Downloads a file from the server

        Expects the message in two parts: a header containing the target file path and the file size, then the actual file.
        """
        message = 'Download request,{}'.format(server_file)
        self.send_text(message)
        response = self.recieve_text()
        response = response.split(',')
        if response[0] != 'File exists':
            self.logger.info('Error: file {} not found on server'.format(server_file))
            return False
        self.logger.info('File {} found on server side'.format(server_file))
        file_size = int(response[1])
        self.recieve_file(client_file, file_size)
        return True
