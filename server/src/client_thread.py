""" Classe responsável por receber cada cliente em uma Thread """

import socket
import threading
import logging
import time

import database

SERVER_BUFF = 1024

class ClientThread(threading.Thread):
    """ Classe ClientThread

    Responsável por receber um novo cliente em uma thread independente.

    Attributes:
        clientAddress: endereço e porta de conexão do socket.
        clientsocket: objeto socket já conectado ao cliente
    """

    def __init__(self,clientAddress,clientsocket):
        """ Contrutor da classe. """
        threading.Thread.__init__(self)
        self.client_socket = clientsocket
        self.client_address = clientAddress
        self.logger_setup()
        self.logger.info('Connection to client at {}'.format(self.client_address))
        print('New connection added: ', self.client_address)


    def run(self):
        """ Main thread function

        Called after thread is started: ie. thread.start().
        Recieves operation commands through socket and performs them.
        """

        print ('Connection from : {}'.format(self.client_address))
        message = ''
        while True:
            message = self.recieve_text()
            if message=='bye':
                print ('User {} at {} disconnected...'.format(self.username, self.client_address))
                break
            # Processes an operation commands (comma separated) -----------------------------
            message = message.split(',')
            if message[0] == 'Log-in request':
                self.log_in_request(message)

            elif message[0] == 'Register request':
                self.register_request(message)

            elif message[0] == 'View files':
                self.view_files_request()

            elif message[0] == 'Upload request':
                self.upload_request(message)

            elif message[0] == 'Download request':
                self.download_request(message)

            elif message[0] == 'Move request':
                self.move_file_request(message)

            elif message[0] == 'Remove request':
                self.remove_file_request(message)

    def logger_setup(self):
        """ Setup logging functionality """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        # create a file handler
        handler = logging.FileHandler('server/server_history.log')
        handler.setLevel(logging.DEBUG)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # add the handlers to the self.logger
        self.logger.addHandler(handler)

    def send_text(self, msg):
        """ Sends text message through socket connection """
        self.logger.debug('Message sent to client at {}: {}'.format(self.client_address, msg))
        self.client_socket.send(bytes(msg,'UTF-8'))

    def recieve_text(self):
        """ Returns text message recieved by the socket """
        try:
            data = self.client_socket.recv(SERVER_BUFF)
            data = data.decode()
        except:
            self.logger.info('Error on recieve_text at {} with data: {}'.format(self.client_address, data))
        self.logger.debug('Message recieved from client at {}: {}'.format(self.client_address, data))
        return data

    def recieve_file(self, filename, file_size):
        """ Recieves and saves binary file recieved by the socket """
        database.create_database_dir() # creates database directory if it doesnt exist
        # Recieve file data
        file_data = b'' # empty bytes string
        recieved_size = 0
        while True:
            new_data = self.client_socket.recv(SERVER_BUFF)
            recieved_size += len(new_data)
            file_data = file_data + new_data
            if recieved_size >= file_size:
                break
        # write file to database
        success = database.write_file_to_database(filename, file_data)
        if success:
            self.logger.info('User {} uploaded a new file, stored on the path {}'.format(self.username, filename))
        else:
            self.logger.info('Error uploading file for user {} on file {} of size {}'.format(self.username, filename, file_size))
        return success

    def send_file(self, server_filename, file_size):
        """ Sends an binary file through socket """
        filename = database.get_database_file_path(server_filename)
        if filename == '':
            self.logger.info('Error: requested file not found on server. filename: {}'.format(filename))
            return False
        try:
            with open(filename, 'rb') as file:
                file_data = file.read(SERVER_BUFF)
                while file_data:
                    self.client_socket.send(file_data)
                    file_data = file.read(SERVER_BUFF)
        except:
            self.logger.info('Error sending file through socket. Filename {}, file size: {}'.format(filename, file_size))
            return False

        self.logger.info('Sent file {} of size {} to client'.format(filename, file_size))
        return True

    def log_in_request(self, message):
        """ Processes a login request recieved for the client.

        arguments:
            message: expected message is an array on the following format:
                ['Log-in Request', Username, Password]
        """
        username = message[1]
        password = message[2]
        user_exists, password_correct = database.authenticate_user(username, password)

        if user_exists and password_correct:
            print('User authenticated')
            self.send_text('Found')
        elif user_exists:
            print('Authentication failure')
            print ('Password incorrect')
            self.send_text('Password incorrect')
        else:
            print('Authentication failure')
            print('User doesnt exist')
            self.send_text('Not found')

        self.username, self.password = username, password
        self.logger.info('User access authenticated {}'.format(self.username))

    def register_request(self, message):
        """ Process an registration request for the client

        arguments:
            message: expected message is an array on the following format:
                ['Register request', Username, Password]
        """
        username = message[1]
        password = message[2]
        database.register_user(username, password)
        self.logger.info('New Username Registered: ' + username)
        self.send_text('Created')

    def view_files_request(self):
        """ Process view files request
        arguments:
            message: expected message a single string command
                ['View files']
        return:
            dictionary of files of the given user
        """
        user_files = database.get_user_filesystem(self.username)
        if user_files is None or not user_files:
            self.send_text('System is Empty')
            return
        # converts to list
        user_files = list(user_files.keys())
        # converts to comma separated string
        user_files_str = ','.join(user_files)
        self.send_text(user_files_str)

    def upload_request(self, message):
        """ Process an upload of file request

        The message shall be the file contents
        arguments:
            message: expected message is an array on the following format:
                ['Upload request', path_to_file, file_size]
            obs: file_size is stored as string and needs convertion
        """
        path_to_file = message[1]
        file_size = message[2]
        # Updates user filesystem
        filename = database.add_user_filesystem(self.username, path_to_file, file_size)
        self.recieve_file(filename, int(file_size))

    def download_request(self, message):
        """ Process a download file request

        After recieving the request, the server sends and acknoledgment if file is found
        Then performs the file trasfer.

        arguments:
            message: The message shall be of the following format
                ['Download request', path_to_file]
        """
        file_requested = message[1]
        user_files = database.get_user_filesystem(self.username)
        if file_requested not in user_files:
            self.send_text('File not found')
            return
        file_size = user_files[file_requested]['size']
        self.send_text('File exists,{}'.format(file_size))
        time.sleep(0.1)
        server_filename = user_files[file_requested]['location']
        self.send_file(server_filename, file_size)
        time.sleep(0.1)

    def move_file_request(self, message):
        """ Process a move of file request

        Recieves a new key for a given file of user dictionary

        arguments:
            message contains three informations:
                ['Move request',original_filename,target_filename]

        """
        original_filename = message[1]
        target_filename = message[2]
        user_files = database.get_user_filesystem(self.username)
        # Updates dictionary key
        if original_filename in user_files:
            user_files[target_filename] = user_files.pop(original_filename)
            database.update_user_filesystem(self.username, user_files)
            self.send_text('Move succeeded')
        else:
            self.send_text('File not found')

    def remove_file_request(self, message):
        """ Process a remove file request

        Both erases the file from user filesystem dictionary and removes the file.

        arguments:
            message: vetor de strings no formato:
                ['Remove request',filename]

        """
        filename = message[1]
        user_files = database.get_user_filesystem(self.username)
        if filename in user_files:
            user_files.pop(filename)
            database.update_user_filesystem(self.username, user_files)
            self.send_text('Remove succeeded')
        else:
            self.send_text('File not found')
