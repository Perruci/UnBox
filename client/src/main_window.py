""" User Interface for UnBox Clients """

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

    def welcome(self):
        """ Mensagem de boas vindas """
        print('Bem vindo ao sistema UnBox\n')
        print('Para ter acesso aos seus dados é necessário efetuar o login.')
        print('Caso ainda não tenha uma conta, iremos criar uma para você.\n')


    def log_in(self):
        """ Futuramente utilizada para realizar o login do usuário no servido """
        self.username = input('Insira o seu nome de usuário:\n ->')
        self.password = input('Insira sua senha:\n ->')
        return self.username, self.password

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
