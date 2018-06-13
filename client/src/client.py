""" Client main file """

import main_window
import network_client

def main():
    client = network_client.NetworkClient()
    client.connect()
    ui = main_window.MainWindow()
    ui.welcome()
    ui.log_in()
    ui.menu()
    run = True
    while run:
      run = client.run()
    client.close()

if __name__ == '__main__':
    main()
