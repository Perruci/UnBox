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
        username, password = self.ui.log_in()
        if self.client.log_in(username, password):
            print('User found!\n Opening your filesystem...')
            return True
        else:
            print('User not found...\n Create a new user?')
            return False

    def main_loop(self):
        """ Main Loop of the client

        Return:
            True for whichever operations beside exit
            False when user choses to end program
        """
        choice = self.ui.menu()

        if choice == '1':
            print('Option 1 was your choice')

        elif choice == '2':
            print('Option 2 was your choice')

        elif choice == '3':
            print('Option 3 was your choice')

        elif choice == '4':
            print('Option 4 was your choice')

        elif choice == '5':
            print('Option 5 was your choice')

        elif choice == '6':
            print('Option 6 was your choice')
            print('Quitting program')
            self.client.close()
            return False

        run = self.client.run()
        return True
