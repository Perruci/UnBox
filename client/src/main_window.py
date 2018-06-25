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

    def __init__(self):
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
            username = input('Insira o seu nome de usuário:\n -> ')
            password = input('Insira sua senha:\n -> ')
            user_exists, password_correct = self.unbox_app.log_in(username, password)
            if user_exists and password_correct:
                print('User found!\n Opening your filesystem...')
                user_auth = True
            elif user_exists and not password_correct:
                print('Incorrect password...\nTry to login again...')
            elif not user_exists:
                print('Username not found...')
                new_user = input('Create a new user? (y/n)\n-> ')
                if new_user == 'y':
                    self.unbox_app.register(username, password)
                    print('User {} registered with success'.format(username))
                    user_auth = True
                else:
                    print('Try to login again...')
        self.username, self.password = username, password

    def show_files(self):
        """ Imprime o sistema de arquivos recebidos do servidor.

        Caso a mensagem seja 'System is Empty', ainda não há arquivos para este usuário.

        Os arquivos são expressos no seguinte formato:
            - [path/to/file1]
            - [path/to/file2]

        """
        files_csv = self.unbox_app.view_files()
        if files_csv == 'System is Empty':
            print('\t{}, seu sistema de arquivos ainda está vazio...'.format(self.username))
            self.files = ''
            return
        print('{}, seu sistema de arquivos atualmente consiste em:'.format(self.username))
        self.files = files_csv.split(',')
        print(''.join('\t - {}\n'.format(file) for file in self.files))

    def menu(self):
        """ Menu de opções do cliente """
        print('\nOlá {} o/'.format(self.username))
        print('Nesta versão do sistema, você é capaz de:')
        print('\t1 - Visualizar seus arquivos')
        print('\t2 - Download de um arquivo')
        print('\t3 - Upload de um arquivo')
        print('\t4 - Mover um arquivo')
        print('\t5 - Deletar um arquivo')
        print('\t6 - Encerrar sessão')
        choice = get_choice('Qual operação deseja realizar? (1-6)\n-> ')
        while(not choice):
            """ While choice is False, repeat the request """
            print('Operação Inválida...')
            choice = get_choice('Qual operação deseja realizar? (1-6)\n-> ')
        return choice

    def main_loop(self):
        """ Main Loop of the UnBox Application

        Return:
            True for whichever operations beside exit
            False when user choses to end program
        """
        choice = self.menu()

        if choice == '1':
            print('Visualizar seus arquivos foi a sua escolha')
            self.show_files()

        elif choice == '2':
            print('Download de um arquivo foi a sua escolha')
            # view files is called
            self.show_files()
            server_path = input('Qual o caminho para o arquivo que deseja baixar?\n-> ')
            client_path = input('Em qual caminho do seu sistema deseja armazená-lo? (a partir de: client/data/)\n-> ')
            if server_path is '':
                print('Caminho inválido, tente novamente')
            elif server_path not in self.files:
                print('Caminho {} não corresponde a arquivos do servidor.\nTente novamente'.format(server_path))
            else:
                self.unbox_app.download_file(server_path, client_path)

        elif choice == '3':
            print('Upload de um arquivo foi a sua escolha')
            file_path = input('Qual o caminho para o arquivo que deseja enviar?\n-> ')
            target_path = input('Em qual caminho deseja armazená-lo? (nome do arquivo incluso)\n-> ')
            if target_path is '':
                print('Caminho de destino inválido, tente novamente')
            else:
                file_path = file_path.strip() # removes empty spaces on begining and end
                file_path = file_path.replace("'", '')
                target_path = target_path.strip() # removes empty spaces on begining and end
                file_path = file_path.replace("'", '')
                file_exist = self.unbox_app.upload_file(file_path, target_path)
                if file_exist:
                    print('O upload foi realizado com sucesso')
                else:
                    print('O arquivo indicado no caminho ({}) não foi encontrado'.format(file_path))

        elif choice == '4':
            print('Mover um arquivo foi a sua escolha')
            # view files is called
            self.show_files()
            original_path = input('Qual o caminho do arquivo que deseja mover?\n-> ')
            target_path = input('Qual o caminho de destino do arquivo?\n-> ')
            if target_path is '':
                print('Caminho de destino inválido')
            elif original_path is '':
                print('Caminho inválido, tente novamente')
            elif original_path not in self.files:
                print('Caminho {} não corresponde a arquivos do servidor.\nTente novamente'.format(original_path))
            else:
                success = self.unbox_app.move_file(original_path, target_path)
                if success:
                    print('O arquivo foi movido com sucesso')
                else:
                    print('Houve um erro ao mover o arquivo')

        elif choice == '5':
            print('Deletar um arquivo foi a sua escolha')
            # view files is called
            self.show_files()
            server_path = input('Qual o caminho para o arquivo que deseja remover?\n-> ')
            if server_path is '':
                print('Caminho inválido, tente novamente')
            elif server_path not in self.files:
                print('Caminho {} não corresponde a arquivos do servidor.\nTente novamente'.format(server_path))
            else:
                success = self.unbox_app.remove_file(server_path)
                if success:
                    print('O arquivo foi removido com sucesso')
                else:
                    print('Houve um erro ao remover o arquivo')

        elif choice == '6':
            print('Saindo do programa...')
            self.unbox_app.close()
            return False

        return True
