""" Classe responsável por receber cada cliente em uma Thread """

import socket
import threading
import logging

import database

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
        msg = ''
        while True:
            msg = self.recieve_text()
            if msg=='bye':
                print ('User {} at {} disconnected...'.format(self.username, self.client_address))
                break
            # Processes an operation commands (comma separated) -----------------------------
            split_msg = msg.split(',')
            if split_msg[0] == 'Log-in request':
                self.log_in_request(split_msg)
            if split_msg[0] == 'Register request':
                self.register_request(split_msg)
            if split_msg[0] == 'Upload request':
                self.upload_request(split_msg)
            if split_msg[0] == 'View files':
                self.view_files_request()

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
        data = self.client_socket.recv(2048)
        data = data.decode()
        self.logger.debug('Message recieved from client at {}: {}'.format(self.client_address, data))
        return data

    def log_in_request(self, message):
        """ Processes a login request recieved for the client.

        arguments:
            message: expected message is an array on the following format:
                ['Log-in Request', Username, Password]
        """
        print(message[0])
        username = message[1]
        password = message[2]
        print('\t Username: {}'.format(username))
        print('\t Password: {}'.format(password))
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
        if user_files is None:
            self.send_text('System is Empty')
            return
        # converts to list
        user_files = list(user_files.keys())
        # converts to comma separated string
        user_files_str = ','.join(user_files)
        self.send_text(user_files_str)

    def upload_request(self, message):
        """ Process an upload of file request

        The next message shall be the file contents
        arguments:
            message: expected message is an array on the following format:
                ['Upload request', path_to_file, file_size]
            obs: file_size is stored as string and needs convertion
        """
        path_to_file = message[1]
        file_size = message[2]
        # Updates user filesystem
        database.add_user_filesystem(self.username, path_to_file, file_size)
        # TODO: actual file transfer
