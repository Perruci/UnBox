""" UnBox Client Class File """

import pathlib
import network_client

def file_exists(file_path):
    """ Returns true if file exists, false if it doesnt """
    file = pathlib.Path(file_path)
    return file.is_file()

def get_file_size(file_path):
    """ Returns file size """
    file = pathlib.Path(file_path)
    return file.stat().st_size

class UnBoxClient:
    """ Classe UnBoxClient

    Conecta os módulos de comunicação em rede e a interfaçe gráfica para servir o cliente UnBox

    """
    def __init__(self):
        """ Construtor """
        self.client = network_client.NetworkClient()

    def log_in(self, username, password):
        """ Login interface """
        return self.client.log_in(username, password)

    def register(self, username, password):
        """ Register a new user """
        self.client.register(username, password)

    def view_files(self):
        """ Requests user filesystem """
        return self.client.request_filesystem()

    def upload_file(self, file_path, target_path):
        """ Verify file existance and size, then calls a file transfer on client
        arguments:
            file_path: path to the pretended upload file
            target_path: path to be stored on server
        return:
            True if file exists, false otherwise
        """
        if not file_exists(file_path):
            return False
        file_size = get_file_size(file_path)
        self.client.upload_file(file_path, target_path, file_size)
        return True

    def close(self):
        self.client.close()
