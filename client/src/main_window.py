""" User Interface for UnBox Clients """

import unbox_client

def get_choice(message):
    """ get_choice

    Captura operação escolhida pelo usuário.
    Retorna falso para operações inválidas e o valor da escolha para operações verdadeiras.
    """
    choice = str(input(message))
    if choice == '':
        return False
    elif choice[0] < '1' or choice[0] > '6':
        return False
    else:
        return choice

class MainWindow:
    """ Main Window

    Classe que abrange funções e variáveis da interface gráfica

    """

    def __init___(self):
        """ Construtor """
        pass

    def setup(self):
        """ Basic UnBox app configuration """
        self.unbox_app = unbox_client.UnBoxClient()
        self.welcome()
        self.log_in()

    def welcome(self):
        """ Mensagem de boas vindas """
        print('Bem vindo ao sistema UnBox\n')
        print('Para ter acesso aos seus dados é necessário efetuar o login.')
        print('Caso ainda não tenha uma conta, iremos criar uma para você.\n')


    def log_in(self):
        """ Futuramente utilizada para realizar o login do usuário no servido """
        user_auth = False
        while not user_auth:
            username = input('Insira o seu nome de usuário:\n ->')
            password = input('Insira sua senha:\n ->')
            user_exists, password_correct = self.unbox_app.log_in(username, password)
            if user_exists and password_correct:
                print('User found!\n Opening your filesystem...')
                user_auth = True
            elif user_exists and not password_correct:
                print('Incorrect password...\nTry to login again...')
            elif not user_exists:
                print('Username not found...')
                new_user = input('Create a new user? (y/n)\n->')
                if new_user == 'y':
                    self.unbox_app.register(username, password)
                    print('User {} registered with success'.format(username))
                    user_auth = True
                else:
                    print('Try to login again...')
        self.username, self.password = username, password

    def menu(self):
        """ Menu de opções do cliente """
        print('Nesta versão do sistema, você é capaz de:')
        print('\t1 - Visualizar seus arquivos')
        print('\t2 - Download de um arquivo')
        print('\t3 - Download de uma pasta')
        print('\t4 - Upload de um arquivo')
        print('\t5 - Upload de uma pasta')
        print('\t6 - Encerrar sessão')
        choice = get_choice('Qual operação deseja realizar? (1-6)\n->')
        while(not choice):
            """ While choice is False, repeat the request """
            print('Operação Inválida...')
            choice = get_choice('Qual operação deseja realizar? (1-6)\n->')
        return choice

    def main_loop(self):
        """ Main Loop of the UnBox Application

        Return:
            True for whichever operations beside exit
            False when user choses to end program
        """
        choice = self.menu()

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
            self.unbox_app.close()
            return False

        return True
