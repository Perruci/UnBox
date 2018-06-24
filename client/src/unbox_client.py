""" UnBox Client Class File """

import pathlib
import network_client

CLIENT_ROOT = 'client/home/'

def get_path_from_file(file_path):
    """ From a givem file_path, returns the folder path

    eg. file_path = 'path/to/file.txt', returns 'path/to/'
    """
    path = pathlib.Path(file_path)
    return str(path.parents[0])

def create_folder_parents(folder_path):
    """ Creates a folder to host the user files. The default root is CLIENT_ROOT """
    folder_path = CLIENT_ROOT + folder_path
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)

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

    def Download_file(self, server_file, client_file):
        """ Cria diretório solicitado pelo usuário e solicita o Download de arquivo do servidor """
        # Cria diretório solicitado pelo usuário
        client_path = get_path_from_file(client_file)
        create_folder_parents(client_path)
        client_file = CLIENT_ROOT + client_file
        self.client.download_file(server_file, client_file)

    def move_file(self, original_file, target_file):
        """ Solicita a mudança no caminho para o arquivo no servidor """
        return self.client.request_move_file(original_file, target_file)

    def close(self):
        self.client.close()
