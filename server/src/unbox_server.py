""" UnBoxServer Class File """

import server_network
import sys

class UnBoxServer:
    """ Classe UnBox Server

    Conecta módulos de rede e processamento de mensagens do servidor UnBox

    """

    def __init__(self):
        """ Construtor """
        self.server = server_network.ServerNetwork()
        self.server.setup()

    def serve(self):
        """ Call service function to reach clients """
        try:
            self.server.monitor()
        except KeyboardInterrupt:
            sys.exit(0)
