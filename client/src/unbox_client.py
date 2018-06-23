""" UnBox Client Class File """

import network_client

class UnBoxClient:
    """ Classe UnBoxClient

    Conecta os módulos de comunicação em rede e a interfaçe gráfica para servir o cliente UnBox

    """
    def __init__(self):
        """ Construtor """
        self.client = network_client.NetworkClient()
        self.client.connect()

    def log_in(self, username, password):
        """ Login interface """
        return self.client.log_in(username, password)

    def register(self, username, password):
        """ Register a new user """
        pass

    def close(self):
        self.client.close()
