""" UnBox Client Class File """

import main_window
import network_client

class UnBoxClient:
    """ Classe UnBoxClient

    Conecta os módulos de comunicação em rede e a interfaçe gráfica para servir o cliente UnBox

    """
    def __init__(self):
        """ Construtor """
        self.client = network_client.NetworkClient()
        self.client.connect()
        self.ui = main_window.MainWindow()
        self.log_in()

    def log_in(self):
        """ UI login and network connection interface """
        self.ui.welcome()
        self.ui.log_in()

    def main_loop(self):
        """ Main Loop of the client """
        self.ui.menu()
        run = True
        while run:
          run = self.client.run()
        self.client.close()
